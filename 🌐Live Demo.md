# 🚀 Getting Started & Troubleshooting

## 🌐 Live Demo

Try the app instantly — no installation needed:

> **🔗 [https://multi-agent-ai-research-langraph-awgycgztbpdsyqmaq4sjap.streamlit.app/](https://multi-agent-ai-research-langraph-awgycgztbpdsyqmaq4sjap.streamlit.app/)**

---

## ⚠️ Seeing a Red Error Screen?

<![Project Reference Image](Reference%20image.png)>

> If you open the app and see **red error text** like the screenshot below — **don't panic, the app is working fine.**

### ✅ What's actually happening

The red screen is **not a bug or a crash.** It simply means no API key has been entered yet. Our main agenda is to try it for free, so our first priority is Mistral AI. That’s why we have made it available with free models, The app requires at least a **Mistral API key** and a **Tavily API key** to run the pipeline.

Just add your keys in the sidebar and the error disappears instantly.

---

## 🔑 Supported Providers

| Provider | Status | Cost |
|---|---|---|
| **Mistral AI** | ✅ Fully supported | 🆓 Free tier available |
| **Tavily Search** | ✅ Required for search | 🆓 Free tier available |
| OpenAI | 🔜 Can be added later | Paid |
| Gemini | 🔜 Can be added later | Paid |
| Llama | 🔜 Can be added later | Varies |

> 💡 **Tip:** Want to test the app for free? Use **Mistral + Tavily** — both offer free API keys with no credit card required.

Currently, this project supports **Mistral AI** as the LLM provider and **Tavily** as the search provider. Other models like OpenAI, Gemini, or Llama can be added later by creating a provider selection layer in `agents.py`.

---

## 🗝️ How to Get Your Free API Keys

### 1. Mistral AI API Key (Free)

1. Go to **[console.mistral.ai](https://console.mistral.ai)**
2. Click **Sign Up** and create a free account
3. Once logged in, navigate to **API Keys** from the left sidebar
4. Click **Create new key**
5. Copy the key — it starts with a random string (e.g. `xxxxxxxxxxxxxxxxxxxxxxxx`)
6. Paste it into the **Mistral API Key** field in the app sidebar

> ⚡ The free tier includes generous usage limits — more than enough for testing and exploring the pipeline.

---

### 2. Tavily API Key (Free)

1. Go to **[app.tavily.com](https://app.tavily.com)**
2. Click **Sign Up** and create a free account
3. After logging in, your API key is shown directly on the **dashboard**
4. Copy the key — it starts with `tvly-`
5. Paste it into the **Tavily API Key** field in the app sidebar

> ⚡ Tavily's free plan includes 1,000 searches/month — plenty for research and testing.

---

## 🖥️ Running the App (Step-by-Step)

Once you have both keys:

1. Open the live app → **[click here](https://multi-agent-ai-research-langraph-awgycgztbpdsyqmaq4sjap.streamlit.app/)**
2. In the **left sidebar**, enter your:
   - `Mistral API Key`
   - `Tavily API Key`
3. Set **LLM Provider** to `Mistral`
4. Choose a model (e.g. `mistral-large-latest`)
5. Type your **research topic** in the main input box
6. Click **🚀 Run Research Pipeline**
7. Watch the 4 agents work — results appear across tabs:
   - 🔍 **Search** — raw web results
   - 📄 **Reader** — scraped article content
   - 📝 **Report** — full written research report
   - 🧐 **Critique** — score, strengths, and feedback
8. Download the final report as a `.md` file

---

## 🔮 Future Provider Support

The pipeline is designed to be extensible. The following providers can be plugged in by adding a model selection layer in `agents.py`:

- **OpenAI** — GPT-4o, GPT-4.1, GPT-3.5-turbo
- **Google Gemini** — gemini-1.5-flash, gemini-pro
- **Llama** — via Ollama or Groq

Pull requests are welcome! 🙌
