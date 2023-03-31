# Shell Craft

[![PyPI version](https://img.shields.io/pypi/v/openai-shell-craft?color=green&label=PyPI)](https://pypi.org/project/openai-shell-craft/)

Generating shell commands and code using natural language models (OpenAI ChatGPT).

## Install using Pip

```sh
pip install openai-shell-craft
```

## Command Line Interface

All command line usage follows the following format:

```bash
shell-craft <request>
```

### Quick Start

```sh
shell-craft "tell me how long the system has been up for"
```

Returns:
```bash
uptime -p
```

## Prompt Types

Shell Craft supports many different `--prompt` options. We have organized them into categories here only to aid in reference usage.

| Category      | Name                                                                  | Argument Value    |
|---------------|-----------------------------------------------------------------------|-------------------|
| Language      | [Bash](https://www.gnu.org/software/bash/)                            | `bash`            |
| Language      | [PowerShell](https://learn.microsoft.com/en-us/powershell/)           | `powershell`      |
| Language      | [Python](https://www.python.org/)                                     | `python`          |
| Language      | [C](https://en.wikipedia.org/wiki/C_(programming_language))           | `c`               |
| Language      | [C#](https://learn.microsoft.com/en-us/dotnet/csharp/)                | `c_sharp`         |
| Language      | [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | `javascript`      |
| Language      | [Java](https://dev.java/)                                             | `java`            |
| Language      | [Go](https://go.dev/)                                                 | `go`              |
| Template      | Feature Request                                                       | `feature_request` |

When `--prompt` is not specified, Shell Craft will use `bash` unless PowerShell is used to call Shell Craft, then it uses `powershell`.

### Help Prompt

For additional help you can run:

```bash
shell-craft --help
```

### Bash Example

Executing:
```bash
shell-craft --prompt bash "find all swp files and delete them if theyre not in use"
```

Returns a Bash command:
```bash
find . -name '*.swp' -type f ! -exec fuser -s {} \; -delete
```

### Powershell Example

Executing:
```ps1
shell-craft --prompt powershell "remove all files older than 30 days"
```

Returns a PowerShell command:
```ps1
Get-ChildItem -Path "C:\your\path" -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Force
```

### Refactoring existing code
```bash
cat my_code.py | python -m shell_craft --prompt python --refactor
```

### Documenting existing code
```bash
cat my_code.py | python -m shell_craft --prompt python --document
```

### Generating tests for existing code
```bash
cat my_code.py | python -m shell_craft --prompt python --test
```

### Feature Request Example

Executing:
```sh
shell_craft --prompt feature_request "add an icon that shows the total test coverage"
```

Returns Markdown:
```markdown
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

## Language Models

Support for different [OpenAI models](https://platform.openai.com/docs/models).

Currently recommended `--model` options:
1. `gpt-3.5-turbo` (default)
2. `gpt-4`
3. `gpt-4-32k`
4. `code-davinci-002`
5. `text-davinci-003`

If `--model` is not specified, it will use `gpt-3.5-turbo` by default.

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

Create a file named `config.json`:
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
