import os, sys, io, re
import pprint, argparse

# 3rd party import

# local imports
from func import make_prompts
from cli_args import args

# decide between file flow and directory flow
if args.file:
    f_path = os.path.normpath(args.file)
    prompts = make_prompts(f_path, args.wlimit)
    with open(os.path.normpath(args.output), 'wb') as f1:
        for i, p in enumerate(prompts):
            f1.write(f"Header:\n")
            f1.write(p)
            f1.write("\n\n")

elif args.directory:
    print(args.directory)
    print(args.output)
