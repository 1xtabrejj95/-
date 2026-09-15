import os
import re
import telebot
import requests

# ═══════════════════════════════════════════════════════════
# 🔥 YAHAN APNA BOT TOKEN DAALO (BotFather se milega)
# ═══════════════════════════════════════════════════════════
BOT_TOKEN = "8720844045:AAGtw1KGzaSnq6MGAQs-tlNJMCLz6hlROqA"

# ═══════════════════════════════════════════════════════════
# 🔥 API CONFIG (Yeh mat badalna)
# ═══════════════════════════════════════════════════════════
API_KEY = "9X0M-TN8Z-G7BV-PO9O"
API_BASE = "https://nitin-devloper-apis.ajayboy3027.workers.dev/api"

# 🔥 Validate token
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
    print("❌ BOT_TOKEN set nahi kiya! Upar line mein daalo.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)


# ═══════════════════════════════════════════════════════════
# 🔥 START
# ═══════════════════════════════════════════════════════════
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name or "User"
    
    text = f"""
╭──────────────────────────────────────╮
│      🔍  𝐕ɪʟʟᴀɪɴ 𝐗 𝐍ᴜɴ 𝐈ɴꜰᴏ 𝐁ᴏᴛ             │
│      📡  Number Intelligence Bot     │
╰──────────────────────────────────────╯

👋 Welcome, {user_name}!

📌 Send any 10-digit mobile number
   → Get Name, Address, Circle

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Example: 9876543210

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢 Updates: @iamvillainx
⚡ Developed by @iamvillainx
    """
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


# ═══════════════════════════════════════════════════════════
# 🔥 NUMBER LOOKUP
# ═══════════════════════════════════════════════════════════
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    try:
        text = message.text.strip() if message.text else ""
        
        # 🔥 Extract 10-digit number
        numbers = re.findall(r'\b[6-9]\d{9}\b', text)
        
        if not numbers:
            bot.reply_to(message, "❌ *Send a valid 10-digit number*", parse_mode='Markdown')
            return
        
        number = numbers[0]
        
        # 🔥 Loading
        loading = bot.reply_to(message, "🔍 *Searching...*", parse_mode='Markdown')
        
        # 🔥 API Call
        api_url = f"{API_BASE}?key={API_KEY}&action=num&number={number}"
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        if not data.get("status"):
            bot.edit_message_text("❌ *Number not found*",
                                 chat_id=message.chat.id,
                                 message_id=loading.message_id,
                                 parse_mode='Markdown')
            return
        
        results = data.get("result", [])
        if not results:
            bot.edit_message_text("❌ *No data found*",
                                 chat_id=message.chat.id,
                                 message_id=loading.message_id,
                                 parse_mode='Markdown')
            return
        
        # 🔥 Format output
        output = "╭──────────────────────────────────────╮\n"
        output += "│      🔍  NUMBER LOOKUP RESULT        │\n"
        output += "╰──────────────────────────────────────╯\n\n"
        output += f"📱 *Number:* `{number}`\n\n"
        
        for i, item in enumerate(results[:3], 1):
            output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            output += f"📋 *Result #{i}*\n\n"
            output += f"👤 *Name:* {item.get('NAME', 'N/A')}\n"
            output += f"🏠 *Address:* {item.get('ADDRESS', 'N/A')}\n"
            output += f"📡 *Circle:* {item.get('circle', 'N/A')}\n"
            output += f"👨 *Father:* {item.get('fname', 'N/A')}\n"
            if item.get('alt'):
                output += f"📞 *Alt:* {item.get('alt')}\n"
            if item.get('email'):
                output += f"📧 *Email:* {item.get('email')}\n"
            if item.get('aadhar'):
                output += f"🆔 *Aadhar:* {item.get('aadhar')}\n"
            output += "\n"
        
        output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        output += "⚡ *Developed by* @iamvillainx"
        
        bot.edit_message_text(output,
                             chat_id=message.chat.id,
                             message_id=loading.message_id,
                             parse_mode='Markdown')
    
    except Exception as e:
        bot.reply_to(message, f"❌ *Error:* `{str(e)}`", parse_mode='Markdown')


# ═══════════════════════════════════════════════════════════
# 🔥 BOT START
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🚀 FREE INFO OSINT Bot Started...")
    bot.polling(non_stop=True)
