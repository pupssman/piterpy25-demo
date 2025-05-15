from fastapi import FastAPI
from contextlib import asynccontextmanager
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import uvicorn
from fastapi.responses import JSONResponse
import os

# Shared counter and lock for thread safety
flash_counter = 0
import asyncio
counter_lock = asyncio.Lock()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start telegram bot polling
    bot_token = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("flash", flash_handler))
    await application.initialize()
    await application.start()
    yield
    await application.stop()

app = FastAPI(lifespan=lifespan)

async def flash_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global flash_counter
    async with counter_lock:
        flash_counter += 1
    await update.message.reply_text("Flash counted! ⚡")

@app.get("/flashes")
async def get_flashes():
    async with counter_lock:
        return JSONResponse(content={"num_flashes": flash_counter})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
