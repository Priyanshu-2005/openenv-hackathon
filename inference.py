import os
import json
from openai import OpenAI
from pydantic import ValidationError
from environment import FakeNewsEnv, Action

def run():
    # Setup credentials defaulting to Hugging Face's free OpenAI-compatible API
    base_url = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
    api_key = os.environ.get("HF_TOKEN", "replace_with_your_hf_token")
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    # Popular, free capable model on HF Serverless API
    model_name = "Qwen/Qwen2.5-72B-Instruct"
    
    env = FakeNewsEnv()
    tasks = ["task_easy", "task_medium", "task_hard"]

    SYSTEM_PROMPT = """You are an elite, autonomous fact-checker AI. Your goal is to verify claims.
You must use tools sequentially. Always output strictly valid JSON matching this schema:
{
  "action_type": "search" | "read" | "submit",
  "query": "string, used only for search (optional)",
  "url": "string, used only for read (optional)",
  "verdict": "true" | "false" | "unverified", used only for submit (optional)
}
Step 1: "search" using keywords derived from the claim.
Step 2: "read" the exact URLs discovered in the search results.
Step 3: "submit" your final verdict based on the read articles."""

    for task in tasks:
        # Strict Format: START
        print(f"[START] task={task} env=FakeNewsFactChecker model={model_name}")
        
        obs = env.reset(task)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Claim to verify: {obs.claim}\nLast Result: {obs.last_result}\nStep: {obs.step_count}"}
        ]
        
        done = False
        step_count = 0
        total_rewards = []
        final_score = 0.0
        success = False

        while not done and step_count < 10:
            step_count += 1
            try:
                # Relying on JSON mode to enforce structured outputs
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    response_format={"type": "json_object"},
                    max_tokens=256,
                    temperature=0.0
                )
                
                raw_output = response.choices[0].message.content
                action_data = json.loads(raw_output)
                action = Action(**action_data)
                
                # Execute against environment
                obs, reward, done, error = env.step(action)
                total_rewards.append(reward)
                actual_error = error if error else "null"
                
                # Strict Format: STEP
                print(f"[STEP] step={step_count} action={action.action_type} reward={reward:.2f} done={str(done).lower()} error={actual_error}")
                
                # Maintain memory
                messages.append({"role": "assistant", "content": raw_output})
                messages.append({"role": "user", "content": f"Next State -> Last Result: {obs.last_result}\nStep: {obs.step_count}"})
                
                if done:
                    final_score = reward
                    success = final_score == 1.0

            except (json.JSONDecodeError, ValidationError) as e:
                # Catch failures dynamically preventing global crash
                error_msg = str(e).replace('\n', ' ')
                print(f"[STEP] step={step_count} action=invalid reward=0.00 done=true error={error_msg}")
                total_rewards.append(0.0)
                final_score = 0.0
                done = True
                success = False

        rewards_str = ",".join([f"{r:.2f}" for r in total_rewards])
        
        # Strict Format: END
        print(f"[END] success={str(success).lower()} steps={step_count} score={final_score:.2f} rewards={rewards_str}")

if __name__ == "__main__":
    run()

