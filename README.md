# Camplight API

This is a simple API with an LLM application. It receives a sentence which may have grammatical errors and returns a
fixed sentence with no errors.

# Example Input

production_json = \
{\
    "sentence": "example sentence you want to check the grammar and style"\
}

## URL

https://camplight-api-test.vercel.app/

## Limitations

This app was deployed using Vercel. Vercel has a limit of 250MB per function. Including 'dspy' results in exceeding
the limit. To avoid this, the production deployment does not include 'dspy'. It still returns the expected result
with traditional OpenAI calls.

## Running Locally

Running locally allows for the user to test the 'dspy' output. Modification to the main.py file will be needed.

```bash
pip install -r requirements.txt
pip install dspy==2.6.13

python3 api/main.py
```

This will now allow you to do an POST request to `http://localhost:3000`.

# Evaluation

For larger applications using LLMs, mlflow is a great way to track
model improvements. A large dataset is needed but it allows for automatic
evaluation.

In production environments, having a reliable way to track feedback and 
user usage/satisfaction is needed. For this specific task, whenever a suggestion
is given to the user, we need track if the user takes that suggestion or ignores it. A simple way to view it is to compare the message the user sent after the recommendation against the one provided 
by the LLM. 

Since LLMs are more difficult to evaluate than standard AI/ML solutions, I believe that using tangible feedback from users is the best option in determining whether a model is performing well.

Once sufficient feedback has been collected, it can be organised into a dataset and be used in afforementioned mlflow implementation for automated testing in future releases.

# TODO

Queueing was mentioned in the task description. I did not have the time to implement it and I would also like to have a chat about it since from my perspective queueing can possibly slow things down in a real-time environment.
