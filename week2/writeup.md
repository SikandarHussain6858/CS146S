# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Student** \
SUNet ID: **TODO** \
Citations: **Ollama structured output docs, FastAPI docs, existing course starter code**

This assignment took me about **2** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Implement an LLM-powered alternative to extract_action_items() in week2/app/services/extract.py using Ollama with structured JSON output, with a clean fallback to the existing heuristic parser when Ollama is unavailable.
``` 

Generated Code Snippets:
```
week2/app/services/extract.py
- Added extract_action_items_llm() and an Ollama chat call using model OLLAMA_MODEL (default: llama3.1:8b).
- Added JSON parsing and a graceful fallback to extract_action_items() when the model call fails.
- Added _clean_item_text() and _deduplicate() to keep the output stable and consistent.
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Write unit tests for the LLM extractor covering bullet lists, keyword-prefixed lines, empty input, and a fallback path when Ollama raises an error.
``` 

Generated Code Snippets:
```
week2/tests/test_extract.py
- Added test_extract_llm_parses_structured_json()
- Added test_extract_llm_falls_back_when_ollama_is_unavailable()
- Added test_extract_llm_returns_empty_list_for_empty_input()
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor the backend to use typed request schemas, clean up route logic, and improve the separation between validation, persistence, and extraction logic.
``` 

Generated/Modified Code Snippets:
```
week2/app/schemas.py
- Added typed Pydantic request models for extraction, note creation, and done-state updates.

week2/app/routers/action_items.py
- Replaced raw dict payload handling with typed request models.
- Added a shared _save_and_extract() helper to keep the endpoint logic concise and consistent.

week2/app/routers/notes.py
- Added the list-notes endpoint and refactored note creation to use the schema type.
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Add a new LLM-powered endpoint and wire the frontend to support an Extract LLM button plus a List Notes button that fetches and displays saved notes.
``` 

Generated Code Snippets:
```
week2/app/routers/action_items.py
- Added POST /action-items/extract-llm.

week2/frontend/index.html
- Added Extract LLM and List Notes buttons.
- Updated the frontend logic to call the new endpoint and render notes from /notes.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Inspect the current codebase and generate a concise README describing the project overview, setup steps, endpoints, and test command.
``` 

Generated Code Snippets:
```
week2/README.md
- Added a new project README describing the architecture, setup, API endpoints, and how to run the test suite.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 