import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import uvicorn

# Shared counter and lock for thread safety
flash_counter = 0
counter_lock = asyncio.Lock()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configure and manage Telegram bot lifecycle."""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN environment variable not set")

    application = (
        Application.builder()
        .token(bot_token)
        .build()
    )
    
    # Register handlers
    application.add_handler(CommandHandler("flash", flash_handler))
    
    # Start the bot in background
    await application.initialize()
    await application.start()
    
    # Set up webhook for production (comment out for polling)
    # await application.bot.set_webhook(f"https://your-domain.com/webhook/{bot_token}")
    
    # Start polling in background
    await application.updater.start_polling()
    
    yield
    
    # Cleanup
    await application.updater.stop()
    await application.stop()

app = FastAPI(lifespan=lifespan)

async def flash_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global flash_counter
    async with counter_lock:
        flash_counter += 1
    await update.message.reply_text("Flash counted! ⚡")

@app.get("/flashes")
async def get_flashes():
    """Endpoint to retrieve current flash count."""
    async with counter_lock:
        return JSONResponse(
            content={"num_flashes": flash_counter}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
