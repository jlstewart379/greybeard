from greybeard.models.change_model import DiffBlock, ChangeBlock, Suggestion

def test_suggestion_structure():
    diff = DiffBlock(start_line=1, end_line=3, original=["a\n"], replacement=["b\n"])
    block = ChangeBlock(label="test", reason="test reason", diff=diff)
    suggestion = Suggestion(path="file.tf", change_blocks=[block])

    assert suggestion.path == "file.tf"
    assert suggestion.change_blocks[0].label == "test"
    assert suggestion.change_blocks[0].diff.original == ["a\n"]
    assert suggestion.change_blocks[0].diff.replacement == ["b\n"]

