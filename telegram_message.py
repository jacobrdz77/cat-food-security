import dotenv
import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class CatSecurityBot:
    "CatSecurityBot is a Telegram bot that sends messages/photos to the user (defined by the MESSAGE_ID in .env)."

    def __init__(self, debug_enabled: bool = True,):
        """Initializes with bot key and user ID from environment variables. By default, it allows for debug logging."""
        load_dotenv()
        BOT_KEY = os.getenv("BOT_KEY")
        self.message_id = os.getenv("MESSAGE_ID")
        if not BOT_KEY or not self.message_id:
            raise ValueError("No Bot Key or Message ID found.")

        if debug_enabled:
            logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO)

        self.app = ApplicationBuilder().token(BOT_KEY).build()
        self.add_handlers()
        self.start_polling()

    def start_polling(self):
        try:
            print("Bot started polling...")
            self.app.run_polling()
        except Exception as e:
            print(f"Error starting polling: Exception Type({type(e).__name__}) {e}")
        finally:
            print("Stopped polling.")

    def add_handlers(self):
        """Adds all of the commands to the bot."""
        # Todo:
        # - Add send_cat_detected
        # - Add send_unkown_detected
        self.app.add_handler(CommandHandler("hello", self.hello_command))

    async def hello_command(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"Hello {update.effective_user.first_name}")


def main():
    bot = CatSecurityBot()

if __name__ == "__main__":
    main()
