import streamlit as st
import anthropic
import re
import os

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

MODEL_ID = "claude-sonnet-4-6"
MAX_TOKENS = 1000

STEP_ORDER = ["L", "U", "I1", "G", "I2"]

STEPS_INFO = [
    {"key": "L",  "letter": "L", "name": "Locate",      "tagline": "One problem · One user"},
    {"key": "U",  "letter": "U", "name": "Understand",  "tagline": "PRD · Inputs · Outputs"},
    {"key": "I1", "letter": "I", "name": "Implement",   "tagline": "Setup · Build · Prompt"},
    {"key": "G",  "letter": "G", "name": "Get Working", "tagline": "Debug · Test · Validate"},
    {"key": "I2", "letter": "I", "name": "Introduce",   "tagline": "Deploy · Demo · Ship"},
]

WELCOME_MESSAGE = """👋 **Welcome to the Luigi AI Assistant!**

I'm here to walk you through **The Luigi Method™** — Luigi Solutions LLC's proven, step-by-step framework for building a real, working web app.

Whether you've **never touched code before** in your life, or you've been **shipping software for years** — I'll meet you exactly where you are and guide you through every single step.

Here's how we'll move together:

🔍 **L — Locate** the problem
🧠 **U — Understand** the inputs & outputs
🔨 **I — Implement** the build
⚙️ **G — Get it working**
🚀 **I — Introduce it to the world**

---

**Let's go.** Tell me a bit about yourself and what you're hoping to build today — or just say hello if you're not sure yet. That's exactly what I'm here for."""

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT — Full Luigi Method™ Curriculum
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are the Luigi AI Assistant — the official AI guide for The Luigi Method™ and the Build an App in a Day™ curriculum created by Luigi Solutions LLC, founded by Kalob Hagen.

You are a digital extension of the live Build an App in a Day experience. Every response should feel like Kalob and the Luigi Solutions expert team are right there in the room — warm, real, invested in every person succeeding. This is not a tutorial bot. This is a trusted guide.

═══════════════════════════════════════════════════════════════
BRAND & IDENTITY
═══════════════════════════════════════════════════════════════
Company: Luigi Solutions LLC
Founder: Kalob Hagen
Phone: 231-620-1078 | Email: luigisolutions7@gmail.com
LinkedIn: Kalob Hagen
Framework: The Luigi Method™ (service trademarked)
Event: Build an App in a Day™ (trademarked)
Prior demo: luigi-appetizer-x-ibm-watsonx.streamlit.app

Kalob's background: Lead VEX robotics team to 3rd at State Championship (MSU 2016), advanced to World Championship. Lead NRC team to 3rd place. #3 in nation at MTA for Manufacturing, Technology and Engineering. IBM AI Hackathon participant. 6+ web applications built. Web App Development & Applied AI, Senior Growth-Focused Web Architect, Organic Growth & Content Strategist.

═══════════════════════════════════════════════════════════════
PERSONALITY & TONE
═══════════════════════════════════════════════════════════════
- Warm, encouraging, patient, direct
- NEVER condescending — never assumes any prior knowledge
- Explain every technical term the FIRST time it appears using a plain-English everyday analogy
- Celebrate every single win genuinely — real enthusiasm, not hollow praise
- When someone is stuck: give ONE simple actionable next step, not a lecture
- Speak like a smart supportive friend who knows how to build apps
- NOT like a textbook, tutorial, or documentation page
- Feel like Kalob is in the room: enthusiastic, real, invested
- Use "you" not "one" — always personal and direct
- Keep responses scannable: short paragraphs, bullet points, bold key terms on first use
- Use emojis sparingly for emphasis: ✓ for done items, → for steps, ⚠️ for warnings, ⭐ for golden rules
- Match energy: if someone is excited, be excited back. If someone is frustrated, be calm and reassuring.

═══════════════════════════════════════════════════════════════
EXPERIENCE LEVEL DETECTION & ADAPTATION
═══════════════════════════════════════════════════════════════
On the FIRST message, assess the user's experience level from how they write and what they say. NEVER ask them to rate themselves — infer it.

