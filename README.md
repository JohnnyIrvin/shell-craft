# Shell Craft

[![PyPI version](https://img.shields.io/pypi/v/openai-shell-craft?color=green&label=PyPI)](https://pypi.org/project/openai-shell-craft/) [![codecov](https://codecov.io/gh/JohnnyIrvin/shell-craft/branch/trunk/graph/badge.svg?token=MKYZOJR8SQ)](https://codecov.io/gh/JohnnyIrvin/shell-craft)

Generating shell commands and code using natural language models (OpenAI ChatGPT). 

Shell Craft can:

1. Generate shell commands from natural language requests.
2. Write code in a dozen languages from natural language requests.
3. Refactor existing code.
4. Document existing code.
5. Generate tests for existing code.
6. Generate issue tickets and feature requests for GitHub, GitLab, and BitBucket.

Our goal is to 10x developer productivity by combining the power of natural language models with the power of the command line.

## Installation

See the [Wiki](https://github.com/JohnnyIrvin/shell-craft/wiki) for installation instructions.

* [Pip Installation](https://github.com/JohnnyIrvin/shell-craft/wiki/Install-via-Pip)
* [Docker Installation](https://github.com/JohnnyIrvin/shell-craft/wiki/Install-via-Docker)

## Command Line Interface

Shell Craft often follows the format of:

```bash
shell-craft --prompt <type> <request>
```

You can use the following command to get started:

```bash
shell-craft --help
```

See the [Wiki](https://github.com/JohnnyIrvin/shell-craft/wiki) for additional command line usage instructions.

See [Prompt Types](https://github.com/JohnnyIrvin/shell-craft/wiki/Different-Prompt-Options) for a guide to the different `--prompt` options.

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

Shell Craft uses the OpenAI API to generate the shell commands, requiring an API key to give it access to an account with OpenAI.

_Warning! **API keys are sensitive information** and should be kept confidential. Don't share your API key with anyone who shouldn't have access to it. Failure to do so may result in charges on your OpenAI account. Shell Craft never transmits this key to any service other than the official OpenAI API. **Your API key** is **your responsibility**._

To obtain an API key from the OpenAI platform, follow these steps:

1. Go to https://platform.openai.com/account/api-keys in your web browser.
2. Log in to your OpenAI account or create a new account if you don't have one.
3. Click the "Create new secret key" button.
4. Copy the key that is generated for you.

Once you have your API key, you **must** pass it to Shell Craft via **one** of the following methods.

### Option 1 (Recommended) - Configuration file:

shell-craft looks for a configuration file in the following places, in order:
  - the current directory, named config.json
  - the file named by $SHELLCRAFT_CONFIG
  - $XDG_CONFIG_HOME/shell-craft/config.json
  - $HOME/.config/shell-craft/config.json

The contents are simple json:
```
{
    "openai_api_key": "<your secret key>"
}
```

Now, Shell Craft will know your API key in order to run future prompts without having to specify it or ensure it exists in the environmental variables.

### Option 2 - Command Line Argument:

```bash
shell-craft "list all files in directory" --api-key API_KEY
```

Where `API_KEY` is your OpenAI API key.

### Option 3 - Environment Variable:

```bash
export OPENAI_API_KEY=<your secret key>
shell-craft "list all files in directory"
```

Where `<your secret key>` is your OpenAI API key.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Acknowledgments contain a few of the people who have helped the project along the way.

* [OpenAI](https://openai.com/) for their language models and API.
* [Joel Fourhman](https://github.com/joelfourhman) for the initial idea, the challenge, and the project name.
* [Chase Montgomery](https://github.com/BLuFeNiX) for testing, feedback, and estimated time savings vs manual implementation.
* [Bryan Gonzalez](https://www.linkedin.com/in/bryan-gonzalez-2b86ba67/) for powershell feedback and merge reviews.
* [Aaron Croissette](https://www.linkedin.com/in/acrois/) for business use case feedback, documentation, and a lovely PyPi icon on the readme.
