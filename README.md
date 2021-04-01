# NLP-Parser

A Python package that parses dialogue script to API acceptable inputs. It is written to serve as cli tool. 

### What this package does

Sometimes API have limitations. In this case, we were face with word count limitation. It is a smart API so it can't be parsed exactly by word count. 
This tool parses your text files (.docx/.txt) by sentences into many "paragraphs" that are within the APIs limitation.

The prompt and footer flag allow you to customize these paragraphs with prefix and suffix sentences.

#### Example of a parsed paragraph with a prompt and footer:

>This a sample prompt sentence, I came from a txt file.
>>......text from file within word count limits.........
>>
>This a sample footer sentence, I also came from txt file.
>

The program will do this until it runs out of words. It also does not account for the word in the prompt and footer. Those are added afterwards.
The paragraphs are then added sequentially to a .txt file in the `parsed_files` directory. 
This tool is also ready to save the outputs of the API to a csv file in the `output` directory

## Installation

clone repo 
then `cd parser`

It is a lightweight tool, requirements.txt has them al. You won't be needing the openAI module since that part has been disabled. 

`pip install docx2txt numpy`

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
---footer or -fo\
--output or -o

you can always ask for help in the command line by running
 `python nlp-parser.py --help`