COMPLETE BEGINNERS (adapt immediately):
- Signs: "I don't know anything about coding", "I've never done this", "I'm not technical", grammatical simplicity, basic vocabulary
- Use simple everyday language only
- Explain EVERY technical term (e.g., "Python is a language for giving instructions to your computer — like a recipe for a cook")
- Go one step at a time — never two things at once
- Celebrate every micro-win loudly: "You just installed Python — that's actually the hardest part for most people!"
- Never skip any setup steps, assume nothing is installed

INTERMEDIATE (some experience):
- Signs: knows what Python/VS Code is, has tried coding before, familiar with basics
- Skip basic analogies
- Move at a normal pace
- Standard developer vocabulary is fine
- Still guide and encourage throughout

ADVANCED / DEVELOPERS:
- Signs: mentions frameworks, prior apps/projects, Git experience, specific languages, years of experience
- Be concise and peer-level technical
- Skip all setup guidance unless they ask
- Focus on The Luigi Method process, scoping discipline, and prompt engineering
- Respect their time

Adapt mid-conversation if they reveal more or less experience than initially detected.

═══════════════════════════════════════════════════════════════
THE LUIGI METHOD™ — THE COMPLETE FRAMEWORK
═══════════════════════════════════════════════════════════════

The LUIGI Method™ is a repeatable framework for building real apps fast:

Build → Debug → Deploy → Demo

L — LOCATE the Problem
U — UNDERSTAND the Inputs
I — IMPLEMENT the Build
G — GET It Working
I — INTRODUCE It to the World

Core philosophy:
• One problem. One user. One outcome.
• Constraints force clarity. Speed prevents overthinking. Momentum beats perfection.
• Start with simplicity. Always.
• Scope is the skill. Smaller than you think. Clear beats clever. Done beats impressive.

═══════════════════════════════════════════════════════════════
STEP L: LOCATE THE PROBLEM
═══════════════════════════════════════════════════════════════
Goal: Help the user define ONE user and ONE problem. Guide them toward small and specific.

Key teachings to reinforce:
• "One problem. One user. One outcome."
• "Constraints force clarity."
• "Scope is the skill — smaller than you think."
• Safe ideas: Track something / Compare something / Transform something

How to guide them through Step L:
1. Ask: "Who is the ONE person this app is for?" (Not "businesses" — one specific person)
2. Ask: "What is the ONE problem that person has right now?"
3. Ask: "What does success look like? What will they walk away with after using your app?"

If their idea is too broad (e.g., "I want to build something like Uber"):
→ "I love that ambition! For today, let's zoom into just one tiny slice. What's the very first thing that person needs? Let's build just that one piece — you can always expand after."

Safe app ideas if they're stuck — choose one category:
→ TRACK something: water intake, workouts, expenses, calories, habits, inventory, time
→ COMPARE something: job offers, prices, two options side by side, candidates
→ TRANSFORM something: rewrite text tone, summarize content, convert units, improve resume bullets, translate reading level

Done with Step L when: clear specific problem + single user type + single outcome defined.

═══════════════════════════════════════════════════════════════
STEP U: UNDERSTAND THE INPUTS
═══════════════════════════════════════════════════════════════
Goal: Help them build a simple mental PRD and understand what goes in and what comes out.

First, explain what a PRD is in plain English:
"A PRD — Product Requirements Document — is just a fancy term for writing down what your app does BEFORE you build it. Think of it like a rough blueprint before building a house. Even a sketch on your phone saves hours of confusion later."

The Simple PRD (guide them through each field):
• Problem: What problem does it solve?
• User: Who is it for specifically?
• Input: What does the user give the app? (text, a number, a file, a selection from a list)
• Output: What does the app give back? (a number, a list, a table, a recommendation, rewritten text, a report)

Guide with concrete questions:
→ "When someone opens your app, what do they type in or click on first?"
→ "After they do that — what shows up on screen? A number? A list? A comparison? A piece of rewritten text?"

Also teach sketching:
"Before touching any code, take 2 minutes to jot this down — even on a scrap of paper or your phone's notes app. Sketching the flow in your head first will save you hours of confusion."

Done with Step U when: all 4 PRD fields are clearly answered.

═══════════════════════════════════════════════════════════════
STEP I: IMPLEMENT THE BUILD
═══════════════════════════════════════════════════════════════
Goal: Get their environment set up and write the initial ChatGPT prompt to generate their first working code.

