# Multi-Agent AI Suite

> Local multi-agent AI Python code generator with Web UI, CLI, and VS Code extension.



## Overview

Multi-Agent AI Suite is a local AI coding assistant designed to generate and review Python code using a multi-agent workflow.

The project combines multiple interfaces around a shared FastAPI backend:

* Streamlit Web Application
* Command Line Interface
* VS Code Extension

The entire pipeline runs locally using open-source Qwen models.



## Features

* Multi-agent architecture
* Local LLM inference
* Streamlit Web UI
* Command Line Interface
* VS Code extension
* FastAPI backend
* Code review pipeline
* Sandboxed code execution
* Import validation
* Offline operation



## Web Application

Generate Python code through a browser interface.

![Web Application](assets/web_ui_Video.gif)

---

## VS Code Extension

Generate Python code directly inside Visual Studio Code.

![VS Code Extension](assets/vscode_ui.gif)

---

## Command Line Interface

![CLI](assets/cli_ui.png)

Generate Python code from the terminal.



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

Choose:

```text
1. Launch Web Application
2. Launch CLI
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



### Visual Studio Code Extension Setup

Open the extension project:

```bash
cd multi-agent-ai-vscode
```

Install the dependencies:

```bash
npm install
```

Launch the Extension Development Host:

```text
Press F5
```

A new VS Code window will open.

### Usage

1. Start the AI backend


```bash
uvicorn backend.app:app --reload
```

2. In the Extension Development Host

* Open a Python file
* Press `Ctrl + Shift + P`
* Run `Generate Python Code`
* Enter your prompt

Example:

```text
Generate bubble sort for five integers
```

The generated code will be inserted into the active editor.




## Project Structure

```text
multi-agent-ai-suite
│
├── README.md
├── assets
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
    ├── package.json
    └── tsconfig.json
```



## Technology Stack

### Backend

* Python
* FastAPI
* PyTorch
* Hugging Face Transformers

### Frontend

* Streamlit

### Extension

* TypeScript
* VS Code Extension API

### Models

* Qwen2.5-Coder-1.5B-Instruct
* Qwen2.5-Coder-3B-Instruct



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
Sandbox Execution
      │
      ▼
Generated Python Code
```



## Future Improvements

* Additional specialized agents
* Better hallucination reduction
* More programming languages
* Packaged VS Code extension
* Improved prompt engineering



## License

This project is licensed under the MIT License.
