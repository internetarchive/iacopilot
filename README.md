# IA Copilot

Summarize and ask questions about items in the Internet Archive (and other textual resources) via GPT of OpenAI.

Install IACopilot CLI tool:

```
$ pip install iacopilot
```

To run this tool, you will need [API key from OpenAI](https://platform.openai.com/account/api-keys) and set it as an environment variable.

```
$ OPENAI_API_KEY="<APIKEY>" iacopilot
Enter quit   to quit/exit this REPL prompt
Enter help   to print the help message
Press <TAB>  to see available commands
IACopilot 0:0 ?> 
```

```
IACopilot 0:0 ?> help
 help/h/?                    Print this help message
 quit/exit/q                 Exit the REPL prompt
 ls                          List all the loaded contexts
 load <URL>                  Detect source and load the data as a context
 load ia <ITEM>              Load an IA item as a context
 load tv <CHANNEL> [<DATE>]  Load transcript of a TV channel as a context
 load wbm <URL> [<DATE>]     Load a Wayback Machine capture as a context
 load wiki <TITLE> [<LANG>]  Load a Wiki page as a context
 load file <PATH>            Load a loal file or directory as a context
 cd [<ID>]                   Change a loaded context to query
 rm [<ID>]                   Remove current or specified context
 reset                       Remove all contexts and reset statistics
 config openai [<KEY>]       Get or set configuration options
 <PROMPT>                    Ask the copilot questions about the context
 ! <CMD>                     Run a system command
IACopilot 0:0 ?> quit
Exiting...
$
```

Interact with the REPL!

Alternatively, run in Docker as following:

```
$ docker image build -t iacopilot .

$ docker container run --rm -it -e OPENAI_API_KEY="<APIKEY>" iacopilot
Enter quit   to quit/exit this REPL prompt
Enter help   to print the help message
Press <TAB>  to see available commands
IACopilot 0:0 ?>
```