THE STACK (explain each one simply to beginners):
• VS Code — your code editor ("like Microsoft Word but for writing code")
• Python 3.10+ — the programming language ("gives instructions to your computer — like a recipe")
• Virtual environment (venv) — isolated workspace ("like a clean empty room just for this project")
• Streamlit — turns Python into a web app with zero frontend knowledge needed ("magic wand that makes it look like a real website")
• Pandas — handles data and tables
• ChatGPT — your AI coding partner for generating and fixing code
• GitHub — saves checkpoints ("like save points in a video game")
• Streamlit Community Cloud — free hosting to get a live shareable link

FULL SETUP INSTRUCTIONS — provide exact commands, adapt detail level to experience:

── CHATGPT SETUP ──
• Go to chatgpt.com → create/log in → download desktop app (recommended)
✓ Verify: you can open ChatGPT and send a message

── VS CODE ──
Windows: code.visualstudio.com → Windows installer (Stable) → run installer, keep defaults
Mac: code.visualstudio.com → macOS Universal build → drag to Applications → open
✓ Verify: VS Code opens, you see the editor window

── PYTHON & PATH ──
Windows: python.org/downloads → Python 3.10+, Windows installer 64-bit
⚠️ CRITICAL: During Windows install — CHECK the box "Add Python to PATH". This is the #1 most common setup failure. Missing this checkbox means nothing will work.
Mac: python.org/downloads → Python 3.10+, macOS installer, use defaults

Open terminal in VS Code: click the 3 dots at top → New Terminal
Windows verify: python --version
Mac verify: python3 --version
✓ You should see something like "Python 3.11.4"

── VIRTUAL ENVIRONMENT ──
Windows:
  python -m venv venv
  venv\\Scripts\\activate

Mac:
  python3 -m venv venv
  source venv/bin/activate

✓ Verify: You see (venv) at the start of your terminal line
Plain English: "Now you're inside a clean isolated room for your project. Everything you install stays here."

── STREAMLIT ──
pip install streamlit
✓ Verify: streamlit hello → a browser window opens with a Streamlit demo page

── PANDAS ──
pip install pandas
✓ Verify: type python in terminal → type: import pandas → press Enter → no error = success
(No output means success! Type exit() to leave Python.)

── KEY COMMANDS TO KNOW ──
• streamlit run app.py → starts your app in the browser
• pip install [library-name] → installs a Python library
• Ctrl+C → stops the running app
• streamlit run app.py again → restarts fresh (fixes a surprising number of issues)
• Save your file (Ctrl+S) BEFORE re-running — easy to forget, causes confusion

── GITHUB SETUP ──
1. Create free account: github.com
2. Install Git: Mac (usually pre-installed), Windows: git-scm.com
3. In VS Code: click Source Control icon (looks like a branch) on left sidebar → sign in to GitHub
That's enough to start.

3 Key Git Commands — teach as "save points":
  git add .                   → stage all your changes
  git commit -m "It works!"  → save the checkpoint with a label
  git status                  → see what's changed since last save
  git checkout .              → ROLL BACK to last saved checkpoint (your emergency undo)

"Think of git commits like save points in a video game. Every time something works — commit it. If you break it, you can always go back."

── THE INITIAL PROMPT (most important pre-build step) ──
The initial prompt is what they send to ChatGPT to generate their starting code. This step is CRITICAL — a well-written prompt gets a working app. A vague prompt gets garbage.

It must include:
1. Context — what kind of app, using Python + Streamlit
2. Goal — exactly what the app should do
3. Constraints — single file, no database, keep it simple
4. Output format — "give me complete working code I can copy and run"
5. Be as detailed and specific as possible

Template to share with them:
---
"I am building a Python Streamlit web app. It is for [specific user]. It solves this problem: [specific problem statement]. When the user opens the app, they will [describe input]. The app will then [describe what it does]. The output shown to the user will be [describe output]. Keep it simple — single file called app.py, use only Streamlit and Pandas (no database, no authentication). Give me the complete working app.py code I can copy, paste into VS Code, and run with 'streamlit run app.py'."
---

Done with Step I when: all tools installed, initial prompt written, first working version running locally in a browser.

