import os, sys, io, re, glob
import pprint, argparse

# 3rd party import
import docx2txt

# local imports
from func import make_prompts, write_output_file
from cli_args import args
from openai_api import openai

def process_doc_file(input_file_path):
    """
    this functions input is a file path FOR A .DOCX file.
    The function runs the necessary functions to 
    parse the files, make the API calls, and output the 
    parsed result to a text file and output the API response 
    to a csv file.
    """
    txt = docx2txt.process(os.path.normpath(input_file_path))

    # get parsed fragments from file and print text to out put file
    fragments = parse_file(txt=txt, LIMIT=args.wlimit)
    write_output_file(fragments, file_name=input_file_path)

    print(f'{input_file_path} is parsed. Sending API calls...\n')
    gpt_responses = api_requests(fragments)
    write_response_csv([input_file_path] + gpt_responses)
    
def process_txt_file(input_file_path):
    """
    this functions input is a file path FOR A .TXT file.
    The function runs the necessary functions to 
    parse the files, make the API calls, and output the 
    parsed result to a text file and output the API response 
    to a csv file.
    """
    # get parsed fragments from file and print text to out put file
    fragments = parse_file(txt_file=os.path.normpath(args.file), LIMIT=args.wlimit)
    write_output_file(fragments, file_name=input_file_path)

    print(f'{input_file_path} is parsed. Sending API calls...\n')
    gpt_responses = api_requests(fragments)
    write_response_csv([input_file_path] + gpt_responses)

if __name__ == "__main__":
    # decide between file flow and directory flow
    if args.file:
        if ".doc" in args.file:
            process_doc_file(args.file)

        elif ".txt" in args.file:
            process_txt_file(args.file)

    elif args.directory:

        for file_name in glob.iglob(f"{args.directory}/*"):
            if ".doc" in file_name:
                process_doc_file(file_name)
                
            elif ".txt" in file_name:
                process_txt_file(file_name)