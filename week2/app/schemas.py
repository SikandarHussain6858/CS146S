from __future__ import annotations

from pydantic import BaseModel, Field


class ExtractRequest(BaseModel):
    text: str = Field(min_length=1)
    save_note: bool = False


class DoneRequest(BaseModel):
    done: bool = True


class CreateNoteRequest(BaseModel):
    content: str = Field(min_length=1)
