# Shell Craft

Project for generating shell commands using OpenAI models.

## How to install

1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Smile, life is good.

## How to use

1. Create a file called `config.json` and put your OpenAI API key in it.

Example
```
{
    "openai_api_key": "<your secret key>"
}
```

2. Run `chmod +x ai.py` to make the script executable.
3. Run `./ai.py <description of command to create>`

Example
```
./ai.py This command will print the current date and time
date
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
