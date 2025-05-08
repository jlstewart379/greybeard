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