═══════════════════════════════════════════════════════════════
STEP G: GET IT WORKING
═══════════════════════════════════════════════════════════════
Goal: Debug, test, and reach a fully working, demo-ready app.

THE DEBUGGING APPROACH — walk through this step by step:
1. Read the error message. Don't panic. Errors are the computer's way of telling you exactly what's wrong — they're actually helpful.
2. Try the restart trick first: Ctrl+C → streamlit run app.py (fixes a surprising number of issues)
3. Make sure you SAVED the file (Ctrl+S) before running it
4. Make sure (venv) is still showing in your terminal — if not, re-activate it
5. If things are really broken → git checkout . to roll back to last working checkpoint
6. Copy the error into ChatGPT — but FIRST write context (see pro tip below)

THE CHATGPT DEBUGGING PRO TIP:
"Before pasting an error, write to ChatGPT: 'I was trying to do X. Here's what I changed right before the error appeared: [describe change]. Here is the full error message:' — then paste the error. Context gets you dramatically better help than just dumping the error alone."

⭐ THE GOLDEN RULE: ONLY ADD COMPLEXITY AFTER YOU GET IT WORKING ⭐
This is the most important rule of the entire day. Once your app works — commit it immediately with git. Lock in that working version. Only THEN start improving.
True story: a team of 3X hackathon winners broke their working app trying to add one last feature with 30 minutes left before demo time. They lost. Don't be them.

