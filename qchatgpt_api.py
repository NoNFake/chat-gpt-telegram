import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from io import StringIO
import sys
import os
import random
import time
import webbrowser
from typing import Dict, Optional
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents.tools import Tool
from langchain.llms import OpenAI


class PythonREPL:
    """Simulates a standalone Python REPL."""

    def __init__(self):
        pass        

    def run(self, command: str) -> str:
        """Run command and returns anything printed."""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, globals())
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = str(e)
        return output


llm = OpenAI(temperature=0.1, openai_api_key="Your Token")
python_repl = Tool(
    "Python REPL",
    PythonREPL().run,
    "A Python shell. Use this to execute python commands. Input should be a valid python command. If you expect output it should be printed out.",
)
tools = [python_repl]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a Python REPL bot. Send me a Python command to execute.")


def help(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me a Python command to execute.")


def yurii(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello Yurii!")


def echo(update: telegram.Update, context: telegram.ext.CallbackContext):
    message = update.message
    if message.document:
        file = message.document.get_file()
        file.download()
        context.bot.send_message(chat_id=message.chat_id, text="File received!")
        context.bot.send_document(chat_id=message.chat_id, document=file)
    else:
        command = message.text
        if command.lower() in ["what is your name?", "what's your name?", "what your name?", "your name?", ""]:
            context.bot.send_message(chat_id=message.chat_id, text="My name is Yurii")
        elif "Yurii" in command:
            yurii(update, context)
        else:
            output = agent.run(command)
            context.bot.send_message(chat_id=message.chat_id, text=output)


def autowrite(update, context):
    message = update.message
    group_id = message.chat.id
    context.bot.send_message(chat_id=group_id, text="Hello")
    for i in range(50):
        context.bot.send_message(chat_id=group_id, text="Hello from the bot!")


def main():
    updater = Updater(token='your_token_here', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('open_website', open_website))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.group, autowrite))
    updater.start_polling()
    updater.idle()

bot = telegram.Bot(token='Telegram Token')

updates = bot.get_updates()

for update in updates:
    user_id = update.message.chat_id
    bot.send_message(chat_id=user_id, text="Hello from the bot!")
    
    # Sleep for a short time to avoid rate limiting
    time.sleep(0.1)

def main():
    updater = Updater(token='Telegram Token', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('open_website', open_website))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

def open_website(update, context):
    url = "https://www.example.com"
    dispatcher = updater.dispatcher
    webbrowser.open(url)
    dispatcher.add_handler(CommandHandler('open_website', open_website))

if __name__ == '__main__':
    main()
def my_function():
    pass