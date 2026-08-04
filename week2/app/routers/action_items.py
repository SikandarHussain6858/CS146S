from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import DoneRequest, ExtractRequest
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


def _save_and_extract(text: str, items: List[str], save_note: bool) -> Dict[str, Any]:
    note_id: Optional[int] = None
    if save_note:
        note_id = db.insert_note(text)

    ids = db.insert_action_items(items, note_id=note_id)
    return {"note_id": note_id, "items": [{"id": i, "text": t} for i, t in zip(ids, items)]}


@router.post("/extract")
def extract(payload: ExtractRequest) -> Dict[str, Any]:
    text = payload.text.strip()
    items = extract_action_items(text)
    return _save_and_extract(text, items, payload.save_note)


@router.post("/extract-llm")
def extract_llm(payload: ExtractRequest) -> Dict[str, Any]:
    text = payload.text.strip()
    items = extract_action_items_llm(text)
    return _save_and_extract(text, items, payload.save_note)


@router.get("")
def list_all(note_id: Optional[int] = None) -> List[Dict[str, Any]]:
    rows = db.list_action_items(note_id=note_id)
    return [
        {
            "id": r["id"],
            "note_id": r["note_id"],
            "text": r["text"],
            "done": bool(r["done"]),
            "created_at": r["created_at"],
        }
        for r in rows
    ]


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, payload: DoneRequest) -> Dict[str, Any]:
    db.mark_action_item_done(action_item_id, payload.done)
    return {"id": action_item_id, "done": payload.done}


