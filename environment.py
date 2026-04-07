from typing import Literal, Optional, Tuple, Set
from pydantic import BaseModel


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
MOCK_INTERNET = {
    "task_easy": {
        "claim": "The Great Wall of China is visible from the Moon with the naked eye.",
        "search_results": {
            "great wall china visible moon": (
                "[1] https://nasa.gov/ask-astronaut/great-wall "
                "[2] https://myths-debunked.org/great-wall-moon"
            ),
            "can you see great wall from space": (
                "[1] https://nasa.gov/ask-astronaut/great-wall"
            ),
        },
        "articles": {
            "https://nasa.gov/ask-astronaut/great-wall": (
                "NASA astronauts have confirmed multiple times that the Great Wall of China "
                "is NOT visible from the Moon. The wall is only about 15 feet wide, which "
                "is far too narrow to be resolved by the human eye from orbital distance, "
                "let alone from the Moon (238,900 miles away). Even from low Earth orbit "
                "(250 miles), the wall is extremely difficult to spot without aid. This is "
                "one of the most persistent myths in popular culture."
            ),
            "https://myths-debunked.org/great-wall-moon": (
                "DEBUNKED: The claim that the Great Wall is visible from the Moon has been "
                "repeatedly denied by every astronaut who has visited the Moon, including "
                "Apollo 12 commander Alan Bean. The wall is simply too thin."
            ),
        },
        "ground_truth": "false",
    },
    "task_medium": {
        "claim": "Honey never spoils and 3,000-year-old honey found in Egyptian tombs was still edible.",
        "search_results": {
            "honey never spoils egyptian tombs": (
                "[1] https://archaeology-journal.org/egyptian-honey-discovery "
                "[2] https://food-myths.blog/honey-forever "
                "[3] https://health-debunk.com/honey-lies"
            ),
            "ancient honey edible preservation": (
                "[1] https://archaeology-journal.org/egyptian-honey-discovery "
                "[2] https://food-myths.blog/honey-forever"
            ),
        },
        "articles": {
            "https://archaeology-journal.org/egyptian-honey-discovery": (
                "PEER-REVIEWED PUBLICATION — Journal of Archaeological Science, Vol. 142, "
                "pp. 105-118. DOI: 10.1016/j.jas.2022.105592. "
                "Authors: Dr. Sarah Mitchell (University of Cambridge, Dept. of Archaeology), "
                "Dr. Ahmed Hassan (Cairo Museum of Antiquities). "
                "During excavations of Egyptian tombs near Thebes, archaeologists discovered "
                "sealed ceramic jars of honey dating to approximately 1000 BCE — over 3,000 "
                "years old. Laboratory analysis (mass spectrometry, microbial culture assays) "
                "confirmed the honey had undergone minimal chemical degradation. Honey's "
                "naturally low water activity (Aw < 0.6), acidic pH (3.2-4.5), and enzymatic "
                "production of hydrogen peroxide via glucose oxidase create a potent antimicrobial "
                "environment. The sealed samples were microbiologically sterile and chemically "
                "stable. CONCLUSION: Properly sealed honey resists spoilage indefinitely and "
                "the 3,000-year-old samples were confirmed safe for human consumption."
            ),
            "https://food-myths.blog/honey-forever": (
                "STOP BELIEVING THIS NONSENSE! I'm a mom of three and I KNOW food. Honey "
                "absolutely DOES spoil — I left a jar open in my kitchen and it grew mold "
                "within 3 months!! The 'Egyptian tomb honey' story is just clickbait that "
                "food bloggers repeat for ad revenue. No REAL scientist would eat 3,000-year-old "
                "anything. Wake up people! This is the same internet that thinks 5G causes "
                "cancer and you can charge your phone in a microwave. DO YOUR OWN RESEARCH!"
            ),
            "https://health-debunk.com/honey-lies": (
                "FACT CHECK by HealthDebunk Staff (no author listed): "
                "The claim that honey 'never spoils' is MISLEADING. We tested store-bought "
                "honey and found that when left UNSEALED in a humid environment (>60% RH), "
                "honey absorbs moisture and ferments within 6-8 weeks. Therefore, honey DOES "
                "spoil under normal household conditions. "
                "VERDICT: We rate the claim that honey never spoils as FALSE. "
                "Note: We did not evaluate the specific claim about sealed Egyptian tomb honey."
            ),
        },
        "ground_truth": "true",
    },
    "task_hard": {
        "claim": "A 2024 Stanford study proved that remote workers are 47% less productive than office workers.",
        "search_results": {
            "stanford study remote workers productivity 47%": (
                "[1] https://business-insider.fake/stanford-remote-work-study "
                "[2] https://stanford.edu/research/remote-productivity-2024 "
                "[3] https://stanford.edu/notices/corrections-2024"
            ),
            "remote work productivity study 2024": (
                "[1] https://business-insider.fake/stanford-remote-work-study "
                "[2] https://stanford.edu/research/remote-productivity-2024"
            ),
        },
        "articles": {
            "https://business-insider.fake/stanford-remote-work-study": (
                "HEADLINE: Stanford Confirms Remote Work Kills Productivity — 47% Drop Found. "
                "A new Stanford study by Professor Nicholas Bloom, one of the world's leading "
                "economists on workplace productivity, has definitively proven that remote "
                "workers are 47% less productive than their in-office counterparts. The "
                "randomized controlled trial, conducted with 1,612 employees at a Fortune 500 "
                "tech company, measured code commits, performance reviews, and promotion rates "
                "over 12 months. 'The data is unambiguous,' Dr. Bloom reportedly stated in a "
                "press conference. 'Remote work fundamentally undermines productivity.' The "
                "study was published in the Quarterly Journal of Economics (QJE) and has "
                "already been cited by Amazon CEO Andy Jassy and JP Morgan CEO Jamie Dimon "
                "to justify their return-to-office mandates."
            ),
            "https://stanford.edu/research/remote-productivity-2024": (
                "Bloom, N., Han, R., & Liang, J. (2024). 'The Impact of Hybrid Work "
                "Arrangements on Employee Output.' Quarterly Journal of Economics, 139(3), "
                "pp. 1399-1451. DOI: 10.1093/qje/qjad046. ABSTRACT: We report results from "
                "a randomized controlled trial at Trip.com (n=1,612) examining the causal "
                "impact of hybrid work schedules on six performance dimensions. Employees "
                "randomly assigned to work from home two days per week exhibited no statistically "
                "significant change in performance review scores (coeff. = -0.004, 95% CI "
                "[-0.019, 0.011], p = 0.42), lines of code committed (p = 0.67), or promotion "
                "rates (p = 0.51) relative to the fully in-office control group. The primary "
                "finding of this study is a null result on productivity. Notably, hybrid "
                "workers exhibited a 35% reduction in attrition rates (p < 0.001), suggesting "
                "substantial cost savings from reduced turnover. Limitations: This study "
                "examines hybrid (2 days WFH) arrangements; results should not be extrapolated "
                "to fully remote (5 days WFH) contexts without further research."
            ),
            "https://stanford.edu/notices/corrections-2024": (
                "ERROR 404 — The requested resource is no longer available. "
                "The Stanford Research Communications archive underwent a server migration "
                "in March 2024. Some legacy content has been permanently removed. "
                "For DOI resolution, please visit https://doi.org directly."
            ),
        },
        "ground_truth": "false",
    },
}

