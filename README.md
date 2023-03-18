# Shell Craft

[![PyPI version](https://img.shields.io/pypi/v/openai-shell-craft?color=green&label=PyPI)](https://pypi.org/project/openai-shell-craft/)

Project for generating shell commands using OpenAI models.

## How to install

1. `pip install openai-shell-craft`
2. Create a file called `config.json` and put your OpenAI API key in it. (See below)

## Command Line Interface

All command line usage follows the following format:

```shell
shell-craft <prompt type> <human request>
```

Shell Craft supports many prompt types, such as:
* Bash
* Powershell

Bash Example
```bash
shell_craft bash find all swp files and delete them if theyre not in use
find . -name '*.swp' -type f ! -exec fuser -s {} \; -delete
```

Powershell Example
```bash
$ shell_craft powershell remove all files older than 30 days
Get-ChildItem -Path "C:\your\path" -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Force
```

## Python API

The following example shows how to use Shell Craft inside of your own Python code. The example loads your api key from an environment variable, uses the Bash prompt, and gets input from the user.

```python
import os

from shell_craft import Service
from shell_craft.prompts import BASH_PROMPT

Server(
    api_key = os.environ.get("OPENAI_API_KEY"),
    prompt = BASH_PROMPT,
).query(
    message = input("Enter your request: ")
)
```

## Configuration file

config.json
```
{
    "openai_api_key": "<your secret key>"
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* [OpenAI](https://openai.com/) for their language models and API.
* [Joel Fourhman](https://github.com/joelfourhman) for the initial idea, the challenge, and the project name.
* [Chase Montgomery](https://github.com/BLuFeNiX) for testing, feedback, and estimated time savings vs manual implementation.
