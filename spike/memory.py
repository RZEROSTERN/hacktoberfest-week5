"""macOS physical footprint, using the public Xcode SDK rusage_info_v2 layout.

Other platforms keep the portable process-tree RSS and Ollama allocation metrics.
No third-party library or elevated privilege is required for owned processes.
"""

import ctypes
import sys


class RUsageV2(ctypes.Structure):
    _fields_ = [("ri_uuid", ctypes.c_uint8 * 16)] + [
        (name, ctypes.c_uint64)
        for name in (
            "ri_user_time",
            "ri_system_time",
            "ri_pkg_idle_wkups",
            "ri_interrupt_wkups",
            "ri_pageins",
            "ri_wired_size",
            "ri_resident_size",
            "ri_phys_footprint",
            "ri_proc_start_abstime",
            "ri_proc_exit_abstime",
            "ri_child_user_time",
            "ri_child_system_time",
            "ri_child_pkg_idle_wkups",
            "ri_child_interrupt_wkups",
            "ri_child_pageins",
            "ri_child_elapsed_abstime",
            "ri_diskio_bytesread",
            "ri_diskio_byteswritten",
        )
    ]


def physical_footprint(pid: int) -> int | None:
    if sys.platform != "darwin":
        return None
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    call = library.proc_pid_rusage
    call.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    call.restype = ctypes.c_int
    data = RUsageV2()
    if call(pid, 2, ctypes.byref(data)) != 0:  # RUSAGE_INFO_V2 in sys/resource.h
        raise OSError(ctypes.get_errno(), "Could not read owned process footprint")
    return int(data.ri_phys_footprint)
