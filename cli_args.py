import argparse

# set up the argument parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--file",
    type=str,
    help="If this flag is present, it will select that file and parse it to the output file path sepcified with the output flag.",
)
parser.add_argument(
    "-d",
    "--directory",
    type=str,
    help="If this flag is present, it will select all the files in the specifed directory and output them to the specified directory.",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="output_files/default_output.csv",
    help="This is a required flag. Tell the program where to save output files.",
)
parser.add_argument(
    "-wl",
    "--wlimit",
    type=int,
    default=350,
    help="If not provided the default is 350 words. Please input a NUMBER(int) to limit the word count in each prompt",
)
parser.add_argument(
    "-p",
    "--prompt",
    type=str,
    help="This is where you specify the file path containing the prompt to the API call to give desired response",
)

args = parser.parse_args()