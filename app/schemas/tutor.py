"""Structured-output models for the Student AI Tutor."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_index: int
    explanation: str


class Quiz(BaseModel):
    questions: List[QuizQuestion]


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardSet(BaseModel):
    cards: List[Flashcard]
