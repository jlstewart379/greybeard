from greybeard.models.change_model import DiffBlock, ChangeBlock, Suggestion
from greybeard.storage.suggestion_store import save_suggestion, load_suggestions
import os
import shutil

TEST_DIR = ".greybeard/suggestions"

def test_save_and_load_suggestion():
    os.makedirs(TEST_DIR, exist_ok=True)
    diff = DiffBlock(start_line=1, end_line=2, original=["line1\n"], replacement=["line2\n"])
    block = ChangeBlock(label="log", reason="improve", diff=diff)
    suggestion = Suggestion(path="demo.tf", change_blocks=[block])

    slug = "test-demo"
    save_suggestion(suggestion, slug)
    suggestions = load_suggestions()

    assert any(s.path == "demo.tf" for s in suggestions)

