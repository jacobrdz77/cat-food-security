import dotenv
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging


load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
MESSAGE_ID = os.getenv("MESSAGE_ID")

class Bot:
    def __init__(self, debug_enabled=True):
        self.app = ApplicationBuilder().token(BOT_KEY).build()

        hello_handler = CommandHandler("hello", hello)
        self.app.add_handler(hello_handler)
        self.app.run_polling()

        if debug_enabled:
            logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO
            )

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def main():
    print("Starting...")
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    app = ApplicationBuilder().token(BOT_KEY).build()

    hello_handler = CommandHandler("hello", hello)
    app.add_handler(hello_handler)
    
    app.run_polling()


if __name__ == "__main__":
    main()
