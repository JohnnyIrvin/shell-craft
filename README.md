# Shell Craft

[![PyPI version](https://img.shields.io/pypi/v/openai-shell-craft?color=green&label=PyPI)](https://pypi.org/project/openai-shell-craft/)

Project for generating shell commands using OpenAI models.

## How to install

1. `pip install openai-shell-craft`

## Command Line Interface

All command line usage follows the following format:

```bash
$ shell-craft <human request>
```

By default, Shell Craft will atempt to determine the prompt type based on the current shell (Powershell or Bash).

```bash

Shell Craft supports many prompt types, such as:
* Bash
* Powershell
* Feature Request

For additional help you can run:

```bash
$ shell-craft --help
```

### Bash Example

```bash
$ shell-craft --prompt bash "find all swp files and delete them if theyre not in use"
find . -name '*.swp' -type f ! -exec fuser -s {} \; -delete
```

### Powershell Example
```bash
$ shell-craft --prompt powershell "remove all files older than 30 days"
Get-ChildItem -Path "C:\your\path" -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Force
```

### Feature Request Example

```bash
$ shell_craft --prompt feature_request "add an icon that shows the total test coverage"
---

name: Add Total Test Coverage Icon
about: Add an icon that shows the total test coverage
labels: Enhancement

---

**Is your feature request related to a problem? Please describe.**
There is currently no easy way to visualize the total test coverage for a project.

**Describe the solution you'd like**
I would like to have an icon on the project dashboard that, when clicked, displays the total test coverage for the project. This will allow developers to easily monitor and improve the overall test coverage for the project.

**Describe alternatives you've considered**
As an alternative, I have considered adding the total test coverage to the project README file. However, this solution would not be as easily accessible as an icon on the project dashboard.
```

## Python API

The following example shows how to use Shell Craft inside of your own Python code. The example loads your api key from an environment variable, uses the Bash prompt, and gets input from the user.

```python
import os

from shell_craft import Service
from shell_craft.prompts import BASH_PROMPT

Service(
    api_key = os.environ.get("OPENAI_API_KEY"),
    prompt = BASH_PROMPT,
).query(
    message = input("Enter your request: ")
)
```

## API Key
To obtain an API key from the OpenAI platform, follow these steps:

Go to https://platform.openai.com/account/api-keys in your web browser.

Log in to your OpenAI account or create a new account if you don't have one.

Click the "Create new secret key" button.

Copy the key that is generated for you.

Decide how you want to use the key:

Note that API keys are sensitive information and should be kept confidential. Make sure you don't share your API key with anyone who shouldn't have access to it.
Shell Craft uses the OpenAI API to generate the shell commands. You will need to create an account with OpenAI and get an API key. Once you have your API key, you can pass it to Shell Craft via command line argument, environment variable, or config file.

Option 1: Command Line Argument:
```bash
shell_craft prompt_type "human_request" --api-key API_KEY
```

Where prompt_type is the type of prompt you want to use, such as bash, powershell, or feature_request. human_request is the human readable request you want to convert to a shell command. API_KEY is your OpenAI API key.

Option 2: Environment Variable:
```bash
export OPENAI_API_KEY=<your secret key>
shell_craft bash "list all files in directory"
```

Option 3 (Recommended): Configuration file - config.json:
```
{
    "openai_api_key": "<your secret key>"
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Acknowledgments contain a few of the people who have helped the project along the way.

* [OpenAI](https://openai.com/) for their language models and API.
* [Joel Fourhman](https://github.com/joelfourhman) for the initial idea, the challenge, and the project name.
* [Chase Montgomery](https://github.com/BLuFeNiX) for testing, feedback, and estimated time savings vs manual implementation.
* [Bryan Gonzalez](https://www.linkedin.com/in/bryan-gonzalez-2b86ba67/) for powershell feedback and merge reviews.
* [Aaron Croissette](https://www.linkedin.com/in/acrois/) for business use case feedback and a lovely PyPi icon on the readme.
