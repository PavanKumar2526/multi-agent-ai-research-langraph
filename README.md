# 🔬 Multi-Agent AI Research System

A **4-agent autonomous research pipeline** that takes any topic and produces a structured, peer-reviewed research report — fully automated using LangChain, Mistral AI, and Tavily Search.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
  - [Step 1 — Search Agent](#step-1--search-agent)
  - [Step 2 — Reader Agent](#step-2--reader-agent)
  - [Step 3 — Writer Chain](#step-3--writer-chain)
  - [Step 4 — Critic Chain](#step-4--critic-chain)
- [Architecture Diagram](#architecture-diagram)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Design Decisions](#design-decisions)

---

## Overview

Traditional LLMs answer from their training data alone — they can't research new topics in real time or self-evaluate their own output. This project solves that by implementing a **Multi-Agent Pipeline**: four specialised agents collaborate in sequence to search the web, scrape top sources, draft a professional report, and then critically review it — all autonomously.

---

## How It Works

### Step 1 — Search Agent

A LangChain agent equipped with the **Tavily web search tool** receives the user's topic and fetches the top 5 most recent, reliable results from the web. It returns titles, URLs, and content snippets that form the foundation of the research.

### Step 2 — Reader Agent

A second agent equipped with a **URL scraper tool** picks the most relevant URL from the search results, visits it, and extracts clean, readable text content. It strips away navigation, ads, scripts, and boilerplate — leaving only the core article content for deeper analysis.

### Step 3 — Writer Chain

A structured **LangChain prompt chain** combines the search results and scraped content into a single research context, then instructs the Mistral LLM to write a detailed, professional report. The report follows a fixed structure: Introduction, Key Findings, Conclusion, and Sources.

### Step 4 — Critic Chain

A separate **critic prompt chain** sends the generated report to the same LLM with a strict review persona. The critic scores the report out of 10, lists strengths, identifies areas for improvement, and delivers a one-line verdict — all in a structured format.

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      RESEARCH PIPELINE                       │
│                                                              │
│  User Topic                                                  │
│      │                                                       │
│      ▼                                                       │
│  ┌─────────────┐     Tavily Search API                       │
│  │ Search Agent│ ──────────────────────► Web Results         │
│  └─────────────┘                             │               │
│                                              ▼               │
│  ┌─────────────┐     URL Scraper Tool                        │
│  │ Reader Agent│ ──────────────────────► Scraped Content     │
│  └─────────────┘                             │               │
│                                              ▼               │
│  ┌──────────────┐   Search + Scraped Data                    │
│  │ Writer Chain │ ──────────────────────► Research Report    │
│  └──────────────┘                            │               │
│                                              ▼               │
│  ┌──────────────┐   Report as Input                          │
│  │ Critic Chain │ ──────────────────────► Score + Feedback   │
│  └──────────────┘                                            │
└──────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
multi-agents-project
├── agents.py
├── pipeline.py
├── tools.py
├── app.py
├── requirement.txt
├── .env
└── .venv/
```

| File | Purpose |
|---|---|
| `agents.py` | Defines the Search Agent, Reader Agent, Writer Chain, and Critic Chain |
| `pipeline.py` | Orchestrates all four agents in sequence; can also be run directly from terminal |
| `tools.py` | LangChain tools — `web_search` (Tavily) and `scrape_url` (BeautifulSoup) |
| `app.py` | Streamlit UI — sidebar config, pipeline trigger, and tabbed results display |
| `requirement.txt` | All Python dependencies |
| `.env` | API keys (never commit this file) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Agent Framework | LangChain + LangGraph |
| LLM | Mistral AI (`ministral-3b-2512`) |
| Web Search | Tavily Search API |
| Web Scraping | Requests + BeautifulSoup4 |
| Prompt Management | LangChain `ChatPromptTemplate` |
| Output Parsing | LangChain `StrOutputParser` |
| Environment Config | `python-dotenv` |

---

## Setup & Installation

**1. Clone the repository and navigate to the project folder.**

**2. Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

**3. Install all dependencies:**

```bash
pip install -r requirement.txt
```

**4. Configure your API keys** (see section below).

**5. Run the Streamlit app:**

```bash
streamlit run app.py
```

Or run the pipeline directly from the terminal:

```bash
python pipeline.py
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> **Note:** Never commit your `.env` file to version control. Add it to `.gitignore`.

Get your keys here:
- Mistral AI → [console.mistral.ai](https://console.mistral.ai)
- Tavily → [app.tavily.com](https://app.tavily.com)

---

## Usage

**Via Streamlit UI:**
1. Launch the app with `streamlit run app.py`
2. Enter your API keys in the sidebar
3. Select your LLM provider and model
4. Type a research topic in the input area
5. Click **Run Research Pipeline**
6. View results across four tabs: Search, Reader, Report, Critique
7. Download the final report as a `.md` file

**Via Terminal:**
```bash
python pipeline.py
# Enter a research topic when prompted
```

---

## Design Decisions

**Why four separate agents instead of one?**
Each agent has a single, well-defined responsibility. This separation of concerns makes the pipeline easier to debug, extend, and swap components in — for example, replacing the search tool or upgrading the writer model independently.

**Why Tavily instead of a raw Google/Bing search?**
Tavily is purpose-built for LLM agents — it returns clean, structured, LLM-ready snippets without rate-limit headaches or HTML parsing. It also surfaces recent content, which matters for research quality.

**Why scrape a full URL after searching?**
Search result snippets are truncated to ~300 characters. The Reader Agent goes deeper by fetching and cleaning the full article, giving the Writer Chain significantly richer source material to work from.

**Why a separate Critic Chain?**
Self-evaluation improves output quality and surfaces weaknesses that would otherwise go unnoticed. The structured critic format (score, strengths, improvements, verdict) makes feedback actionable and easy to render in the UI.
