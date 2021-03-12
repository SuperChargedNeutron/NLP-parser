# GPT3-Parser
A Python package that parses dialogue script to GPT-3 acceptable inputs.  You can clone the files into your machine by running
`git clone https://github.com/techcheese/GPT3-Parser.git`
then ` cd GPT3-Parser `

To use the tools, place the files you would to parse in a _known file path_.
The file will then out put some files which we can direct the output via the CLI.

Sample use:
*To parse a single file use flag --file or -f:
`python gptparser --file txt_file.docx --output output_files/parsed_file.txt`*
You can also shorten flags like so:
*`python gptparser -f txt_file.docx -o output_files/parsed_file.txt`*
*To parse an entire directory at once  with flags '--directory' or '-d':
**with shortened flags:
`python gptparser -d docs -o output_files/`
*To change the word count limit in the prompts use flag '--wlimit' or '-wl'
**`python gptparser -d docs -o output_files/ -wl 500`
