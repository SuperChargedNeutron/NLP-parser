import os

import pytest
from func import get_prompt_length, less_than_500
from gptparser import make_prompts


def test_propt_length1():
    assert get_prompt_length(["a word is worth how much in integers?"]) == 8


def test_two_sents():
    assert get_prompt_length(["two words", "three words", "six words"]) == 6


def prompts_less_than_500():
    assert less_than_500() == True
