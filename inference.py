import os
import json
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError
from pydantic import ValidationError
from environment import FakeNewsEnv, Action


def run():
    # ---------------------------------------------------------------
    # Credentials: read from environment (hackathon requirement)
    # ---------------------------------------------------------------
    base_url = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
    api_key = os.environ.get("HF_TOKEN", "replace_with_your_hf_token")

    client = OpenAI(api_key=api_key, base_url=base_url)
    model_name = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

    env = FakeNewsEnv()
    tasks = ["task_easy", "task_medium", "task_hard"]

    # ---------------------------------------------------------------
    # System prompt — no markdown fences, strict JSON instruction
    # ---------------------------------------------------------------
    SYSTEM_PROMPT = (
        "You are an autonomous fact-checking AI agent. You investigate claims "
        "by searching for evidence and reading articles before submitting a verdict.\n\n"
        "IMPORTANT: You MUST output ONLY valid JSON. No markdown, no explanation, no commentary.\n\n"
        "JSON schema (output exactly one JSON object per turn):\n"
        '  action_type: one of "search", "read", or "submit"\n'
        '  query: string (required when action_type is "search", omit otherwise)\n'
        '  url: string (required when action_type is "read", omit otherwise)\n'
        '  verdict: one of "true", "false", or "unverified" (required when action_type is "submit", omit otherwise)\n\n'
        "Your investigation workflow:\n"
        "1. First, SEARCH using keywords extracted from the claim.\n"
        "2. Then, READ each URL returned in the search results. Read ALL available URLs.\n"
        "3. After reading ALL sources, SUBMIT your verdict.\n\n"
        "Verdict rules:\n"
        '- "true" if the claim is factually supported by credible sources.\n'
        '- "false" if the claim is contradicted or debunked by credible sources.\n'
        '- "unverified" if sources conflict, evidence is insufficient, or no authoritative confirmation exists.\n\n'
        "Be skeptical of unverified blogs and anonymous sources. Prefer official/scientific sources. "
        "Do NOT guess. If evidence is genuinely ambiguous, choose unverified."
    )

    # ---------------------------------------------------------------
    # Task loop
    # ---------------------------------------------------------------
    for task in tasks:
        print(f"[START] task={task} env=FakeNewsFactChecker model={model_name}")

        obs = env.reset(task)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Investigate this claim: \"{obs.claim}\"\n"
                    f"Status: {obs.last_result}\n"
                    f"Steps remaining: {obs.steps_remaining}"
                ),
            },
        ]

        done = False
        step_count = 0
        total_rewards = []
        final_score = 0.0
        success = False

        while not done and step_count < 10:
            step_count += 1
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    response_format={"type": "json_object"},
                    max_tokens=256,
                    temperature=0.0,
                )

                raw_output = response.choices[0].message.content

                # Parse and validate
                action_data = json.loads(raw_output)
                action = Action(**action_data)

                # Execute step
                obs, reward, done, error = env.step(action)
                total_rewards.append(reward)
                actual_error = error if error else "null"

                # Strict Format: STEP
                print(
                    f"[STEP] step={step_count} action={action.action_type} "
                    f"reward={reward:.2f} done={str(done).lower()} "
                    f"error={actual_error}"
                )

                # Maintain conversation memory
                messages.append({"role": "assistant", "content": raw_output})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"Result: {obs.last_result}\n"
                            f"Step: {obs.step_count} | Steps remaining: {obs.steps_remaining}"
                        ),
                    }
                )

                if done:
                    final_score = reward
                    success = final_score >= 0.7

            except (json.JSONDecodeError, ValidationError) as e:
                error_msg = str(e).replace("\n", " ")[:200]
                print(
                    f"[STEP] step={step_count} action=invalid "
                    f"reward=0.00 done=true error={error_msg}"
                )
                total_rewards.append(0.0)
                final_score = 0.0
                done = True
                success = False

            except (APIError, APIConnectionError, APITimeoutError) as e:
                error_msg = str(e).replace("\n", " ")[:200]
                print(
                    f"[STEP] step={step_count} action=api_error "
                    f"reward=0.00 done=true error={error_msg}"
                )
                total_rewards.append(0.0)
                final_score = 0.0
                done = True
                success = False

        # Handle edge case: loop ended without submit (step budget in inference)
        if not done:
            total_rewards.append(0.0)
            final_score = 0.0
            success = False
            print(
                f"[STEP] step={step_count} action=timeout "
                f"reward=0.00 done=true error=inference_step_limit_reached"
            )

        rewards_str = ",".join([f"{r:.2f}" for r in total_rewards])
        print(
            f"[END] success={str(success).lower()} steps={step_count} "
            f"score={final_score:.2f} rewards={rewards_str}"
        )


if __name__ == "__main__":
    run()
