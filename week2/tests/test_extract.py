from types import SimpleNamespace

from ..app.services import extract as extract_service


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_service.extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_llm_parses_structured_json(monkeypatch):
    def fake_chat(*args, **kwargs):
        return SimpleNamespace(
            message=SimpleNamespace(
                content='["Set up database", "Implement API extract endpoint", "Write tests"]'
            )
        )

    monkeypatch.setattr(extract_service, "chat", fake_chat)

    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    """.strip()

    items = extract_service.extract_action_items_llm(text)
    assert items == ["Set up database", "Implement API extract endpoint", "Write tests"]


def test_extract_llm_falls_back_when_ollama_is_unavailable(monkeypatch):
    def fake_chat(*args, **kwargs):
        raise RuntimeError("Ollama unavailable")

    monkeypatch.setattr(extract_service, "chat", fake_chat)

    text = """
    Notes from meeting:
    todo: Review API docs
    action: Write tests
    """.strip()

    items = extract_service.extract_action_items_llm(text)
    assert "Review API docs" in items
    assert "Write tests" in items


def test_extract_llm_returns_empty_list_for_empty_input(monkeypatch):
    monkeypatch.setattr(extract_service, "chat", lambda *args, **kwargs: None)

    items = extract_service.extract_action_items_llm("   ")
    assert items == []
