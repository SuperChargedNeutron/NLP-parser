# NLP-Parser
A Python package that parses dialogue script to API acceptable inputs.

clone repo 
then `cd parser`

inside of the directory

run  `python nlp-parser.py [-f|-d,-o,-wl,-p]`

1) choose between file or directory mode, provide relative path to your choice
2) set the word count limit for each prompt with -wl or --wlimit, defaults to 350
3) Specify the prompt file path with --prompt or -p
4) if desired, name the output csv with --output or -o, provide relative path

Params\
--file or -f\
--directory or -d\
--wlimit or -wl\
--prompt or -p\
--output or -o

you can always ask for help in the command line by running
 `python nlp-parser.py --help`
