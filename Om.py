import re
import asyncio
from telethon import TelegramClient, events
import requests

# Your API ID and hash
API_ID = 26404724
API_HASH = 'c173ec37cd2a6190394a0ec7915e7d50'
PHONE_NUMBER = '+10000000'  # Your phone number in international format
TARGET_CHAT_ID = -1002160767030  # Your target chat ID

# Keywords to filter messages
KEYWORDS = ["charged", "approved"]

# Fixed author name
FIXED_AUTHOR = "@rundilundlegamera"

# Set to keep track of processed CCs
processed_ccs = set()

# Function to extract data from the message
def extract_data(text):
    regex = r'\b(\d{15,16})[/| -]+(\d{1,2})[/| -]+(\d{2,4})[/| -]+(\d{3,4})\b'
    matches = re.findall(regex, text)
    if not matches:
        return []

    # Format each credit card detail
    formatted_cc = []
    for match in matches:
        cc_number, month, year, cvv = match
        formatted_month = month.zfill(2)
        formatted_year = '20' + year if len(year) == 2 else year
        formatted_cc.append(f"{cc_number}|{formatted_month}|{formatted_year}|{cvv}")

    return formatted_cc

def bincheck(bin):
    url = f"https://api.dlyar-dev.tk/info-bin?bin={bin}"
    res = requests.get(url).json()
    if res["status"] == True:
        try:
            return {
                "bin": res.get("bin", "N/A"),
                "country": res.get("country", "N/A"),
                "flag": res.get("flag", "N/A"),
                "type": res.get("type", "N/A"),
                "brand": res.get("brand", "N/A"),
                "bank": res.get("bank", "N/A"),
                "scheme": res.get("scheme", "N/A")
            }
        except Exception as e:
            return None
    else:
        return None

def vbv_status(bin):
    url = f"https://api.adwadev.com/api/vbvapi.php?bin={bin}"
    res = requests.get(url).json()
    if "status" in res and "response" in res:
        return res["status"], res["response"]
    else:
        return "N/A", "N/A"

def format(cardd):
    card_parts = cardd.split('|')
    bin = card_parts[0][:6]
    bin_lookup = bincheck(bin)
    vbv_stat, vbv_resp = vbv_status(bin)
    
    if bin_lookup:
        bin = bin_lookup.get("bin", "N/A")
        country = bin_lookup.get("country", "N/A")
        flag = bin_lookup.get("flag", "N/A")
        type = bin_lookup.get("type", "N/A")
        brand = bin_lookup.get("brand", "N/A")
        bank = bin_lookup.get("bank", "N/A")
        scheme = bin_lookup.get("scheme", "N/A")
    else:
        bin = country = flag = type = brand = bank = scheme = "N/A"

    extracted_data = (
        f"⏤͟͞𝙊𝗠 「𝗫𝗬」\n"
        f"═ ═ ═ ═ ═\n"
        f"𝘾𝙖𝙧𝙙: {cardd}\n"
        f"𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚: Approved ✅\n"
        f"═ ═ ═ ═ ═\n"
        f"𝘽𝙞𝙣 𝙄𝙣𝙛𝙤: {scheme} - {type} - {brand}\n"
        f"𝘽𝙖𝙣𝙠: {bank}\n"
        f"𝘾𝙤𝙪𝙣𝙩𝙧𝙮: {country}\n"
        f"═ ═ ═ ═ ═\n"
        f"𝙑𝘽𝙑 𝙎𝙩𝙖𝙩𝙪𝙨: {vbv_stat}\n"
        f"𝙑𝘽𝙑 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚: {vbv_resp}\n"
        f"═ ═ ═ ═ ═\n"
        f"𝘼𝙪𝙩𝙝𝙤𝙧 ↯ {FIXED_AUTHOR}"
    )
    return extracted_data

# Initialize the client
client = TelegramClient('session_name', API_ID, API_HASH)

# Define the event handler
@client.on(events.NewMessage)
async def handler(event):
    message_text = event.message.message
    if message_text:
        message_text_lower = message_text.lower()
        if any(keyword in message_text_lower for keyword in KEYWORDS):
            cc_numbers = extract_data(message_text)
            for cc_number in cc_numbers:
                if cc_number not in processed_ccs:
                    extracted_data = format(cc_number)
                    if extracted_data:
                        # Add the CC number to the set of processed CCs
                        processed_ccs.add(cc_number)
                        # Send the extracted data to the target chat ID
                        await client.send_message(TARGET_CHAT_ID, extracted_data)
                        await asyncio.sleep(2)  # Wait for 2 seconds

async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Client Created")
    # Run the client until disconnected
    await client.run_until_disconnected()

# Start the client
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
