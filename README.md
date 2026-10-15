# 🔎 Deep Research Desk

A multi-agent research application with a Streamlit interface. Enter any topic and four AI agents work in sequence to search the web, read the best source, write a full report and critique it.

## Features

- **Four-stage pipeline** with live progress: Search, Read, Write, Critique
- **Full written report** you can download as a Markdown file
- **Critic feedback** that points out weaknesses in the report
- **Source transparency**: view the raw search results and the scraped page
- **Past reports** kept in the sidebar for the current session
- **Three colour themes**: Aurora (dark), Daylight (light) and Sunset (dark)

## How it works

| Step | Agent | What it does |
|------|-------|--------------|
| 1 | Search agent | Finds recent, reliable information about the topic |
| 2 | Reader agent | Picks the most relevant URL and scrapes it for deeper content |
| 3 | Writer chain | Drafts a report from the search results and scraped content |
| 4 | Critic chain | Reviews the report and gives feedback |

## Project structure

```
multi-agent-application/
├── app.py             # Streamlit user interface
├── agents.py          # Agent and chain definitions
├── tools.py           # Tools used by the agents (search, scraping)
├── pipeline.py        # Command-line version of the pipeline
├── requirements.txt   # Python dependencies
├── .env               # API keys (local only, never commit this)
└── .gitignore
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/deep-research-desk.git
cd deep-research-desk
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

Create a file named `.env` in the project folder and add the keys your `agents.py` and `tools.py` use. For example:

```
OPENAI_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```

The key names above are examples. Use the names your code actually reads.

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Command-line version

To run the pipeline without the interface:

```bash
python pipeline.py
```

## Deploying for free on Streamlit Community Cloud

1. Push this project to a public GitHub repository. Do not upload `.env`.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app**, choose your repository, set the branch to `main` and the main file to `app.py`.
4. Open **Advanced settings** and paste your API keys into **Secrets** in TOML format:
   ```toml
   OPENAI_API_KEY = "your-key-here"
   TAVILY_API_KEY = "your-key-here"
   ```
5. Click **Deploy**.

To update the live app, commit and push your changes. It redeploys automatically.

## Notes

- A full research run usually takes a minute or two.
- Anyone with access to a deployed app uses your API credits. Keep the app private or add a password if you do not want public use.
- Past reports are stored only in the browser session and disappear on refresh.

## Tech stack

- [Streamlit](https://streamlit.io) for the interface
- [LangChain](https://www.langchain.com) for agents and chains
- Python 3

## License

Add a license of your choice, for example MIT.