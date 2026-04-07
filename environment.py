from typing import Literal, Optional, Dict, Any, Tuple
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

# Mock Internet Database enforcing the 0-dependency/local requirement
MOCK_INTERNET = {
    "task_easy": {
        "claim": "Eating 1kg of uranium provides your daily recommended caloric intake.",
        "search_results": {
            "uranium daily calories intake": "[1] https://science-facts.org/uranium-nutrition",
        },
        "articles": {
            "https://science-facts.org/uranium-nutrition": "Uranium does contain millions of calories in terms of pure atomic energy potential, but it is radioactive metal. Human digestion cannot metabolize uranium into nutritional calories. Eating it will kill you, not provide healthy calories."
        },
        "ground_truth": "false"
    },
    "task_medium": {
        "claim": "A new peer-reviewed study proves caffeine causes a 50% increase in heart disease.",
        "search_results": {
            "study caffeine heart disease 50% increase": "[1] https://medical-journals.org/caffeine-study-2026"
        },
        "articles": {
            "https://medical-journals.org/caffeine-study-2026": "Our 10-year study found that caffeine consumption causes a 50% relative increase in the rate of heart disease EXCLUSIVELY among individuals possessing the rare XYZ-1 genetic mutation (0.01% of the population). For the remaining 99.99%, caffeine showed slight cardioprotective effects."
        },
        "ground_truth": "false" # It's false because the claim implies a general truth, omitting the critical genetic caveat.
    },
    "task_hard": {
        "claim": "The mysterious 'Red Signal' phenomenon observed last night over the Pacific Ocean is a classified military test.",
        "search_results": {
            "red signal pacific ocean military test": "[1] https://military.gov/press-release/red-signal [2] https://global-news.com/red-signal-mystery"
        },
        "articles": {
            "https://military.gov/press-release/red-signal": "Error 404: Page removed or classified.",
            "https://global-news.com/red-signal-mystery": "Military spokespersons flatly refuse to confirm or deny involvement in the 'Red Signal' event. Civilian astronomers strongly suspect it was a meteor, but leaked unauthenticated forum posts claim it was a weapon. The government has initiated a total media blackout. The origin remains highly unknown."
        },
        "ground_truth": "unverified"
    }
}

class FakeNewsEnv:
    def __init__(self):
        self.task_id = None
        self.step_count = 0
        self.actions_taken = set()
        self.history = []

    def reset(self, task_id: str) -> Observation:
        self.task_id = task_id
        self.step_count = 0
        self.actions_taken = set()
        self.history = []
        
        claim = MOCK_INTERNET[self.task_id]["claim"]
        return Observation(
            claim=claim, 
            last_result="Environment initialized. Awaiting your first search action.", 
            step_count=0
        )

    def state(self) -> Observation:
        claim = MOCK_INTERNET[self.task_id]["claim"]
        last_res = self.history[-1] if self.history else "Environment initialized."
        return Observation(claim=claim, last_result=last_res, step_count=self.step_count)

    def step(self, action: Action) -> Tuple[Observation, float, bool, Optional[str]]:
        self.step_count += 1
        claim = MOCK_INTERNET[self.task_id]["claim"]
        reward = 0.0
        done = False
        error = None
        last_result = ""

        # Process actions
        if action.action_type == "search":
            self.actions_taken.add("search")
            reward = 0.1  # Dense reward for exploring
            queries = MOCK_INTERNET[self.task_id]["search_results"]
            matched = False
            
            if action.query:
                # Loose keyword matching for the mock database
                for key, results in queries.items():
                    if any(word.lower() in key.split() for word in action.query.lower().split()):
                        last_result = f"Search results for '{action.query}': {results}"
                        matched = True
                        break
            
            if not matched:
                last_result = "No results found. Try using different keywords from the claim."

        elif action.action_type == "read":
            self.actions_taken.add("read")
            reward = 0.1  # Dense reward for extracting information
            articles = MOCK_INTERNET[self.task_id]["articles"]
            
            if action.url and action.url in articles:
                last_result = f"Article content ({action.url}): {articles[action.url]}"
            else:
                last_result = f"Error 404: URL not found or inaccessible."

        elif action.action_type == "submit":
            self.actions_taken.add("submit")
            done = True
            is_correct = action.verdict == MOCK_INTERNET[self.task_id]["ground_truth"]
            
            # Trajectory Reward Logic
            if is_correct:
                if "search" in self.actions_taken and "read" in self.actions_taken:
                    reward = 1.0  # Perfect execution
                    last_result = "Correct verdict validated with proper investigation."
                else:
                    reward = 0.2  # Heavy penalty for hallucinating/guessing
                    last_result = "Correct verdict, but heavily penalized for failing to search and read sources."
            else:
                reward = 0.0
                last_result = "Incorrect verdict."

        else:
            error = "Unknown action_type."

        # Bound trajectory scores safely
        reward = max(0.0, min(1.0, float(reward)))
        self.history.append(last_result)
        
        obs = Observation(claim=claim, last_result=last_result, step_count=self.step_count)
        return obs, reward, done, error
