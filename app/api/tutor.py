"""Student AI Tutor endpoints: explain, quiz, flashcards, notes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.tutor import FlashcardSet, Quiz
from app.services.tutor_service import (
    TutorError,
    explain_topic,
    generate_flashcards,
    generate_notes,
    generate_quiz,
)

router = APIRouter(prefix="/tutor", tags=["tutor"])


class ExplainRequest(BaseModel):
    topic: str
    level: str = "beginner"


class ExplainResponse(BaseModel):
    explanation: str


class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "medium"


class FlashcardsRequest(BaseModel):
    topic: str
    count: int = 10


class NotesRequest(BaseModel):
    topic: str


class NotesResponse(BaseModel):
    notes_markdown: str


@router.post("/explain", response_model=ExplainResponse)
async def explain_endpoint(request: ExplainRequest):
    try:
        return ExplainResponse(explanation=explain_topic(request.topic, request.level))
    except TutorError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc


@router.post("/quiz", response_model=Quiz)
async def quiz_endpoint(request: QuizRequest):
    try:
        return generate_quiz(request.topic, request.num_questions, request.difficulty)
    except TutorError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc


@router.post("/flashcards", response_model=FlashcardSet)
async def flashcards_endpoint(request: FlashcardsRequest):
    try:
        return generate_flashcards(request.topic, request.count)
    except TutorError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc


@router.post("/notes", response_model=NotesResponse)
async def notes_endpoint(request: NotesRequest):
    try:
        return NotesResponse(notes_markdown=generate_notes(request.topic))
    except TutorError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
