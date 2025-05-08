# 🧙 Greybeard

**Greybeard** is a terminal-native AI assistant for infrastructure engineers. It analyzes your codebase using OpenAI's GPT models and gives actionable suggestions — with inline diffs and the ability to apply changes directly from the terminal.

---

## 🚀 Features

- GPT-4-powered CLI assistant
- Automatic project context loading
- Intelligent file ignore system (`.greybeardignore`)
- Suggestion review: preview, apply, or skip
- JSON diff-based patching
- File-based suggestion history
- Python 3.11 compatible

---

## 📦 Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/)
- An OpenAI API key

---

## 🛠 Setup

### Option 1: Manual

```bash
git clone git@github.com:your-username/greybeard.git
cd greybeard
python3.11 -m venv .venv
source .venv/bin/activate
poetry install
poetry env use .venv/bin/python
export OPENAI_API_KEY="sk-..."
```

### Option 2: One-Line Bootstrap

```bash
chmod +x bootstrap_greybeard.sh
./bootstrap_greybeard.sh
```

---

## 💬 Usage

### 🧭 Basic Command

```bash
poetry run greybeard chat --path .
```

### 🧾 Options

| Flag     | Description                          | Default |
|----------|--------------------------------------|---------|
| `--path` | Root path to analyze for context     | `.`     |
| `--help`| Show help message                    |         |

### 🧠 Example Prompts

You can ask Greybeard:

- `Suggest a refactor for my Terraform output blocks`
- `How can I modularize this Helm chart?`
- `Propose a logging abstraction for main.tf`
- `Is there a better way to structure my ECS task definition?`

### 📘 Sample Interaction

```bash
poetry run greybeard chat --path .
```

```
🧠 You: Suggest a logging module refactor for main.tf

📥 Greybeard:
```json
{
  "path": "main.tf",
  "label": "Add logging module",
  "reason": "Improve modularity and reuse",
  "diff": {
    "start_line": 10,
    "end_line": 14,
    "original": [
      "  log_configuration {",
      "    log_driver = \"awslogs\"",
      "  }"
    ],
    "replacement": [
      "  module \"logging\" {",
      "    source = \"../modules/logging\"",
      "  }"
    ]
  }
}
```

🔧 Terminal then prompts:
```
What would you like to do? [apply|save|skip]
```

---

## 📂 Directory Structure

```
greybeard/
├── greybeard/                  # Core app logic
│   ├── cli.py
│   ├── chat_engine.py
│   ├── context_loader.py
│   ├── diff_engine.py
│   ├── models/
│   │   └── change_model.py
│   └── storage/
│       ├── suggestion_store.py
│       └── journal.py
├── tests/                      # Pytest unit tests
├── .greybeard/                 # Runtime suggestions
│   └── suggestions/
├── pyproject.toml              # Poetry-managed metadata
├── README.md
└── bootstrap_greybeard.sh
```

---

## 🧪 Run Tests

```bash
poetry run pytest
```

Covers:
- Suggestion models
- Suggestion store (save/load)
- GPT reply parsing

---

## 🔐 API Access

You'll need an [OpenAI API key](https://platform.openai.com/account/api-keys). Set it like this:

```bash
export OPENAI_API_KEY="sk-..."
```

---

## 📄 License

MIT. Use freely and adapt for internal tools or custom workflows.

---

## 🤝 Contributing

Greybeard is in early development. Feature suggestions, issues, and PRs are welcome!

Planned features:
- Persistent chat session history
- Undo/redo change journal
- Multi-suggestion batching
