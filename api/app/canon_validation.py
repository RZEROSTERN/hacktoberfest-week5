"""Finite, conservative canon checks for the spike, not a semantic proof of truth.

The benchmark must separately audit uncaught contradictions and false positives.
This prototype is not wired to a player-facing endpoint.
"""

import re
import unicodedata

from app.ollama import Proposal
from app.story import Story


def normalize(text: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", text.casefold())
        if not unicodedata.combining(char)
    )


def validate_proposal(story: Story, proposal: Proposal, recovered: set[str]) -> list[str]:
    text = normalize(proposal.reply)
    visible = {fact.id for fact in story.canon.facts if recovered.intersection(fact.revealed_by)}
    reasons: list[str] = []
    if not set(proposal.fact_ids) <= visible:
        reasons.append("unavailable_fact_reference")
    for person in story.canon.people:
        first = normalize(person.name.split()[0])
        if re.search(rf"\b{first}\b", text) and not recovered.intersection(person.revealed_by):
            reasons.append(f"locked_person:{person.id}")

    identity = normalize(story.canon.spirit.name)
    for match in re.finditer(r"(?:my name is|me llamo|mi nombre es)\s+([a-z]+)", text):
        if not identity.startswith(match[1]) or "identity" not in visible:
            reasons.append("wrong_or_locked_identity")

    visible_text = " ".join(
        normalize(fact.text.en + " " + fact.text.es)
        for fact in story.canon.facts
        if fact.id in visible
    )
    visible_text += " " + " ".join(
        normalize(obj.memory.scene.en + " " + obj.memory.scene.es)
        for obj in story.objects
        if obj.id in recovered
    )
    allowed_years = set(re.findall(r"\b\d{4}\b", visible_text)) | {"2026"}
    if set(re.findall(r"\b\d{4}\b", text)) - allowed_years:
        reasons.append("unknown_or_locked_year")
    for cue, year, fact_id in [
        (r"born|naci(?:o)?", str(story.canon.spirit.born.year), "identity"),
        (r"died|mori|murio", str(story.canon.spirit.died.year), "death"),
    ]:
        for match in re.finditer(rf"\b(?:{cue})\b[^.!?]*?\b(\d{{4}})\b", text):
            if match[1] != year or fact_id not in visible:
                reasons.append("wrong_life_date")

    roles = {
        "father": "aurelio",
        "padre": "aurelio",
        "husband": "ernesto",
        "esposo": "ernesto",
        "son": "julian",
        "hijo": "julian",
        "granddaughter": "lucia",
        "nieta": "lucia",
        "friend": "berta",
        "amiga": "berta",
        "neighbor": "berta",
        "vecina": "berta",
    }
    people = [normalize(person.name.split()[0]) for person in story.canon.people]
    names_pattern = "|".join(people)
    for role, expected in roles.items():
        patterns = [
            rf"\b(?:my|mi) {role}\b"
            rf"(?:\s+(?:is|was|es|era|se llama|called|named))?\s+({names_pattern})\b",
            rf"\b({names_pattern})\b(?:\s+\w+){{0,2}}\s+(?:is|was|es|era)\s+(?:my|mi) {role}\b",
        ]
        if any(
            match[1] != expected for pattern in patterns for match in re.finditer(pattern, text)
        ):
            reasons.append("wrong_relationship")
    if re.search(r"\b(?:my daughter|mi hija|two sons|dos hijos|three children|tres hijos)\b", text):
        reasons.append("invented_family")
    if re.search(r"\b(?:you are|eres) (?:my|mi)\b", text):
        reasons.append("player_assigned_family")

    for match in re.finditer(
        r"\b(?:i was a|i am a|i worked as a|worked as a|era una?|fui una?|trabajaba como)"
        r"\s+([a-z ]+)",
        text,
    ):
        if "trade" not in visible or not re.match(
            r"(?:radio repair|reparadora? de radios)", match[1]
        ):
            reasons.append("unsupported_occupation")
    if re.search(
        r"\b(?:never repaired|nunca repare|never had a family|nunca tuve familia)\b", text
    ):
        reasons.append("negated_canon")
    if re.search(
        r"\b(?:murdered|asesinada|car crash|accidente|drowned|ahogada|curse|maldicion|zombie)\b",
        text,
    ):
        reasons.append("unsupported_death_or_tone")

    if (
        re.search(r"\b(?:never had (?:a |any )?sons?|nunca tuve (?:un |ningun )?hijo)\b", text)
        and "family" in visible
    ):
        reasons.append("negated_known_family")
    if (
        re.search(
            r"\b(?:never met (?:my )?granddaughter|nunca conoci (?:a )?(?:mi )?nieta)\b", text
        )
        and "teaching" in visible
    ):
        reasons.append("negated_known_teaching")
    if re.search(
        r"\b(?:learned|learnt|aprendi)\b[^.!?]*"
        r"(?:after (?:i )?died|despues de morir)",
        text,
    ):
        reasons.append("impossible_life_sequence")

    # Proper nouns outside the visible canon are suspicious. This is intentionally
    # conservative and its false-positive rate must be reported, not hidden.
    allowed_words = set(re.findall(r"\w+", visible_text))
    for sentence in re.split(r"[.!?]\s*", proposal.reply):
        words = re.findall(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b", sentence)
        for word in words[1:]:
            if normalize(word) not in allowed_words:
                reasons.append("unknown_proper_noun")
    if re.search(
        r"\b(?:system prompt|developer message|ignore previous|instrucciones del sistema)\b", text
    ):
        reasons.append("out_of_character")
    return sorted(set(reasons))
