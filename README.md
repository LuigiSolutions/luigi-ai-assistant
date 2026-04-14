# Luigi AI Assistant

An AI-powered conversational guide for **The LUIGI Method™** — Luigi Solutions LLC's proven framework for building a real, working web app in a day.

Built with Python, Streamlit, and the Anthropic Claude API.

---

## What It Does

The Luigi AI Assistant walks users through every step of the **Build an App in a Day™** curriculum — the same material taught at Luigi Solutions LLC live events — so anyone can access expert guidance 24/7, on their own schedule.

The assistant:
- Detects your experience level automatically (beginner → advanced) and adapts its language and pacing
- Guides you through all five LUIGI steps with a live visual progress indicator
- Maintains full conversation memory throughout the session
- Provides a collapsible sidebar with quick-reference materials for each step

---

## The LUIGI Method™

| Step | Name | Focus |
|------|------|-------|
| **L** | Locate | One problem · One user · One outcome |
| **U** | Understand | PRD · Inputs · Outputs |
| **I** | Implement | Setup · Build · Prompt |
| **G** | Get Working | Debug · Test · Validate |
| **I** | Introduce | Deploy · Demo · Ship |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | [Streamlit](https://streamlit.io) |
| AI Model | Anthropic Claude (`claude-sonnet-4-6`) |
| Language | Python 3.9+ |
| API Client | `anthropic` Python SDK |
| Config | Streamlit secrets / environment variables |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/LuigiSolutions/luigi-ai-assistant.git
cd luigi-ai-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Anthropic API key

Create the secrets file:

```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml` with the following content:

```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

Get an API key at [console.anthropic.com](https://console.anthropic.com).

> **Note:** `.streamlit/secrets.toml` is gitignored and will never be committed. Keep your key safe.

Alternatively, you can set the environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"  # Mac/Linux
set ANTHROPIC_API_KEY=your-api-key-here        # Windows
```

Or enter it directly in the app's UI when prompted.

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Project Structure

```
luigi-ai-assistant/
├── app.py               # Full application — single file
├── requirements.txt     # Python dependencies
├── .gitignore           # Protects secrets from being committed
└── .streamlit/
    └── secrets.toml     # API key (local only, not in repo)
```

---

## Features

- **Experience level detection** — The assistant infers your background from how you write and adapts instantly. No self-assessment forms.
- **LUIGI step progress indicator** — Visual tracker shows which step you're on with name and tagline. Updates as Claude guides you forward.
- **Full conversation memory** — The entire conversation history is passed to Claude on every turn so it never loses context.
- **Collapsible sidebar** — Quick reference for each LUIGI step: goals, done criteria, common mistakes, pro tips, and tech stack.
- **Automatic retry** — One automatic retry on API failure before showing a user-friendly error message.
- **Flexible API key input** — Resolves from Streamlit secrets → environment variable → in-app text input.

---

## About Luigi Solutions LLC

**Luigi Solutions LLC** is founded by Kalob Hagen — web app developer, AI integrations specialist, and creator of The LUIGI Method™ and Build an App in a Day™.

- Email: luigisolutions7@gmail.com
- Phone: 231-620-1078
- LinkedIn: [Kalob Hagen](https://linkedin.com/in/kalob-hagen)

---

## License

Proprietary. The LUIGI Method™ and Build an App in a Day™ are trademarked by Luigi Solutions LLC. All rights reserved.