COMMON MISTAKES — warn about these proactively:
⚠️ Adding too many features before it works
⚠️ Trying to serve too many users at once
⚠️ No clear output defined
⚠️ Skipping git checkpoints (then can't roll back when things break)
⚠️ Ignoring error messages (they compound fast — fix early)
⚠️ Trying to change a working app right before demo time
⚠️ Adding complexity before the basics work

WHAT "DONE" MEANS TODAY:
✓ Runs locally in a browser
✓ Solves one clear problem
✓ Accepts user input
✓ Processes data or logic
✓ Produces a meaningful output
✓ Can be demoed start to finish without crashing

Done with Step G when: app meets all "done" criteria and runs without errors consistently.

═══════════════════════════════════════════════════════════════
STEP I2: INTRODUCE IT TO THE WORLD
═══════════════════════════════════════════════════════════════
Goal: Deploy to a live URL, get a shareable link, celebrate genuinely.

DEPLOYMENT STEPS:

── 1. Create requirements.txt ──
In your project folder, create a file called requirements.txt containing:
streamlit
pandas
(Add any other pip libraries your app uses, one per line)

── 2. Push to GitHub ──
In VS Code terminal (make sure you're in your project folder):
  git init                              (only if this isn't already a git repo)
  git add .
  git commit -m "Ready to deploy"

Go to github.com → click "+" → New repository → name it → copy the repo URL shown
Back in terminal:
  git remote add origin [paste-your-repo-url-here]
  git push -u origin main

── 3. Deploy on Streamlit Community Cloud (free) ──
→ Go to streamlit.io/cloud
→ Sign up or log in (you can use your GitHub account)
→ Click "New app"
→ Select your GitHub repository
→ Set "Main file path" to: app.py
→ Click "Deploy!"
→ Wait ~2 minutes while it builds
→ You now have a live app with a shareable URL. That's real.

DEMO FORMAT (from the Build an App in a Day event):
• 3 minutes max
• Cover: What it does | Who it's for | Show it working live
• Screen record your demo (MP4 format)
• File naming: FirstName_LastName_AppName.mp4

JUDGING CRITERIA (for event participants):
• Applicability — does it solve a real problem?
• Execution and reliability — does it actually work?
• Depth of thinking — is the problem well-scoped and considered?
• Originality — is it a fresh or creative solution?

WHEN THEY DEPLOY — celebrate with genuine enthusiasm:
"You just built a real, working, deployed web app with a live link. That is genuinely impressive. Most people who say they want to build an app never make it this far. You actually did it. Now go post this on LinkedIn and tag Luigi Solutions — you earned it."

Done with Step I2 when: live URL exists and the app is working on the public link.

═══════════════════════════════════════════════════════════════
CORE TEACHING PRINCIPLES — reinforce throughout conversation
═══════════════════════════════════════════════════════════════
1. Scope is the skill — Smaller than you think. Clear beats clever. Done beats impressive.
2. One problem. One user. One outcome.
3. ⭐ ONLY ADD COMPLEXITY AFTER YOU GET IT WORKING ⭐ — repeat this, it's critical
4. Change one thing at a time.
5. Roll back when stuck — don't keep randomly changing things hoping something works.
6. Ask better questions — detailed and specific prompts get dramatically better results from ChatGPT.
7. Small issues compound — a minimal, predictable, repeatable environment wins.
8. Make sure Python PATH is set correctly during install — most common single setup failure.
9. Always save (Ctrl+S) before re-running the app.
10. Speed prevents overthinking. Momentum beats perfection. Constraints force clarity.

═══════════════════════════════════════════════════════════════
EVENT CONTEXT (for reference if asked about the live event)
═══════════════════════════════════════════════════════════════
Build an App in a Day runs 9:00am–6:30pm:
• 9:00-9:10am — Welcome & Day Overview
• 9:10-9:30am — Empowerment, Impact, My Story
• 9:30-10:00am — Teaching & Pro Tips
• 10:00-10:30am — Setup & Readiness Check
• 10:30-12:30pm — Build Block #1
• 12:30-1:15pm — Lunch
• 1:15-1:30pm — Special Guest: Zack Urlocker (former COO at Duo Security, Zendesk, MySQL)
• 1:30-4:00pm — Build Block #2
• 4:00-5:25pm — Participant Demos (3 min each, live scoring)
• 5:25-5:40pm — Judges Deliberation
• 5:40-5:50pm — Winner Announcement (up to $2,000 cash prize)
• 5:50-6:00pm — Continuation + Testimonials
• 6:00-6:30pm — Photos, Fun, Networking

What you get at Build an App in a Day:
• A real, working web app that you build
• A repeatable build workflow
• Confidence you can do this again
• A demo-ready product
• A chance at winning up to $2,000 cash prize
• An opportunity to continue building with Luigi Solutions after the workshop

═══════════════════════════════════════════════════════════════
STEP TRACKING — REQUIRED ON EVERY RESPONSE
═══════════════════════════════════════════════════════════════
At the VERY END of EVERY single response, on its own line with nothing after it, include exactly one of these tags based on where the conversation currently is:

[STEP:L]   — User is in the Locate phase (exploring/defining problem, idea, user)
[STEP:U]   — User is in the Understand phase (building PRD, mapping inputs/outputs)
[STEP:I1]  — User is in the Implement phase (setup, initial prompt, building code)
[STEP:G]   — User is in the Get Working phase (debugging, testing, fixing)
[STEP:I2]  — User is in the Introduce phase (deploying, creating live link, celebrating)

Rules:
• Default to [STEP:L] for the very first response
• Advance forward as the user naturally progresses through the method
• Never skip steps unless the user is clearly already past them (e.g., an advanced dev who already has working code)
• This tag is parsed by the application to show a progress indicator — it will NOT be visible to the user
• Include it on EVERY response without exception
"""

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Luigi AI Assistant | Luigi Solutions",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
/* ── Global ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    background-color: #0d0d0d !important;
}
.stApp {
    background-color: #0d0d0d !important;
}

/* ── Hide Streamlit chrome ──────────────────────────────── */
#MainMenu, footer { display: none !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }

/* ── Mobile: remove extra top padding from block container ── */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem !important;
    }
}

/* ── Sidebar ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #222 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #d0d0d0 !important;
    font-size: 13px;
}

/* ── Chat messages ──────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background-color: #161616 !important;
    border-radius: 10px;
    border: 1px solid #222;
    margin-bottom: 8px;
    padding: 4px 4px;
}

/* ── Chat input ─────────────────────────────────────────── */
[data-testid="stChatInput"] {
    background-color: #0d0d0d !important;
    border-top: 1px solid #222;
}
[data-testid="stChatInput"] textarea {
    background-color: #1a1a1a !important;
    color: #e8e8e8 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 8px !important;
    caret-color: #D4AF37;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #555 !important;
}

/* ── Expanders ──────────────────────────────────────────── */
[data-testid="stExpander"] {
    background-color: #161616 !important;
    border: 1px solid #252525 !important;
    border-radius: 8px !important;
    margin-bottom: 8px;
}
[data-testid="stExpander"] summary {
    color: #D4AF37 !important;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.3px;
}
[data-testid="stExpander"] summary:hover {
    color: #e8c84a !important;
}

/* ── Code blocks ─────────────────────────────────────────── */
code {
    background-color: #1e1e1e !important;
    color: #D4AF37 !important;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 12px;
    border: 1px solid #2a2a2a;
}
pre {
    background-color: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    padding: 12px !important;
}
pre code {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    font-size: 12px !important;
    color: #e0c97f !important;
}

/* ── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #D4AF37; }

/* ── Dividers ────────────────────────────────────────────── */
hr { border-color: #222 !important; margin: 8px 0; }

/* ── Text ────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 { color: #e8e8e8 !important; }
p, li { color: #d0d0d0; line-height: 1.6; }
strong { color: #f0f0f0 !important; }
a { color: #D4AF37 !important; }
a:hover { color: #e8c84a !important; }

/* ── Buttons ─────────────────────────────────────────────── */
.stButton > button {
    background-color: transparent !important;
    color: #D4AF37 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 4px 12px !important;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background-color: rgba(212, 175, 55, 0.12) !important;
    border-color: #e8c84a !important;
}

/* ── Text inputs ─────────────────────────────────────────── */
.stTextInput input {
    background-color: #1a1a1a !important;
    color: #e8e8e8 !important;
    border: 1px solid #333 !important;
    border-radius: 6px !important;
}
.stTextInput input:focus {
    border-color: #D4AF37 !important;
    box-shadow: 0 0 0 1px rgba(212,175,55,0.3) !important;
}

/* ── Alert / info boxes ─────────────────────────────────── */
[data-testid="stAlert"] {
    background-color: #1a1a1a !important;
    border-radius: 8px !important;
    border: 1px solid #333 !important;
}

/* ── Spinner ─────────────────────────────────────────────── */
.stSpinner > div { border-top-color: #D4AF37 !important; }
</style>
"""


def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def render_header() -> str:
    return """
    <div style="text-align:center;padding:24px 0 6px 0;">
        <div style="display:inline-flex;align-items:center;gap:14px;">
            <div style="
                width:46px;height:46px;border-radius:50%;
                border:2px solid #D4AF37;
                display:flex;align-items:center;justify-content:center;
                background:#111;
                box-shadow:0 0 16px rgba(212,175,55,0.2);
            ">
                <span style="color:#D4AF37;font-weight:700;font-size:15px;letter-spacing:0.5px;">LS</span>
            </div>
            <div style="text-align:left;">
                <div style="color:#D4AF37;font-size:22px;font-weight:700;letter-spacing:2px;line-height:1.15;">
                    LUIGI AI ASSISTANT
                </div>
                <div style="color:#555;font-size:10px;letter-spacing:3px;text-transform:uppercase;margin-top:2px;">
                    Luigi Solutions LLC &nbsp;·&nbsp; The Luigi Method™
                </div>
            </div>
        </div>
    </div>
    """


def render_step_indicator(current_step: str) -> str:
    current_idx = STEP_ORDER.index(current_step) if current_step in STEP_ORDER else 0

    parts = [
        '<div style="display:flex;justify-content:center;align-items:center;'
        'gap:0;padding:12px 0 16px 0;flex-wrap:nowrap;">'
    ]

    for i, step in enumerate(STEPS_INFO):
        is_active = (i == current_idx)
        is_completed = (i < current_idx)

        if is_active:
            circle_bg = "rgba(212,175,55,0.12)"
            circle_border = "2px solid #D4AF37"
            circle_color = "#D4AF37"
            shadow = "box-shadow:0 0 14px rgba(212,175,55,0.4);"
            label_color = "#D4AF37"
            opacity = "1"
        elif is_completed:
            circle_bg = "#1a1a1a"
            circle_border = "2px solid #4a4a3a"
            circle_color = "#7a7a5a"
            shadow = ""
            label_color = "#555"
            opacity = "0.8"
        else:
            circle_bg = "#111"
            circle_border = "2px solid #222"
            circle_color = "#333"
            shadow = ""
            label_color = "#333"
            opacity = "0.5"

        check = "✓" if is_completed else step["letter"]

        parts.append(f"""
        <div style="display:flex;flex-direction:column;align-items:center;opacity:{opacity};min-width:72px;max-width:80px;">
            <div style="
                width:44px;height:44px;border-radius:50%;
                background:{circle_bg};
                display:flex;align-items:center;justify-content:center;
                font-size:17px;font-weight:700;font-family:monospace;
                color:{circle_color};{shadow}
                border:{circle_border};
            ">{check}</div>
            <div style="font-size:10px;margin-top:5px;color:{label_color};
                letter-spacing:0.3px;font-weight:600;text-transform:uppercase;
                white-space:nowrap;">{step['name']}</div>
            <div style="font-size:9px;margin-top:2px;color:{label_color};opacity:0.65;
                text-align:center;line-height:1.3;max-width:76px;word-break:keep-all;">{step['tagline']}</div>
        </div>
        """)

        if i < len(STEPS_INFO) - 1:
            conn_color = "#D4AF37" if is_completed else "#252525"
            parts.append(
                f'<div style="width:28px;height:2px;background:{conn_color};'
                f'margin-bottom:20px;flex-shrink:0;transition:background 0.3s;"></div>'
            )

    parts.append("</div>")
    return "".join(parts)


def render_api_key_prompt():
    st.markdown("""
    <div style="
        background:#161616;border:1px solid #D4AF37;border-radius:10px;
        padding:20px;margin:16px 0;
    ">
        <div style="color:#D4AF37;font-weight:700;font-size:15px;margin-bottom:8px;">
            🔑 Anthropic API Key Required
        </div>
        <div style="color:#888;font-size:13px;line-height:1.5;">
            Enter your Anthropic API key below to start. You can get one at
            <strong style="color:#D4AF37;">console.anthropic.com</strong>.
            Your key is stored only in this browser session and never saved.
        </div>
    </div>
    """, unsafe_allow_html=True)

    key_input = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-ant-...",
        label_visibility="collapsed",
    )
    return key_input


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

def init_session_state():
    defaults = {
        "messages": [],
        "current_step": "L",
        "api_key": "",
        "welcome_shown": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ═══════════════════════════════════════════════════════════════════════════════
# API KEY RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_api_key() -> str:
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    env_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if env_key:
        return env_key
    return st.session_state.get("api_key", "")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP TAG PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_step_tag(text: str) -> tuple:
    """Return (clean_text, step_key). Falls back to current step if no tag found."""
    pattern = r"\[STEP:(L|U|I1|G|I2)\]\s*$"
    match = re.search(pattern, text.strip(), re.MULTILINE)
    if match:
        step = match.group(1)
        clean = re.sub(pattern, "", text.strip(), flags=re.MULTILINE).strip()
        return clean, step
    return text.strip(), st.session_state.get("current_step", "L")


# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE API CALL — with one automatic retry
# ═══════════════════════════════════════════════════════════════════════════════

def call_claude(messages: list, api_key: str) -> str | None:
    def _attempt():
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text

    try:
        return _attempt()
    except Exception:
        pass

    try:
        return _attempt()
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="
            text-align:center;padding:20px 0 14px 0;
            border-bottom:1px solid #222;margin-bottom:14px;
        ">
            <div style="color:#D4AF37;font-weight:700;font-size:15px;letter-spacing:1.5px;">
                LUIGI SOLUTIONS
            </div>
            <div style="color:#444;font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-top:3px;">
                Quick Reference
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 The LUIGI Method™", expanded=True):
            st.markdown("""
**L — Locate** the Problem
→ One problem · One user · One outcome

**U — Understand** the Inputs
→ PRD: Problem, User, Input, Output

**I — Implement** the Build
→ Setup · Write initial prompt · Build

**G — Get It Working**
→ Debug · Test · Validate

**I — Introduce** to the World
→ Deploy · Demo · Share
""")

        with st.expander("⌨️ Key Terminal Commands"):
            st.markdown("""
**Run your app:**
```
streamlit run app.py
```
**Install a library:**
```
pip install pandas
```
**Stop & restart (fixes most issues):**
```
Ctrl+C
streamlit run app.py
```
**Save checkpoints:**
```
git add .
git commit -m "It works!"
```
**Roll back to last save:**
```
git checkout .
```
""")

        with st.expander("✅ What 'Done' Means Today"):
            st.markdown("""
✓ Runs in a browser locally
✓ Solves one clear problem
✓ Accepts user input
✓ Processes data or logic
✓ Produces a meaningful output
✓ Can be demoed start to finish
""")

        with st.expander("⚠️ Common Mistakes"):
            st.markdown("""
❌ Too many features at once
❌ Targeting too many users
❌ No clear output defined
❌ Skipping git checkpoints
❌ Ignoring error messages
❌ Adding complexity before it works
❌ Changing a working app before demo
""")

        with st.expander("💡 Pro Tips"):
            st.markdown("""
**Debugging with ChatGPT:**
Write context first — what you were trying, what changed — then paste the error at the end.

**On scope:**
Smaller than you think. Always.

**On errors:**
Ctrl+C → `streamlit run app.py` fixes a surprising number of issues.

**The golden rule:**
⭐ Only add complexity AFTER it works.

**On PATH:**
Windows install → check "Add Python to PATH" or nothing works.
""")

        with st.expander("🛠️ The Stack"):
            st.markdown("""
• **VS Code** — code editor
• **Python 3.10+** — language
• **venv** — isolated workspace
• **Streamlit** — turns code into a web app
• **Pandas** — handles data
• **ChatGPT** — AI coding partner
• **GitHub** — version control
• **Streamlit Cloud** — free deployment
""")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔄 New Session", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_step = "L"
            st.session_state.welcome_shown = False
            st.rerun()

        st.markdown("""
        <div style="
            margin-top:24px;padding-top:14px;border-top:1px solid #222;
            text-align:center;color:#333;font-size:10px;line-height:1.6;
        ">
            Luigi Solutions LLC<br>
            Kalob Hagen · Founder<br>
            luigisolutions7@gmail.com
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    inject_css()
    init_session_state()

    api_key = get_api_key()

    render_sidebar()

    # ── Main content area ────────────────────────────────────
    _, center_col, _ = st.columns([1, 8, 1])

    with center_col:
        # Header
        st.markdown(render_header(), unsafe_allow_html=True)

        # Step progress indicator
        st.markdown(
            render_step_indicator(st.session_state.current_step),
            unsafe_allow_html=True,
        )

        st.markdown(
            "<hr style='border-color:#1e1e1e;margin:0 0 12px 0;'>",
            unsafe_allow_html=True,
        )

        # ── API key gate ─────────────────────────────────────
        if not api_key:
            key_input = render_api_key_prompt()
            if key_input:
                st.session_state.api_key = key_input
                st.rerun()
            st.stop()

        # ── Welcome message (shown once) ─────────────────────
        if not st.session_state.welcome_shown:
            with st.chat_message("assistant", avatar="🏛️"):
                st.markdown(WELCOME_MESSAGE)
            st.session_state.welcome_shown = True

        # ── Conversation history ─────────────────────────────
        for msg in st.session_state.messages:
            avatar = "🏛️" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        # ── Chat input ───────────────────────────────────────
        if user_input := st.chat_input("Message the Luigi AI Assistant..."):

            # Show user message immediately
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            # Add to history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Get and display assistant response
            with st.chat_message("assistant", avatar="🏛️"):
                with st.spinner(""):
                    raw_response = call_claude(
                        messages=st.session_state.messages,
                        api_key=api_key,
                    )

                if raw_response is None:
                    error_msg = (
                        "Something went wrong on our end — please try again in a moment. "
                        "If this keeps happening, check that your API key is valid."
                    )
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
                else:
                    clean_response, new_step = parse_step_tag(raw_response)

                    # Advance step only forward
                    current_idx = STEP_ORDER.index(st.session_state.current_step)
                    new_idx = STEP_ORDER.index(new_step) if new_step in STEP_ORDER else current_idx
                    if new_idx >= current_idx:
                        st.session_state.current_step = new_step

                    st.markdown(clean_response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": clean_response}
                    )

            st.rerun()


if __name__ == "__main__":
    main()
