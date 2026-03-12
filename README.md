# 🦌 Truth Field Detector
### AI-Powered Narrative Risk Analyzer | Built with Amazon Nova

**Live Demo:** https://truth-field-detector.onrender.com

---

## ⚠️ Copyright Notice

© 2026 Eloisa Flores. All rights reserved.

This project and all its contents — including but not limited to source code, design, logic, and assets — are the exclusive intellectual property of Eloisa Flores. This repository is shared publicly for evaluation purposes only, including the Amazon Nova Hackathon. Copying, cloning, redistributing, or using any part of this project without explicit written permission from the author is strictly prohibited. Submission to the Amazon Nova Hackathon grants Amazon and Devpost a non-exclusive license to evaluate and promote this project as described in the official hackathon rules — all other rights are reserved by the author.

---

## What It Does

Truth Field Detector helps you spot manipulative content in real time. Paste any news article, headline, or text — and our AI instantly tells you if it's **HIGH**, **MEDIUM**, or **LOW** risk, and explains why.

It detects:
- 😱 **Emotional language** designed to trigger reactions
- ⚠️ **Absolutist claims** with no nuance
- 🤓 **Missing citations** and unverifiable sources

And then it **reads the results out loud** — so you get the information fast, hands-free.

---

## How It Works

```
User pastes text or URL
        ↓
Amazon Nova 2 Lite analyzes narrative risk
        ↓
Returns Risk Score (0–100) + detailed breakdown
        ↓
Amazon Polly reads results aloud instantly
        ↓
User sees + hears: HIGH / MEDIUM / LOW risk
```

---

## Amazon Nova Integration

| Service | Role |
|---|---|
| **Amazon Nova 2 Lite** | Real-time narrative risk analysis via Amazon Bedrock |
| **Amazon Polly** | Natural voice feedback of results |

### Why Nova 2 Lite?

Nova 2 Lite was chosen for its **low latency** — users get results in seconds, not minutes. The model receives the text, returns a structured JSON with risk level, score, emotional language detected, absolutist claims, and missing citations — all in one call.

---

## Features

- 🌐 **Multilingual** — paste text in any language, get results in English
- 🔗 **URL support** — paste a news link directly
- 🔊 **Voice feedback** — results are read aloud automatically
- 📊 **Risk Score 0–100** with HIGH / MEDIUM / LOW classification
- 🎨 **Professional dark UI** with deer detective mascot
- ⚡ **Real-time** — analysis in under 3 seconds

---

## Tech Stack

- **Backend:** Python + Flask
- **AI:** Amazon Nova 2 Lite via Amazon Bedrock (boto3)
- **Voice:** Amazon Polly (neural engine)
- **Hosting:** Render (auto-deploy from GitHub)
- **Frontend:** Vanilla HTML/CSS/JavaScript

---

## Use Cases

- **Journalists** fact-checking sources before publishing
- **Educators** teaching media literacy
- **Citizens** navigating social media and news
- **Organizations** monitoring narrative risks in communications

---

## 🔧 Technical Challenges & Solutions

Building Truth Field Detector involved solving several real engineering challenges:

**Git repository not found in expected path**
Git Bash couldn't locate the project folder in the expected location. Located it at `~/truth-field-detector` and resolved path conflicts between Git Bash and Windows file system.

**GitHub authentication failure**
Push authentication failed due to an expired token. Generated a new Personal Access Token (classic) and updated the remote URL with the new credentials.

**Branch mismatch between local and remote**
The local project was on `master` while GitHub expected `main`. Resolved by pushing explicitly with `git push origin master:main` to sync both branches.

**Nova Sonic incompatible with standard API calls**
Amazon Nova 2 Sonic requires bidirectional WebSocket streaming, which is not supported in our Flask architecture. Switched to Amazon Polly (neural engine) for voice output — fully AWS-native, production-ready, and delivering natural-sounding voice feedback.

**MSN and paywalled URLs returning no content**
Some news sites block web scraping. Solved by detecting failed URL fetches and prompting the user to paste the text directly — maintaining a smooth user experience.

**Render deploying outdated version**
Render was serving a cached older version after code updates. Fixed by adjusting the branch setting in the Render dashboard and triggering a fresh manual deploy.

---

## Built For

🏆 [Amazon Nova Hackathon](https://amazon-nova.devpost.com) — March 2026

**Category:** Multimodal Understanding

---

*Created by Eloisa Flores — because in a world full of noise, you deserve clarity.* 🦌
