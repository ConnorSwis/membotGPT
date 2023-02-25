# MemBot-GPT

MemBot is a Discord bot that uses OpenAI's GPT-2 model to generate responses based on prompts provided by users. The bot is designed to help users with their Membean vocabulary homework, reminding them to do three 15-minute sessions per week.

## Getting Started

To use MemBot, you will need to have a Discord account and create a new Discord application with a bot user. You will also need to sign up for an OpenAI API key.

### Prerequisites

- Python 3.x
- Discord account
- OpenAI API key

### Installing

1. Clone the repository: `git clone https://github.com/<your-username>/membot.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and replace `DISCORD_TOKEN` and `OPENAI_API_KEY` with your own values.

### Usage

To run MemBot, run the following command in your terminal:

```
python main.py
```

You can then use the `prompt` command to create a new thread and generate a response based on a provided prompt. For example:

```
??prompt How many minutes do I need to train for membean this week?
```

MemBot will open a thread and you and others will be able to talk with MemBot with previous message knowledge.

You can also configure the bot to send reminder messages to a specified Discord channel at a certain time by changing the value of `CHANNEL_ID` in the `.env` file.

## Contributing

If you would like to contribute to MemBot, please open a new pull request or issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
