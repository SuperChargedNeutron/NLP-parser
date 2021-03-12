import os, sys, datetime, io
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


def make_prompts(txt_file, LIMIT=350):
    """
    function takes in a file and a word limit for each prompts

    file: file of .txt format
    parses by sentences and count words by seperating
    the text in each space character.
    """
    # read transcript from file
    with io.open(txt_file, "r", encoding="utf-8") as fil:
        timestamp_regex = re.compile(r"[0-9]+:[0-9]+:?[0-9]+", flags=re.IGNORECASE)
        lines = fil.read().replace("\ufeff", "")

        lines = timestamp_regex.sub("", lines).split(".")
    # .repalce('\n') does GTP3 have some sort of preference with newlines?
    speakers = find_speakers(lines)

    # # initialize empty variables to be used in the loop
    prompts = []
    p = []

    for l in lines:

        # add the new sentence
        l = f"{l}."
        p.append(l)
        p_length = get_prompt_length(p)

        # if the sentence is within 10 words of the 500 limit
        # it will automatically start a new prompt
        if (LIMIT - p_length) < 10 and (LIMIT - p_length) >= 0:
            prompts.append(p)
            p = []

        # if the total length of prompt is > 500 it will take the last sentence
        # and start the next prompt with it
        elif p_length > LIMIT:

            old_line = p.pop(-1)
            prompts.append(p)
            p = [old_line]

    # join each prompt to one whole string and return list of prompts
    prompts = [" ".join(p) for p in prompts]

    for i, p in enumerate(prompts):
        if any(p.strip().startswith(s) for s in speakers):
            continue
        else:
            last_s = find_last_speaker(prompts[i - 1], speakers)

            prompts[i] = f"{last_s}: {p}"

    return prompts
