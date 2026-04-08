from typing import Literal, Optional, Tuple, Set
from pydantic import BaseModel
import random
from database import MOCK_INTERNET


class Action(BaseModel):
    action_type: Literal["search", "read", "submit"]
    query: Optional[str] = None
    url: Optional[str] = None
    verdict: Optional[Literal["true", "false", "unverified"]] = None


class Observation(BaseModel):
    claim: str
    last_result: str
    step_count: int
    steps_remaining: int
    credibility_scores: dict[str, str] = {}
    discovered_urls: list[str] = []
    read_urls: list[str] = []
    available_actions: list[str] = []


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Mock Internet Database (zero-dependency, no web scraping)
# ---------------------------------------------------------------------------
# SCORE VARIANCE DESIGN:
#
#   task_easy   → ground_truth = "false"
#       Obvious lie. All models should get this. Weak=1.0, Strong=1.0
#
#   task_medium → ground_truth = "true"
#       The claim sounds absurd but IS true. Articles are split:
#       one official source confirms it, two "debunking" blogs loudly deny it.
#       A weak model will be overwhelmed by the majority-false signal and
#       answer "false." A strong model weighs SOURCE CREDIBILITY and answers
#       "true." Expected: Weak ≈ 0.0, Strong ≈ 0.7-1.0
#
#   task_hard   → ground_truth = "false"
#       TRAP: The claim cites a "Harvard study" with specific statistics.
#       The mock articles contain a real study that DOES exist, but the
#       claim subtly misquotes the key number (reverses cause & effect,
#       or cherry-picks). Article 1 seems to confirm the claim at first
#       glance. Article 2 is the actual study abstract that contradicts
#       the claim if read carefully. Article 3 is a RETRACTION notice.
#       A frontier model that skims will say "true." Only a careful
#       reader catches the discrepancy. Expected: Weak ≈ 0.0, Strong ≈ 0.5-0.7
# ---------------------------------------------------------------------------

# Maximum steps before environment auto-terminates
MAX_STEPS = 15

# Maximum times search/read rewards can be earned (anti-reward-hacking)
MAX_SEARCH_REWARDS = 1
MAX_READ_REWARDS = 2

# Reward constants
REWARD_SEARCH_NEW = 0.10       # Reward for a search that yields results
REWARD_READ_NEW = 0.10         # Reward for reading a new, valid URL
STEP_COST = 0.01               # Small cost per step to discourage looping
PENALTY_FAILED_ACTION = 0.0    # No reward for garbage searches or 404 reads


