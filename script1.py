import asyncio
#import nest_asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext

# Apply nest_asyncio to allow running the bot in Jupyter or other nested asyncio environments
#nest_asyncio.apply()

# Bot token
#TOKEN = "7660007316:AAHis4NuPllVzH-7zsYhXGfgokiBxm_Tml0"

# Channel ID (replace with your actual channel ID)
CHANNEL_ID = "-1002400575005"  # You can also use the numeric version of the channel ID

# Define the asynchronous function that handles incoming media messages
async def handle_media(update: Update, context: CallbackContext) -> None:
    thumb = None
    media = None

    # Check the type of media and handle accordingly
    if update.message.video:
        media = update.message.video
        thumb = media.thumb  # Get the thumbnail of the video
    elif update.message.photo:
        # Use the highest resolution photo (last item in the list)
        media = update.message.photo[-1]
        thumb = media.thumb  # Photos don't have a 'thumb', this is just an empty check
    elif update.message.document:
        media = update.message.document
        thumb = media.thumb  # Documents might have a thumbnail (e.g., PDFs)
    elif update.message.sticker:
        media = update.message.sticker
        thumb = media.thumb  # Stickers might have a thumbnail (preview)
    elif update.message.animation:
        media = update.message.animation
        thumb = media.thumb  # GIFs also might have a thumbnail
    elif update.message.audio:
        media = update.message.audio
        thumb = media.thumb  # Audio may have a thumbnail (cover image)
    else:
        thumb = None

    if thumb:
        # Download the thumbnail if available
        file = await context.bot.get_file(thumb.file_id)
        file_path = "thumbnail.jpg"  # Save the file as thumbnail.jpg
        await file.download_to_drive(file_path)
        
        # Send the thumbnail to the user
        await update.message.reply_photo(photo=open(file_path, 'rb'))
    else:
        await update.message.reply_text("No thumbnail or preview available for this media.")
    
    # Forward the message to the channel
    await update.message.forward(chat_id=CHANNEL_ID)

# Define the start command handler
async def start(update: Update, context: CallbackContext) -> None:
    # Send a welcome message when the user starts the bot
    await update.message.reply_text("Hello! 👋 I'm your media bot. Send me any gif, sticker, photo, video, audio, or document, and I’ll fetch its thumbnail or preview for you! Let’s get started! 🚀")
