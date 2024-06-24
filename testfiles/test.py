from requests import get, Session
from requests_file import FileAdapter
from rss_parser import RSSParser

rss_url = "file:///Users/matth/Coding/Python/rss_telegram_bot/mock_rss/mock.xml"
session = Session()
session.mount("file://", FileAdapter())
response = session.get(rss_url)

rss = RSSParser.parse(response.text)

# Print out rss meta data
print("Language", rss.channel.language)
print("RSS", rss.version)

# Iteratively print feed items
for item in rss.channel.items:
    print(item.title)
    print(item.description[:50])