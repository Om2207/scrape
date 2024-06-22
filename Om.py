import re
import asyncio
from telethon import TelegramClient, events

# Your API ID and hash
API_ID = 26404724
API_HASH = 'c173ec37cd2a6190394a0ec7915e7d50'
PHONE_NUMBER = '+917739098908'  # Your phone number in international format
TARGET_CHAT_ID = -1002219374008  # Your target chat ID

# Keywords to filter messages
KEYWORDS = ["charged", "approved"]

# Fixed author name
FIXED_AUTHOR = "@rundilundlegamera"

# Set to keep track of processed CCs
processed_ccs = set()

# Function to extract data from the message
def extract_data(message_text: str) -> str:
    # Regular expressions to extract data
    cc_pattern = re.compile(r'(?:CC:|Cc:|Cc\s*:\s*|cc:|𝗖𝗮𝗿𝗱:|𝗖𝗮𝗿𝗱\s*:\s*|[ϟ]\s*Cc:|☀️⇾|•\s*sᴛᴀᴛᴜs⇾)\s*(\d{12,19}\|\d{1,2}\|\d{2,4}\|\d{3})')
    response_pattern = re.compile(r'(?:RESPONSE:|Response:|response:|Status:|status:|[ϟ]\s*Response:|𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞:|•\s*ʀᴇsᴘᴏɴsᴇ⇾)\s*(.*(Charged|Approved|approved|CHARGED|APPROVED|𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝|approved).*)')
    bin_pattern = re.compile(r'(?:BIN:|Bin:|bin:|Info:|info:|[ϟ]\s*BIN:|[ϟ]\s*Info:|𝗜𝗻𝗳𝗼:|𝗜𝗻𝗳𝗼\s*:\s*|•\s*ʙɪɴ⇾)\s*(.*)')
    bank_pattern = re.compile(r'(?:BANK:|Bank:|bank:|Issuer:|issuer:|[ϟ]\s*BANK:|[ϟ]\s*Issuer:|𝐈𝐬𝐬𝐮𝐞𝐫:|•\s*ʙᴀɴᴋ⇾)\s*(.*)')
    country_pattern = re.compile(r'(?:COUNTRY:|Country:|country:|[ϟ]\s*Country:|𝐂𝐨𝐮𝐧𝐭𝐫𝐲:|𝐂𝐨𝐮𝐧𝐭𝐫𝐲\s*:\s*|•\s*ᴄᴏᴜɴᴛʀʏ⇾)\s*(.*)')

    cc_match = cc_pattern.search(message_text)
    response_match = response_pattern.search(message_text)
    bin_match = bin_pattern.search(message_text)
    bank_match = bank_pattern.search(message_text)
    country_match = country_pattern.search(message_text)

    # Create a formatted message with the extracted data
    if cc_match and response_match and bin_match and bank_match and country_match:
        extracted_data = (
            f"𝙓𝙔𝙋𝙃𝙄𝘾「𝗫𝗬」\n"
            f"═ ═ ═ ═ ═\n"
            f"𝘾𝙖𝙧𝙙: {cc_match.group(1)}\n"
            f"𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚: {response_match.group(1)}\n"
            f"═ ═ ═ ═ ═\n"
            f"𝘽𝙞𝙣 𝙄𝙣𝙛𝙤: {bin_match.group(1)}\n"
            f"𝘽𝙖𝙣𝙠: {bank_match.group(1)}\n"
            f"𝘾𝙤𝙪𝙣𝙩𝙧𝙮: {country_match.group(1)}\n"
            f"═ ═ ═ ═ ═\n"
            f"𝘼𝙪𝙩𝙝𝙤𝙧 ↯ {FIXED_AUTHOR}"
        )
        return extracted_data, cc_match.group(1)
    return None, None

# Initialize the client
client = TelegramClient('session_name', API_ID, API_HASH)

# Define the event handler
@client.on(events.NewMessage)
async def handler(event):
    message_text = event.message.message
    if message_text:
        message_text_lower = message_text.lower()
        if any(keyword in message_text_lower for keyword in KEYWORDS):
            extracted_data, cc_number = extract_data(message_text)
            if extracted_data and cc_number not in processed_ccs:
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
