import os
import json
import logging

from groq import Groq
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GROQ_KEY")
api = Groq(api_key=api_key)


def fetch_llm_review(system_prompt, user_message, max_attempts=3):
    attempt = 0

    while attempt < max_attempts:
        try:
            response = request_to_llm(system_prompt, user_message)
            response = response.replace("```json", "```")
            response = response.replace("```", "")

            response_json = json.loads(response)

            for param in ("rating", "downsides", "conclusion"):
                if param not in response_json:
                    logging.error(f"Param '{param}' was not provided in LLM response")
                    raise ValueError(f"Missing parameter: {param}")

            return response_json

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logging.error(f"Attempt {attempt + 1} failed. Error: {e}. Response: {response}")
            attempt += 1

    logging.error("All attempts to process LLM response failed.")
    raise ValueError("Failed to process LLM response")


def request_to_llm(system_prompt, user_prompt):
    completion = api.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    return completion.choices[0].message.content
