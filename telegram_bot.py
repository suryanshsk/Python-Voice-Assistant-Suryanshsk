from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text('Hello! I am your bot. Send me any message and I will echo it back!')

async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the received message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    app = ApplicationBuilder().token("YOUR_API").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

if __name__ == '__main__':
    main()
