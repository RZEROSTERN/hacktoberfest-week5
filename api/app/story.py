"""Typed authored content, shared by future dialogue and deterministic game logic."""

import json
from datetime import date
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Authored(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Localized(Authored):
    en: str = Field(min_length=1)
    es: str = Field(min_length=1)


class Fact(Authored):
    id: str
    text: Localized
    revealed_by: list[str] = Field(min_length=1)


class Person(Authored):
    id: str
    name: str
    relationship: Localized
    revealed_by: list[str] = Field(min_length=1)


class Spirit(Authored):
    name: str
    born: date
    died: date
    home: str
    place_is_fictional: bool
    era: Localized
    trade: Localized
    personality: Localized
    voice: Localized


class Canon(Authored):
    schema_version: Literal[1]
    review_status: Literal["pending_owner_approval", "approved"]
    id: str
    title: Localized
    premise: Localized
    player_role: Localized
    spirit: Spirit
    people: list[Person]
    facts: list[Fact]
    guardrails: list[str]


class Memory(Authored):
    id: str
    title: Localized
    scene: Localized
    fact_ids: list[str] = Field(min_length=1)


class Relevance(Authored):
    accept: Localized
    reject: Localized


class Fallbacks(Authored):
    unrecovered: Localized
    connected: Localized
    recovered: Localized
    unrelated: Localized
    redirect: Localized
    error: Localized


class Object(Authored):
    id: str
    title: Localized
    description: Localized
    hint: Localized
    memory: Memory
    relevance: Relevance
    fallbacks: Fallbacks


class Ending(Authored):
    id: str
    condition: Literal["all_memories", "some_memories", "no_memories"]
    title: Localized
    scene: Localized


class Story(Authored):
    canon: Canon
    objects: list[Object] = Field(min_length=5, max_length=6)
    endings: list[Ending] = Field(min_length=3, max_length=3)
    lines: dict[str, Localized]

    @model_validator(mode="after")
    def consistent_references(self) -> Self:
        def unique(values: list[str], label: str) -> set[str]:
            result = set(values)
            if len(result) != len(values):
                raise ValueError(f"Duplicate {label}")
            return result

        object_ids = unique([obj.id for obj in self.objects], "object ids")
        fact_ids = unique([fact.id for fact in self.canon.facts], "fact ids")
        unique([person.id for person in self.canon.people], "person ids")
        unique([obj.memory.id for obj in self.objects], "memory ids")
        unique([ending.id for ending in self.endings], "ending ids")
        if {ending.condition for ending in self.endings} != {
            "all_memories",
            "some_memories",
            "no_memories",
        }:
            raise ValueError("All three ending conditions must be present")
        if self.canon.spirit.born >= self.canon.spirit.died:
            raise ValueError("The spirit's life dates are reversed")
        reveal_items: list[Person | Fact] = [*self.canon.people, *self.canon.facts]
        for item in reveal_items:
            if not set(item.revealed_by) <= object_ids:
                raise ValueError(f"Unknown reveal object for {item.id}")
        for obj in self.objects:
            if not set(obj.memory.fact_ids) <= fact_ids:
                raise ValueError(f"Unknown fact for {obj.id}")
            expected = {fact.id for fact in self.canon.facts if obj.id in fact.revealed_by}
            if set(obj.memory.fact_ids) != expected:
                raise ValueError(f"Fact reveal mismatch for {obj.id}")
        required_lines = {
            "opening",
            "early",
            "middle",
            "late",
            "empty_message",
            "redirect",
            "unavailable",
            "resume",
            "memory_recovered",
            "ending",
        }
        if not required_lines <= self.lines.keys():
            raise ValueError("Missing game-state fallback lines")
        return self


def load_story(directory: Path) -> Story:
    """Read an explicit directory, so callers can pass packaged or test paths."""
    names = {
        "canon": "canon.json",
        "objects": "objects.json",
        "endings": "endings.json",
        "lines": "lines.json",
    }
    return Story.model_validate(
        {
            key: json.loads((directory / filename).read_text(encoding="utf-8"))
            for key, filename in names.items()
        }
    )
