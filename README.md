# Shell Craft

Project for generating shell commands using OpenAI models.

## How to install

1. `pip install shell-craft`
2. Create a file called `config.json` and put your OpenAI API key in it. (See below)

or

1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. `pip install .`
4. Create a file called `config.json` and put your OpenAI API key in it. (See below)


## How to use
`shell-craft <win:optional> <description>` - This will generate a shell command for you based on the description you provide. If you provide the `win` argument, it will generate a powershell command. Otherwise, it will generate a bash command.

Example
```
shell-craft This command will print the current date and time
date
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

Acknowledgments contain a few of the people who have helped the project along the way.

* [OpenAI](https://openai.com/) for their language models and API.
* [Joel Fourhman](https://github.com/joelfourhman) for the initial idea, the challenge, and the project name.
* [Chase Montgomery](https://github.com/BLuFeNiX) for testing, feedback, and estimated time savings vs manual implementation.
* [Bryan Gonzalez](https://www.linkedin.com/in/bryan-gonzalez-2b86ba67/) for powershell feedback and merge reviews.
* [Aaron Croissette](https://www.linkedin.com/in/acrois/) for business use case feedback and a lovely PyPi icon on the readme.