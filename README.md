---
title: OpenEnv Fact Checker
emoji: 🕵️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
tags:
  - openenv
---

# 🕵️ Active Investigation — Fake News Fact-Checker

> **OpenEnv AI Agent Hackathon — Round 1 Submission**

An RL environment where an AI agent uses `search` and `read` tools to investigate claims before submitting a final verdict (`true`, `false`, or `unverified`). Features 15 diverse adversarial scenarios with disinformation traps, source credibility tracking, and a rich observation space.

---

## Project Structure

```
openenv-hackathon/
├── environment.py      # Core RL environment (Pydantic schemas, mock internet, grader)
├── database.py         # 15 diverse scenarios (5 Easy, 5 Medium, 5 Hard) — randomly sampled each episode
├── inference.py        # Frontier agent (Qwen-72B via HuggingFace Serverless API)
├── baseline.py         # Baseline agent (Qwen-7B, same prompt — weaker model for comparison)
├── openenv.yaml        # OpenEnv task declaration (Easy, Medium, Hard)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container for reproducible runs
└── README.md           # This file
```

---

## Environment Description

The agent is presented with a **news claim** and given access to a **mock internet** (simulated search engine + article reader). It must investigate before submitting a verdict. Each episode:

- Randomly samples one of 15 unique scenarios so the agent cannot memorize answers
- Provides structured observations including discovered URLs, read history, and per-domain credibility ratings
- Penalizes lazy behavior (no investigation = no dense rewards)

**Real-world parallel:** This mirrors what human fact-checkers and journalists do every day — find sources, evaluate credibility, cross-reference, then conclude.

---

## Action Space

| Action | Parameters | Description |
|--------|-----------|-------------|
| `search` | `query: str` | Search the mock internet using keyword queries |
| `read` | `url: str` | Read a discovered article URL |
| `submit` | `verdict: "true"\|"false"\|"unverified"` | Submit final verdict and end the episode |

---

## Observation Space

```python
class Observation(BaseModel):
    claim: str                          # The claim to investigate
    last_result: str                    # Result of the last action
    step_count: int                     # Steps taken so far
    steps_remaining: int                # Budget remaining (MAX_STEPS=15)
    discovered_urls: list[str]          # URLs found via search (structured state)
    read_urls: list[str]                # URLs already read (anti-repetition)
    credibility_scores: dict[str, str]  # Domain credibility ratings (High/Medium/Low)
    available_actions: list[str]        # Valid actions at this state
```

---

## Tasks & Baseline Scores

| Task | Difficulty | Trap Type | Ground Truth | Baseline Score | Frontier Score |
|------|-----------|-----------|-------------|---------------|---------------|
| `task_easy` | 🟢 Easy | Popular myth, all sources clearly agree | varies | ~0.70 | ~0.97 |
| `task_medium` | 🟡 Medium | True claim buried under loud debunking blogs | varies | ~0.00 | ~0.96 |
| `task_hard` | 🔴 Hard | Misquoted study stats + 404 cache trap | varies | ~0.10 | ~0.96 |

**Why Medium is hard:** The agent must weigh source credibility — 2 tabloid blogs say `false`, but the peer-reviewed journal says `true`.

**Why Hard is hard:** A 404 page contains a recovered cache snippet that is the decisive clue. Agents that skip 404 pages miss it entirely.

---

## Reward Logic

```
Dense rewards (each step):
  search (new, successful):  +0.10 − 0.01 step cost = +0.09 net  (max 1 reward)
  read   (new, valid URL):   +0.10 − 0.01 step cost = +0.09 net  (max 2 rewards)
  failed/duplicate action:   −0.01 step cost only

On submit:
  correct verdict:    +0.70
  unverified on medium: +0.30  (rational choice when evidence conflicts)
  wrong verdict:      +0.00

final_score = sum(all_step_rewards) clamped to [0.0, 1.0]
```

**Maximum achievable:** Search(+0.09) + Read(+0.09) + Read(+0.09) + Submit correct(+0.70) = **0.97**

---

## Anti-Exploit Measures

- ✅ 15 scenarios randomly sampled on `reset()` — no memorization possible
- ✅ Dense rewards capped: max 1 search reward, max 2 read rewards per episode
- ✅ Step cost (`−0.01`) on every step — discourages looping
- ✅ Re-reading the same URL → `0.0` reward
- ✅ Jaccard similarity search (stop-word filtered) — lazy 1-word queries fail
- ✅ Handles `JSONDecodeError`, `ValidationError`, and `APIError` gracefully

---

## Setup & Run

### Prerequisites
- Python 3.10+
- A free [HuggingFace API token](https://huggingface.co/settings/tokens)

### Local Run
```bash
pip install -r requirements.txt

export HF_TOKEN="hf_your_token_here"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"

# Run frontier agent
python inference.py

# Run baseline agent
python baseline.py
```

### Docker Run
```bash
docker build -t openenv-fact-checker .
docker run \
  -e HF_TOKEN=$HF_TOKEN \
  -e API_BASE_URL="https://router.huggingface.co/v1" \
  -e MODEL_NAME="Qwen/Qwen2.5-72B-Instruct" \
  openenv-fact-checker
```

---

## License

MIT
