"""Shared state (the agents' memory) and the structured output schemas."""
import operator
from typing import Annotated, TypedDict
from pydantic import BaseModel


class Points(BaseModel):
    points: list[str]            # each point ~25 words max


class Verdict(BaseModel):
    recommendation: str          # Yes / No / Yes, with conditions + one line
    confidence: int              # 0-100
    deciding_factors: list[str]  # 3 items
    risks: list[str]             # 2 items
    first_step: str


class Questions(BaseModel):
    questions: list[str]


class Brief(BaseModel):
    brief: str


class DebateState(TypedDict):
    decision: str
    brief: str
    round: int
    arguments: Annotated[list[dict], operator.add]  # appended, never overwritten
    verdict: dict