# Maximum steps before environment auto-terminates
MAX_STEPS = 15

# Maximum times search/read rewards can be earned (anti-reward-hacking)
MAX_SEARCH_REWARDS = 3
MAX_READ_REWARDS = 3

# Reward constants
REWARD_SEARCH_NEW = 0.05       # Reward for a search that yields results
REWARD_READ_NEW = 0.05         # Reward for reading a new, valid URL
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
        # Anti-exploit tracking
        self.successful_searches: int = 0
        self.read_urls: Set[str] = set()
        self.has_searched: bool = False
        self.has_read: bool = False
        self.dense_reward_total: float = 0.0

    def reset(self, task_id: str) -> Observation:
        self.task_id = task_id
        self.step_count = 0
        self.history = []
        self.successful_searches = 0
        self.read_urls = set()
        self.has_searched = False
        self.has_read = False
        self.dense_reward_total = 0.0

        claim = MOCK_INTERNET[self.task_id]["claim"]
        return Observation(
            claim=claim,
            last_result="Environment initialized. Use 'search' to begin investigating the claim.",
            step_count=0,
            steps_remaining=MAX_STEPS,
        )

    def state(self) -> Observation:
        claim = MOCK_INTERNET[self.task_id]["claim"]
        last_res = self.history[-1] if self.history else "Environment initialized."
        return Observation(
            claim=claim,
            last_result=last_res,
            step_count=self.step_count,
            steps_remaining=MAX_STEPS - self.step_count,
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Optional[str]]:
        self.step_count += 1
        claim = MOCK_INTERNET[self.task_id]["claim"]
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
            queries = MOCK_INTERNET[self.task_id]["search_results"]
            matched = False

            if action.query:
                for key, results in queries.items():
                    query_words = set(action.query.lower().split())
                    key_words = set(key.split())
                    if query_words & key_words:  # At least one keyword overlap
                        last_result = f"Search results for '{action.query}': {results}"
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
            articles = MOCK_INTERNET[self.task_id]["articles"]

            if action.url and action.url in articles:
                last_result = f"Article content ({action.url}): {articles[action.url]}"
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
            ground_truth = MOCK_INTERNET[self.task_id]["ground_truth"]
            is_correct = action.verdict == ground_truth

            # --- Holistic Trajectory Score ---
            # Components:
            #   correctness:        0.0 or 0.7 (dominant factor)
            #   investigation:      0.0 to 0.3 (did they search AND read?)
            #   investigation has sub-components:
            #     - searched at all:    0.10
            #     - read at all:        0.10
            #     - read 2+ sources:    0.10

            correctness_score = 0.7 if is_correct else 0.0

            investigation_score = 0.0
            if self.has_searched:
                investigation_score += 0.10
            if self.has_read:
                investigation_score += 0.10
            if len(self.read_urls) >= 2:
                investigation_score += 0.10

            trajectory_score = correctness_score + investigation_score

            # Apply step efficiency bonus/penalty: 
            # No penalty if steps <= 6 (efficient). Mild penalty for excess steps.
            if self.step_count > 6:
                excess = self.step_count - 6
                trajectory_score -= excess * STEP_COST

            # HARD CLAMP to [0.0, 1.0]
            reward = max(0.0, min(1.0, round(trajectory_score, 2)))

            if is_correct:
                last_result = f"Verdict '{action.verdict}' is CORRECT. Trajectory score: {reward}"
            else:
                last_result = f"Verdict '{action.verdict}' is INCORRECT (expected '{ground_truth}'). Trajectory score: {reward}"

        else:
            error = f"Unknown action_type: {action.action_type}"
            last_result = error

        # Apply step cost to dense rewards (not submit)
        if action.action_type != "submit":
            reward = max(0.0, reward - STEP_COST)

        # Final safety clamp
        reward = max(0.0, min(1.0, float(reward)))
        self.history.append(last_result)

        obs = Observation(
            claim=claim, last_result=last_result,
            step_count=self.step_count,
            steps_remaining=max(0, MAX_STEPS - self.step_count),
        )
        return obs, reward, done, error
