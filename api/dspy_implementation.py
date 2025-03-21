import os

import dspy

from llm import Sentence, DEFAULT_MODEL

API_KEY = os.getenv("OPENAI_API_KEY")


def configure(model: str = DEFAULT_MODEL):
    lm = dspy.LM(model, api_key=API_KEY)
    dspy.configure(lm=lm)


class InputOutput(dspy.Signature):
    sentence_with_or_without_grammatical_and_stylistic_error: Sentence = dspy.InputField()
    fixed_sentence: str = dspy.OutputField()


def dspy_prediction(query: str) -> str:
    predictor = dspy.ChainOfThought(InputOutput)

    prediction = predictor(sentence_with_or_without_grammatical_and_stylistic_error=query)

    return prediction.fixed_sentence
