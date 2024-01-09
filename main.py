from pyrogram import Client, filters
import httpx
import base64

# Create a new Telegram bot using BotFather and replace the token below
bot = Client("my_bot", api_id=3845818, api_hash="95937bcf6bc0938f263fc7ad96959c6d", bot_token="6869978658:AAFnveEPtkB5HiBG3nkjwsgyZiLCJhNw0Ec")
username = "SchMaister"
password = "Sqaq DCUW YqR0 lWTe 0vVp iVzt"

# Encode the username and password in base64 format
credentials_b64 = base64.b64encode(f"{username}:{password}".encode()).decode()

# Set up the request with the Authorization header
url = "https://your-api-endpoint-url.com"
headers = {
    "Authorization": f"Basic {credentials_b64}",
    "Content-Type": "application/json"  # or any other content type as per your API
}

async def search_anime(query):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{url}/wp-json/wp/v2/search", params={"search": query}, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error: {response.status_code}")
            return None

# Define a command handler to handle user search queries
@bot.on_message(filters.command("search"))
async def handle_search(bot, message):
    # Get the user query from the message
    query = message.text.split(" ", 1)[1]
    
    # Fetch the content from the URL using the query
    result = await search_anime(query)
    
    # Create a list of titles with hyperlinks
    titles = [f'<a href="{item["url"]}">{item["title"]}</a>' for item in result]
    
    # Join the titles list with line breaks and send the result to the user
    result_text = "\n\n".join(titles)
    await bot.send_message(chat_id=message.chat.id, text=result_text, parse_mode="HTML")

# Start the bot
bot.run()
