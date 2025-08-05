import dotenv
import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError

class CatSecurityBot:
    "CatSecurityBot is a Telegram bot that sends messages/photos to the user (defined by the MESSAGE_ID in .env)."

    def __init__(self, debug_enabled: bool = True,):
        """Initializes with bot key and user ID from environment variables. By default, it allows debug logging."""
        load_dotenv()
        BOT_KEY = os.getenv("BOT_KEY")
        self.message_id = os.getenv("MESSAGE_ID")
        if not BOT_KEY or not self.message_id:
            raise ValueError("No Bot Key or Message ID found. Make sure they are defined in the .env file.")

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

    async def shutdown(self):
        try:
            await self.app.shutdown()
        except Exception as e:
            print(f"Unkown error in stop_polling: Exception Type({type(e).__name__}) {e}")
        finally:
            print("Manually stopped polling.")

    def add_handlers(self):
        """Adds all of the commands to the bot."""
        self.app.add_handler(CommandHandler("hello", self.hello_command))

    async def hello_command(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        """Example Hello command for bot."""
        await update.message.reply_text(f"Hello {update.effective_user.first_name}")

    async def send_image(self, image_path: str, message: str):
        """Sends image using the image_path provided. (Parse Mode is MarkdownV2)"""
        try:
            with open(image_path, "rb") as image:
                await self.app.bot.send_photo(
                    chat_id=self.message_id,
                    photo=image,
                    caption=message,
                    parse_mode="MarkdownV2"
                )
            print("Sent image successfully!")
        except TelegramError as e:
            print(f"Telegram error when sending image: {e}")
        except Exception as e:
            print(f"Unexpected error sending image: {e}")


def main():
    bot = CatSecurityBot()

if __name__ == "__main__":
    main()
