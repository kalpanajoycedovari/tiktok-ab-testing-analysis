# 🎭 Mime & Meme — AI Meme Consultant Agent

> *An n8n AI agent that tells you exactly which trending memes to put in your video and where. Built out of frustration, spite, and a broke girl's ingenuity.*

---

## 🤔 The Problem

I make videos. I know what I want. I have a full cinematic vision in my head.

And then I open a video editor and my brain just... leaves. ✌️

So I thought — what if an AI could at least tell me *which memes are trending* and *exactly where to slap them* in my video? That way I just have to execute, not think.

Turns out building that is its own adventure. Buckle up.

---

## 💀 The Journey (aka everything that went wrong)

### Act 1: Flowise (a tragedy in 3 acts)
Started with Flowise. Seemed simple. Was not simple.

- `npm install -g flowise` ✅
- `npx flowise start` ❌ *Cannot find module 'turndown'*
- Install turndown ✅
- `npx flowise start` ❌ *Cannot find module 'winston-daily-rotate-file'*
- Install that ✅
- `npx flowise start` ❌ *Cannot find module 'multer-s3'*

At some point I was just manually installing the entire internet one package at a time. We don't talk about Flowise anymore.

### Act 2: The Node.js Problem
Turns out I had Node.js v24 installed. Flowise wanted v20. They did not get along.

Had to install `nvm-windows`, switch Node versions, and start over. Classic.

### Act 3: n8n enters the chat 🦸
Switched to n8n. `npm install -g n8n` actually worked. `n8n start` actually worked. I nearly cried.

### Act 4: The API Key Incident 🔑
Set up Google Gemini as the AI brain. Free tier. No budget. Perfect.

Accidentally pasted my API key in a public chat. 

Someone (or something) used my entire free quota in approximately 4 seconds.

Quota: **0**. Daily limit: **0**. Me: 💀

### Act 5: Groq saves the day
Switched to Groq (free, fast, no drama). Used `llama-3.3-70b-versatile`.

First model I tried was decommissioned. Second one worked.

**Workflow executed successfully.** 🎉

---

## 🛠️ What It Actually Does

You describe your video → the agent searches for trending memes → it tells you exactly where to put them.

**Example input:**
> "I'm making a 60-second morning routine video for Instagram Reels, audience is Gen Z"

**Example output:**
> 1. *"I'm not a morning person" meme* — insert at 0:05 when you hit snooze, use as reaction overlay
> 2. *"Coffee is my love language"* — insert at 0:30 when brewing coffee, use as text overlay
> 3. *"Adulting is hard"* — insert at 0:45 when getting ready, use as cutaway

Timestamp. Placement. Reason. All of it. You just have to execute.

---

## 🧱 Tech Stack

| Tool | Role | Cost |
|------|------|------|
| [n8n](https://n8n.io) | Workflow automation & agent orchestration | Free (self-hosted) |
| [Groq](https://console.groq.com) | LLM — LLaMA 3.3 70B Versatile | Free |
| [SerpAPI](https://serpapi.com) | Real-time Google search for trending memes | Free tier |
| n8n Simple Memory | Conversational memory across the chat | Built-in |

---

## 🚀 How to Run It

### Prerequisites
- Node.js v20 (use [nvm-windows](https://github.com/coreybutler/nvm-windows) if you have v24 like me 😭)
- A [Groq API key](https://console.groq.com) (free)
- A [SerpAPI key](https://serpapi.com) (free tier)

### Setup

```bash
# Install n8n
npm install -g n8n

# Start n8n
n8n start
```

Open `http://localhost:5678` in your browser.

### Import the workflow

1. Go to your n8n dashboard
2. Click the **+** → **Import from file**
3. Upload `Mime and Meme.json`
4. Add your Groq and SerpAPI credentials
5. Hit **Open chat** and describe your video!

---

## 💬 Example Prompts to Try

- *"I'm making a 30-second gym motivation video for TikTok, targeting college students"*
- *"YouTube video about studying at 2am, 10 minutes long, my audience loves dark humour"*
- *"Instagram Reel of my London cafe hopping day, very aesthetic and cozy vibes"*

---

## 🗺️ What's Next (v2 plans)

- [ ] Multi-agent setup: Trend Researcher → Edit Planner → Caption Writer
- [ ] YouTube trending sounds integration
- [ ] Reddit meme scraper for niche communities
- [ ] Clean formatted output (instead of a wall of text)

---

## 🧠 What I Learned

- n8n is genuinely powerful and the free self-hosted version has no limits
- Always revoke API keys you accidentally paste anywhere (ask me how I know)
- Node version conflicts will humble you
- Groq is underrated and fast
- Building something that solves *your own* problem hits different

---

*Built by [Kalpana Joyce Dovari](https://github.com/kalpanajoycedovari) — MSc AI student, chronic video procrastinator, now slightly less so.*
