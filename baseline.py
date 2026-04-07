"""
baseline.py — Dumb Baseline Agent (No LLM, rule-based)

This agent demonstrates what happens when a naive strategy is used:
  - It always searches once (to get some dense reward)
  - It NEVER reads any articles (skips investigation)
  - It always submits "false" as the verdict (majority-class guess)

Expected scores:
  task_easy:   ~0.80 (correct guess + partial investigation)
  task_medium: ~0.00 (wrong — truth is "true", agent always says "false")
  task_hard:   ~0.80 (lucky correct guess + partial investigation)
  Average:     ~0.53

This proves the environment has score variance: a dumb agent cannot
achieve a high average score, while a frontier model can.
"""
import os
from environment import FakeNewsEnv, Action


def run():
    env = FakeNewsEnv()
    tasks = ["task_easy", "task_medium", "task_hard"]
    model_name = "baseline-always-false"

    for task in tasks:
        print(f"[START] task={task} env=FakeNewsFactChecker model={model_name}")

        obs = env.reset(task)
        done = False
        step_count = 0
        total_rewards = []
        final_score = 0.0
        success = False

        # --- Strategy 1: Search once (grab some dense reward) ---
        step_count += 1
        # Extract first word from claim as a naive keyword
        keyword = obs.claim.split()[0].lower()
        action = Action(action_type="search", query=keyword)
        obs, reward, done, error = env.step(action)
        total_rewards.append(reward)
        actual_error = error if error else "null"
        print(
            f"[STEP] step={step_count} action={action.action_type} "
            f"reward={reward:.2f} done={str(done).lower()} error={actual_error}"
        )

        # --- Strategy 2: Skip reading entirely (lazy agent) ---
        # --- Strategy 3: Always submit "false" ---
        if not done:
            step_count += 1
            action = Action(action_type="submit", verdict="false")
            obs, reward, done, error = env.step(action)
            total_rewards.append(reward)
            actual_error = error if error else "null"
            print(
                f"[STEP] step={step_count} action={action.action_type} "
                f"reward={reward:.2f} done={str(done).lower()} error={actual_error}"
            )
            final_score = reward
            success = final_score >= 0.7

        rewards_str = ",".join([f"{r:.2f}" for r in total_rewards])
        print(
            f"[END] success={str(success).lower()} steps={step_count} "
            f"score={final_score:.2f} rewards={rewards_str}"
        )


if __name__ == "__main__":
    run()