class FakeNewsEnv:
    """
    Hardened Fake News Fact-Checker environment.

    Anti-exploit measures:
      - Dense rewards ONLY for *new, successful* search/read actions
      - Step budget enforced inside environment (MAX_STEPS)
      - Per-step cost to discourage meaningless looping
      - Trajectory score computed holistically on submit
      - Reward capped at [0.0, 1.0] at all times
    """

    def __init__(self):
        self.task_id: Optional[str] = None
        self.step_count: int = 0
        self.history: list = []
        self.active_scenario: dict = {}
        # Anti-exploit tracking
        self.successful_searches: int = 0
        self.read_urls: Set[str] = set()
        self.has_searched: bool = False
        self.has_read: bool = False
        self.dense_reward_total: float = 0.0
        self.credibility_scores: dict[str, str] = {}
        self.discovered_urls: list[str] = []

    def reset(self, task_id: str) -> Observation:
        self.task_id = task_id
        self.step_count = 0
        self.history = []
        self.successful_searches = 0
        self.read_urls = set()
        self.has_searched = False
        self.has_read = False
        self.dense_reward_total = 0.0
        self.credibility_scores = {}
        self.discovered_urls = []

        self.active_scenario = random.choice(MOCK_INTERNET[self.task_id])
        claim = self.active_scenario["claim"]
        actions = ["search", "submit"]

        return Observation(
            claim=claim,
            last_result="Environment initialized. Use 'search' to begin investigating the claim.",
            step_count=0,
            steps_remaining=MAX_STEPS,
            credibility_scores=self.credibility_scores,
            discovered_urls=self.discovered_urls.copy(),
            read_urls=sorted(list(self.read_urls)),
            available_actions=actions,
        )

    def state(self) -> Observation:
        claim = self.active_scenario["claim"]
        last_res = self.history[-1] if self.history else "Environment initialized."
        
        actions = ["search", "submit"]
        if self.discovered_urls:
            actions.append("read")

        return Observation(
            claim=claim,
            last_result=last_res,
            step_count=self.step_count,
            steps_remaining=MAX_STEPS - self.step_count,
            credibility_scores=self.credibility_scores,
            discovered_urls=self.discovered_urls.copy(),
            read_urls=sorted(list(self.read_urls)),
            available_actions=actions,
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Optional[str]]:
        self.step_count += 1
        claim = self.active_scenario["claim"]
        reward = 0.0
        done = False
        error = None
        last_result = ""

        # ---------------------------------------------------------------
        # BUDGET CHECK: Auto-terminate if steps exhausted
        # ---------------------------------------------------------------
        if self.step_count > MAX_STEPS:
            done = True
            reward = 0.0
            last_result = "Step budget exhausted. Episode terminated with score 0.0."
            self.history.append(last_result)
            obs = Observation(
                claim=claim, last_result=last_result,
                step_count=self.step_count, steps_remaining=0,
            )
            return obs, reward, done, "max_steps_exceeded"

        # ---------------------------------------------------------------
        # ACTION: search
        # ---------------------------------------------------------------
        if action.action_type == "search":
            queries = self.active_scenario["search_results"]
            matched = False

            if action.query:
                stop_words = {"the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or", "is", "are", "do", "does", "did", "how", "what", "why", "when", "where", "can", "you", "it", "that", "this", "be", "with", "true", "false"}
                for key, results in queries.items():
                    query_words = set(action.query.lower().split())
                    query_words = {w for w in query_words if w not in stop_words}
                    key_words = set(key.split())
                    
                    if not query_words:
                        continue
                        
                    intersection = query_words.intersection(key_words)
                    union = query_words.union(key_words)
                    jaccard = len(intersection) / len(union) if union else 0.0

                    # Match if 2+ non-stop words overlap OR Jaccard similarity is > 0.25
                    if len(intersection) >= 2 or jaccard > 0.25:
                        last_result = f"Search results for '{action.query}': {results}"
                        for url in self.active_scenario["articles"]:
                            if url in results and url not in self.discovered_urls:
                                self.discovered_urls.append(url)
                        matched = True
                        break

            if matched:
                self.has_searched = True
                # Only reward if under the cap
                if self.successful_searches < MAX_SEARCH_REWARDS:
                    reward = REWARD_SEARCH_NEW
                    self.successful_searches += 1
                else:
                    reward = 0.0  # Capped, no more search rewards
            else:
                reward = PENALTY_FAILED_ACTION
                last_result = "No results found. Try different keywords from the claim."

        # ---------------------------------------------------------------
        # ACTION: read
        # ---------------------------------------------------------------
        elif action.action_type == "read":
            articles = self.active_scenario["articles"]

            if action.url and action.url in articles:
                import urllib.parse
                domain = urllib.parse.urlparse(action.url).netloc
                
                # Determine credibility rating
                cred_lower = domain.lower()
                if ".gov" in cred_lower or ".edu" in cred_lower or ".ac.uk" in cred_lower or ".org" in cred_lower or "nature.com" in cred_lower:
                    credibility = "High (Official/Peer-Reviewed)"
                elif ".fake" in cred_lower or "myths" in cred_lower or "lies" in cred_lower or "skeptic" in cred_lower or "debunk" in cred_lower or "creepy" in cred_lower or "miracle" in cred_lower:
                    credibility = "Low (Unverified/Tabloid)"
                else:
                    credibility = "Medium (Standard Media)"
                
                self.credibility_scores[domain] = credibility

                last_result = f"Article content ({action.url}): {articles[action.url]}\n[System Note: {domain} credibility rated as {credibility}]"
                self.has_read = True
                # Only reward for NEW urls
                if action.url not in self.read_urls and len(self.read_urls) < MAX_READ_REWARDS:
                    reward = REWARD_READ_NEW
                    self.read_urls.add(action.url)
                else:
                    reward = 0.0  # Already read or cap reached
            else:
                reward = PENALTY_FAILED_ACTION
                last_result = "Error 404: URL not found or inaccessible."

        # ---------------------------------------------------------------
        # ACTION: submit
        # ---------------------------------------------------------------
        elif action.action_type == "submit":
            done = True
            ground_truth = self.active_scenario["ground_truth"]
            is_correct = action.verdict == ground_truth

            # --- Holistic Trajectory Score ---
            # Components:
            #   correctness:        0.0 or 0.7 (dominant factor)
            #   investigation:      0.0 to 0.3 (did they search AND read?)
            #   investigation has sub-components:
            #     - searched at all:    0.10
            #     - read at all:        0.10
            #     - read 2+ sources:    0.10

            correctness_score = 0.0
            if is_correct:
                correctness_score = 0.7
            elif action.verdict == "unverified":
                if self.task_id == "task_medium":
                    # In medium tasks, the signal is noisy. "Unverified" is a 
                    # rational, cautious answer representing partial success.
                    correctness_score = 0.3
                else:
                    # For easy/hard tasks, the evidence definitively points to the answer,
                    # but unverified is still safer than a confident wrong answer.
                    correctness_score = 0.1

            # Give them only the correctness score here. Their investigation
            # quality is ALREADY captured by the dense rewards earned in previous steps.
            reward = correctness_score

            if is_correct:
                last_result = f"Verdict '{action.verdict}' is CORRECT. Correctness score: {reward}"
            else:
                last_result = f"Verdict '{action.verdict}' is INCORRECT (expected '{ground_truth}'). Correctness score: {reward}"

        else:
            error = f"Unknown action_type: {action.action_type}"
            last_result = error

        # Apply step cost to dense rewards (not submit)
        if action.action_type != "submit":
            reward = reward - STEP_COST

        self.history.append(last_result)

        obs = Observation(
            claim=claim, last_result=last_result,
            step_count=self.step_count,
            steps_remaining=max(0, MAX_STEPS - self.step_count),
            credibility_scores=self.credibility_scores,
            discovered_urls=self.discovered_urls.copy(),
            read_urls=sorted(list(self.read_urls)),
            available_actions=["search", "submit"] + (["read"] if self.discovered_urls else []),
        )
        return obs, reward, done, error
