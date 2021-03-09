import os, sys, datetime
import re, operator

# 3rd party import
import numpy as np

# local imports

## utils
sentence_flatten = lambda t: [word for item in t for word in item.split(" ")]
flatten = lambda t: [item for sublist in t for item in sublist]


def unique(list1):
    x = np.array(list1)
    return np.unique(x)


def get_prompt_length(p):
    """
    This function will receive a list of sentences.
    It will return the total word of all
    sentences in the list as an int.
    """
    if len(p) == 0:
        return 0
    elif len(p) == 1:
        return len(p[0].split(" "))
    else:
        return len(sentence_flatten(p))


def find_speakers(lines):
    """
    This function will take in the data straight
    off the file reader and analyze for possible
    RegEx patterns to find all distinct speaker in the
    podcast

    returns: a list of distinct speakers in podcast
    """
    colon_pattern = r"([A-Z][A-z]+\s[A-Z][A-z]+):"
    newline_pattern = r"\n([A-Z][A-z]+ [A-Z][A-z]+)\n"

    strr = " ".join(sentence_flatten(lines))

    colon_matches = re.findall(colon_pattern, strr)
    newline_matches = re.findall(newline_pattern, strr)

    return list(unique(colon_matches)) + list(unique(newline_matches))


def find_last_speaker(prompt, speakers):
    speak_dict = {}
    for s in speakers:
        if s in prompt:
            speak_dict[s] = prompt.rfind(s)

    return max(speak_dict.items(), key=operator.itemgetter(1))[0]


def less_than_500():
    from gptparser import make_prompts

    doc_path = os.path.join("..", "docs", "timferris-harryfinkelstein.txt")

    prompts = make_prompts(doc_path, LIMIT=500)

    bools = []

    for p in prompts:
        if len(p.split(" ")) <= 500:
            bools.append(True)
        else:
            bools.append(False)

    if False in bools:
        return False
    else:
        return True
