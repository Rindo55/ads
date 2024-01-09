from pyrogram import Client, filters
from requests_html import HTMLSession

# Create a new Telegram bot using BotFather and replace the token below
bot = Client("my_bot", api_id=3845818, api_hash="95937bcf6bc0938f263fc7ad96959c6d", bot_token="6869978658:AAFnveEPtkB5HiBG3nkjwsgyZiLCJhNw0Ec")
# Define a function to fetch content from the given URL and return the result
def search_anime(query):
    session = HTMLSession()
    url = f"https://anidl.org/wp-json/wp/v2/search?search={query}"
    response = session.get(url)
    response.html.render()
    result = response.json()
    session.close()
    return result

# Define a command handler to handle user search queries
@bot.on_message(filters.command("search"))
def handle_search(bot, message):
    # Get the user query from the message
    query = message.text.split(" ", 1)[1]
    
    # Fetch the content from the URL using the query
    result = search_anime(query)
    
    # Create a list of titles with hyperlinks
    titles = []
    for item in result:
        title = item["title"]
        url = item["url"]
        hyperlink = f'<a href="{url}">{title}</a>'
        titles.append(hyperlink)
    
    # Join the titles list with line breaks and send the result to the user
    result_text = "\n".join(titles)
    bot.send_message(chat_id=message.chat.id, text=result_text, parse_mode="HTML")

# Start the bot
bot.run()
