import logging

from flask import Flask, request

from llm import get_llm_response, get_openai_client
from cache import redis_connection, write, read
from dspy_implementation import dspy_prediction, configure


app = Flask(__name__)
logger = logging.Logger(__name__)

logger.setLevel(logging.INFO)


@app.route('/', methods=["POST"])
def correct_errors():
    redis_client = redis_connection()

    prompt = request.get_json().get("prompt")
    if not prompt:
        raise ValueError("'prompt' variable not provided in request!")

    existing_response = read(redis_client=redis_client, original_prompt=prompt)  # Checks if sentence was already seen
    if existing_response is not None:  # If so, return the previous result
        logging.info("Question already asked!")
        return {"sentence": existing_response}

    method = request.get_json().get("implementation", "traditional")

    if method == "traditional":
        client = get_openai_client()

        response = get_llm_response(query=prompt, client=client)

    elif method == "dspy":
        configure()
        response = dspy_prediction(query=prompt)

    else:
        raise ValueError("method variable can only be 'traditional' or 'dspy'.")

    write(redis_client=redis_client, original_prompt=prompt, fixed_prompt=response)  # Write to redis for future reference

    return {"sentence": response}


if __name__ == "__main__":
    app.run(port=8000)
