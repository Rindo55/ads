
from pyrogram import Client, filters, enums
import requests
import base64

# Create a new Telegram bot using BotFather and replace the token below
bot = Client("my_bot", api_id=3845818, api_hash="95937bcf6bc0938f263fc7ad96959c6d", bot_token="6869978658:AAFnveEPtkB5HiBG3nkjwsgyZiLCJhNw0Ec")
username = "SchMaister"
password = "Sqaq DCUW YqR0 lWTe 0vVp iVzt"

# Encode the username and password in base64 format
credentials = f"{username}:{password}"
credentials_b64 = base64.b64encode(credentials.encode()).decode()

# Set up the request with the Authorization header
url = "https://your-api-endpoint-url.com"
headers = {
    "Authorization": f"Basic {credentials_b64}",
    "Content-Type": "application/json"  # or any other content type as per your API
}
def search_anime(query):
    
    url = f"https://anidl.org/wp-json/wp/v2/search?search={query}&per_page=50"
    response = requests.get(url, headers=headers)
    print(response.text)
    if response.ok:
        try:
            result = response.json()
            return result
        except ValueError:
            print("Invalid JSON")
    else:
        print("Response not OK")

# Define a command handler to handle user search queries
@bot.on_message(filters.text)
def handle_search(bot, update):
    # Get the user query from the message
    query = update.text
    if query.startswith("/"):
        bot.send_message(chat_id=update.chat.id, text="Just send an anime/manga title & I will search over AniDL.org and send you the post links.")
    # Fetch the content from the URL using the query
    else:
        result = search_anime(query)
        titles = []
        count = 0
        for item in result:
            title = item["title"]
            url = item["url"]
            count+=1
            hyperlink = f'<a href="{url}"><b>🔗 {title}</b></a>'
            titles.append(hyperlink)
        result_text = "\n\n".join(titles)
        bot.send_message(chat_id=update.chat.id, text=f"""Found <b>{count}</b> results for "<b>{query}</b>"\n\n{result_text}""", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)

# Start the bot
bot.run()
