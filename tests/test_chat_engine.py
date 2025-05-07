from chat_engine import parse_suggestion_from_reply

def test_parse_valid_reply():
    reply = '''```json
{
  "path": "main.tf",
  "label": "Add logging",
  "reason": "Improve modularity",
  "diff": {
    "start_line": 5,
    "end_line": 8,
    "original": ["line1\n"],
    "replacement": ["line2\n"]
  }
}
```'''
    slug, suggestion = parse_suggestion_from_reply(reply)
    assert suggestion.path == "main.tf"
    assert suggestion.change_blocks[0].label == "Add logging"

