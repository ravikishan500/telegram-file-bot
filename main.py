import logging
from pyrogram import Client, filters
from pyrogram.types import Message

logging.basicConfig(level=logging.INFO)

API_ID = 39238534                     
API_HASH = "bc0e02158c6a9d32dd4a0a1a803c55e9" 
BOT_TOKEN = "8971123464:AAED6HfKvADj2IFn7tn_5lpK2rCMbGTkMlI"
CHANNEL_ID = -1004458161660           

bot = Client("FileStoreBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    if len(message.command) > 1:
        file_msg_id = int(message.command[1])
        try:
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=file_msg_id
            )
        except Exception as e:
            await message.reply_text(f"❌ Error: File nahi mili.\nDetails: {e}")
    else:
        await message.reply_text("👋 Hello! Mujhe koi bhi file send karein, main bina kisi command ke uska permanent shareable link de dunga.")

@bot.on_message((filters.document | filters.video | filters.audio | filters.photo) & filters.private)
async def automatic_file_to_link(client: Client, message: Message):
    status_msg = await message.reply_text("⏳ Aapki file ko store kiya ja raha hai...")
    
    try:
        stored_msg = await message.copy(chat_id=CHANNEL_ID)
        file_unique_id = stored_msg.id
        
        me = await client.get_me()
        bot_username = me.username
        
        shareable_link = f"https://t.me{bot_username}?start={file_unique_id}"
        
        await status_msg.edit_text(
            f"✅ **Aapki file ka permanent link taiyar hai!**\n\n"
            f"🔗 Link:\n`{shareable_link}`",
            disable_web_page_preview=True
        )
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: Check karein ki bot channel me Admin hai ya nahi.\nDetails: {e}")

if __name__ == "__main__":
    print("⚡ Aapka File Storage Bot active ho chuka hai...")
    bot.run()
  
