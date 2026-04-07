# 🕵️ Active Investigation / Fake News Fact-Checker

An OpenEnv reinforcement learning environment where an AI agent uses `search` and `read` tools to investigate claims before submitting a final `verdict` (`true`, `false`, or `unverified`).

Built for the **OpenEnv AI Agent Hackathon**.

---

## Project Structure

```
openenv-hackathon/
├── environment.py      # Core RL environment (Pydantic schemas, mock internet, grader)
├── inference.py        # Frontier agent (Qwen-72B via HuggingFace Serverless API)
├── baseline.py         # Dumb baseline agent (always guesses "false", no reading)
├── openenv.yaml        # OpenEnv task declaration (Easy, Medium, Hard)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container for reproducible runs
└── README.md           # This file
```

## Tasks & Score Variance

| Task | Difficulty | Trap | Ground Truth | Baseline Score | Frontier Score |
|------|-----------|------|-------------|---------------|---------------|
| Easy | 🟢 | Popular myth, all sources agree | `false` | ~0.80 | ~1.00 |
| Medium | 🟡 | True claim buried under 2 loud "debunking" blogs | `true` | ~0.00 | ~0.30-1.00 |
| Hard | 🔴 | Fake "47% statistic" attributed to a real Stanford study | `false` | ~0.80 | ~1.00 |

**Why Medium is hard:** The correct answer is `"true"`, but 2 out of 3 articles aggressively call it false. Only the peer-reviewed archaeology journal confirms it. A weak agent that follows majority opinion will fail.

**Why Hard is hard:** Article 1 (clickbait) loudly confirms the claim. Articles 2 & 3 (the actual study + a correction notice) quietly contradict it. A skimming agent will say `"true"` — only careful cross-referencing catches the discrepancy.

## Anti-Exploit Measures

- ✅ Dense rewards ONLY for **new, successful** search/read actions (capped at 3 each)
- ✅ Step budget enforced inside environment (`MAX_STEPS=15`)
- ✅ Per-step cost (`-0.01`) to discourage meaningless looping
- ✅ Re-reading same URL → `0.0` reward
- ✅ Failed searches / 404 reads → `0.0` reward
- ✅ Holistic trajectory scoring on submit: `correctness (0.7) + investigation_quality (0.3)`
- ✅ Catches `JSONDecodeError`, `ValidationError`, and `openai.APIError` gracefully

## Setup & Run

### Prerequisites
- Python 3.10+
- A free [HuggingFace API token](https://huggingface.co/settings/tokens)

### Local Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export HF_TOKEN="hf_your_token_here"

# Run frontier agent
python inference.py

# Run baseline (no API key needed)
python baseline.py
```

### Docker Run
```bash
docker build -t openenv-hackathon .
docker run -e HF_TOKEN=$HF_TOKEN openenv-hackathon
```

## Reward Logic

```
On each step (search/read):
  reward = 0.05 (if new + successful) - 0.01 (step cost) = 0.04 net
  reward = 0.00 (if duplicate, failed, or cap reached)

On submit:
  correctness    = 0.70 if verdict matches ground_truth, else 0.00
  investigation  = 0.10 (searched) + 0.10 (read) + 0.10 (read 2+ sources)
  efficiency     = -0.01 per step beyond 6
  final_score    = clamp(correctness + investigation - efficiency, 0.0, 1.0)
```

## License

MIT
