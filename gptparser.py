import os, sys, io, re

import pprint

# 3rd party import

# local imports
from func import get_prompt_length, find_speakers, find_last_speaker


def make_prompts(txt_file, LIMIT=500):
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

        # if the sentence is within 10 words of the 500 limit
        # it will automatically start a new prompt
        if (LIMIT - get_prompt_length(p)) < 10 and (LIMIT - get_prompt_length(p)) >= 0:
            prompts.append(p)
            p = []

        # if the total length of prompt is > 500 it will take the last sentence
        # and start the next prompt with it
        elif get_prompt_length(p) > LIMIT:

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


if __name__ == "__main__":

    tim_path = os.path.join("docs", "timferris-harryfinkelstein.txt")
    elon_path = os.path.join("docs", "joerogan_elonmusk.txt")
    american_path = os.path.join("docs", "american_life533.txt")

    prompts = make_prompts(tim_path, LIMIT=350)

    elon = make_prompts(elon_path, LIMIT=350)

    am = make_prompts(american_path, LIMIT=350)

    with open("output_files/parsed_tim_harry.txt", "w") as f1:
        for i, p in enumerate(prompts):
            f1.write(f"Prompt {i}:\n\n")
            f1.write(p)
    with open("output_files/parsed_joe_elon.txt", "w") as f2:
        for i, p in enumerate(elon):
            f2.write(f"Prompt {i}:\n\n")
            f2.write(p)
            f2.write("\n\n\n")
    with open("output_files/parsed_americanlife.txt", "w") as f3:
        for i, p in enumerate(am):
            f3.write(f"Prompt {i}:\n\n")
            f3.write(p)
