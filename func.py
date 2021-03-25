import os, sys, datetime, io
import re, operator

# 3rd party import
import numpy as np

# local imports
from cli_args import args

## utils
sentence_flatten = lambda t: [word for item in t for word in item.split(" ")]
flatten = lambda t: [item for sublist in t for item in sublist]
parsed_file_name = (
    lambda x: f"parsed_{x.lower().replace(' ', '-').replace('.docx', '.txt')}"
)
unique = lambda list1: np.unique(np.array(list1))

def write_output_file(fragments, file_name=""):
    """
    turn parsed fragments into readable text files

    input is parsed paragraphs from the text

    does not return anything
    """
    ## read in prompt from txt file

    if not os.path.exists("parsed_docs"):
        os.mkdir("parsed_docs")

# i have the program placing the prompt then a newline then the text fragment
    if file_name == "":
        with open(os.path.join(parsed_file_name(args.file)), "w") as f1:
            for f in fragments:
                f1.write(f)
                f1.write("\n\n\n\n")
    else:
        file_name = file_name.split("""\\""")[-1]
        with open(os.path.join(parsed_file_name(file_name)), "w") as f1:
            for f in fragments:
                f1.write(f)
                f1.write("\n\n\n\n")


def write_response_csv(responses):
    """
    Inputs the responses from GPT3 into a spreadsheet

    Where each file makes up one column, and each cell below
    represents the response for each fragment

    does not return anything
    """
    if os.path.exists(args.output):
        with open(os.path.normpath(args.output), "a") as out_file:
            writer = csv.writer(out_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(responses)
    else:
        os.makedirs("/".join(args.output.split("/")[:-1]))

        with open(os.path.normpath(args.output), "w+") as out_file:
            writer = csv.writer(out_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(responses)


def api_requests(fragments):
    """
    This function takes a list of parsed documents
    The whole list is one file

    Returns a list of all response texts in the same order as the
        parsed file
    """
    responses = []

    for f in fragments:
        resp = openai.Completion.create(engine="davinci", prompt=f, max_tokens=100)
        responses.append(resp["choices"][0]["text"])

    return responses


def get_fragment_length(p):
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
    gen_pattern = r"(\n[A-z]+(\n|:)?\s?(([A-Z][A-z]+)?)(\n+|:))"

    strr = " ".join(sentence_flatten(lines))

    gen_matches = [x[0].strip() for x in list(re.findall(gen_pattern, strr))]

    return list(unique(gen_matches))


def find_last_speaker(fragment, speakers):
    """
    Take in the fragment that is being cut off and find the last speaker in the paragraph

    Takes in the fragment itself and a list of speakers

    Returns the last speaker that shoes up in the fragment
    """
    speak_dict = {}
    for s in speakers:
        if s in fragment:
            speak_dict[s] = fragment.rfind(s)

    return max(speak_dict.items(), key=operator.itemgetter(1))[0]


def parse_file(txt="", txt_file="", LIMIT=350):
    """
    function takes in a file and a word limit for each fragments

    file: file of .txt format
    parses by sentences and count words by seperating
    the text in each space character.
    """
    if txt == "":
        # read transcript from file
        with io.open(txt_file, "r", encoding="utf-8") as fil:
            timestamp_regex = re.compile(r"[0-9]+:[0-9]+:?[0-9]+", flags=re.IGNORECASE)
            lines = fil.read().replace("\ufeff", "")

            lines = timestamp_regex.sub("", lines).split(".")
    # .repalce('\n') does GTP3 have some sort of preference with newlines?

    elif txt_file == "":
        lines = str(txt).replace("\ufeff", "").split(".")

    speakers = find_speakers(lines)

    # # initialize empty variables to be used in the loop
    fragments = []
    p = []

    for l in lines:

        # add the new sentence
        l = f"{l}."
        p.append(l)
        p_length = get_fragment_length(p)

        # if the sentence is within 10 words of the 500 limit
        # it will automatically start a new fragment
        if (LIMIT - p_length) < 10 and (LIMIT - p_length) >= 0:
            fragments.append(p)
            p = []

        # if the total length of fragment is > 500 it will take the last sentence
        # and start the next fragment with it
        elif p_length > LIMIT:

            old_line = p.pop(-1)
            fragments.append(p)
            p = [old_line]

    # join each fragment to one whole string and return list of fragments
    fragments = [" ".join(p) for p in fragments]

    for i, p in enumerate(fragments):
        if any(p.strip().startswith(s) for s in speakers):
            continue
        else:
            try:
                last_s = find_last_speaker(fragments[i - 1], speakers)

                fragments[i] = f"{last_s} {p}"
            except:
                fragments[i] = p

    with open(os.path.normpath(args.prompt), 'r') as in_file:
        prompt = in_file.read()