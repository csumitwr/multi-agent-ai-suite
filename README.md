# Multi-Agent AI Suite

Local multi-agent AI Python code generator with Web UI, CLI and Visual Studio Code extension.

![Streamlit Demo](assets/web_ui_Video.gif)

---

## 📌 Overview

Multi-Agent AI Suite is a local AI coding assistant that generates and reviews Python code using a multi-agent architecture.

The project includes three different interfaces:

* Streamlit Web Application
* Command Line Interface
* VS Code Extension

The entire pipeline runs locally using open-source Qwen models.

---

## Features

* Multi-Agent Architecture
* Local LLM Inference
* Streamlit Web UI
* Command Line Interface
* VS Code Extension
* FastAPI Backend
* Code Review Pipeline
* Sandboxed Code Execution
* Import Validation
* Offline Operation

---

## Web Application

![Web UI](assets/web_ui_Video.gif)

Generate Python code through a simple browser interface.

---

## VS Code Extension

![VS Code Extension](assets/vscode_ui.gif)

Generate Python code directly inside Visual Studio Code.

---

## Command Line Interface

![CLI](assets/cli_ui.png)

Generate Python code from the terminal.

---

## Project Structure

```text
multi-agent-ai-suite
│
├── multi-agent-ai
│   ├── agents
│   ├── backend
│   ├── cli
│   ├── frontend
│   ├── models
│   ├── pipeline
│   └── main.py
│
└── multi-agent-ai-vscode
    ├── src
    └── package.json
```

---

## Tech Stack

* Python
* FastAPI
* Streamlit
* PyTorch
* Hugging Face Transformers
* TypeScript
* VS Code Extension API

---

## Installation

### Clone the repository

```bash
git clone https://github.com/csumitwr/multi-agent-ai-suite.git
```

### Install dependencies

```bash
pip install -r multi-agent-ai-suite/requirements.txt
```

### Download the models

```bash
python -m models.download_model
```

### Run the application

```bash
python main.py
```

### OR

```bash
uvicorn backend.app:app --reload
```

```bash
streamlit run frontend/app.py
```
```text
Run the backedn first and then the streamlit UI
```

Choose:

```text
1. Launch Web Application
2. Launch CLI
```

---

## Multi-Agent Workflow

```text
User Prompt
      │
      ▼
 FastAPI Backend
      │
      ▼
 Code Agent
      │
      ▼
 Review Agent
      │
      ▼
 Sandbox
      │
      ▼
 Generated Python Code
```

---

## Future Improvements

* Additional AI agents
* More programming languages
* Better hallucination reduction
* Packaged VS Code extension
* Improved prompt engineering

---

## License

This project is licensed under the MIT License.