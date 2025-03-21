import os

import openai
from pydantic import BaseModel, Field

API_KEY = os.getenv("OPENAI_API_KEY")

GPT_4O = "gpt-4o-2024-08-06"
GPT_4O_MINI = "gpt-4o-mini-2024-07-18"

DEFAULT_MODEL = GPT_4O


def get_openai_client() -> openai.Client:
    return openai.OpenAI(api_key=API_KEY)


class Sentence(BaseModel):
    sentence: str = Field(
        title="sentence",
        description="This is a sentence which may require correction. Think of it as a text message in a chat."
    )


def compose_prompt(query: str) -> list:
    SYSTEM_PROMPT = f"""You are an expert in grammar rules in English and are capable of finding grammatical
                        and stylistic errors in all types of sentences.

                        You will receive a single sentence where a grammatical error MAY exist or it may not.
                        Same applies for styling. A sentence could be styled correctly, or could be confusing
                        to read.

                        If a sentence does not have a grammatical error and a stylistic error, you return it 
                        in it's original state."""

    USER_PROMPT = f"""Here is the received sentence: {query}"""

    return [{"role": "system",
             "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": USER_PROMPT}]


def get_llm_response(query: str, client: openai.OpenAI):
    messages = compose_prompt(query=query)

    completion = client.beta.chat.completions.parse(
        model=DEFAULT_MODEL,
        messages=messages,
        response_format=Sentence,
        temperature=0
    )

    return completion.choices[0].message.content
