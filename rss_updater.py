import time
import signal
import sys

RSS_FILE = "mock_rss/mock.xml"
RSS_ITEM = "    <item>\n    <title>A cool Tatoeba sentence #1</title>\n    <link>https://tatoeba.org/en/sentences/show/8070858</link>\n    <description>A cool sentence in the Berber language.</description>\n    </item>\n\n"
RSS_HEADER = "<rss xmlns:atom=\"http://www.w3.org/2005/Atom\" version=\"2.0\">\n<channel>\n    <title>Mock XML Object</title>\n    <link>https://tatoeba.org/</link>\n    <description>A mock RSS feed for testing only.</description>\n    <atom:link href=\"https://www.rssboard.org/files/sample-rss-2.xml\" rel=\"self\" type=\"application/rss+xml\"/>\n    <item>\n"
RSS_FOOTER = "</channel>\n</rss>"

i = 0

def main():
    global i
    cur_write_position = len(RSS_HEADER) - 1


    with open(RSS_FILE, "w") as fh:
        fh.write(RSS_HEADER)

    while True:
        with open(RSS_FILE, "r+") as fh:
            fh.seek(cur_write_position)
            fh.write(RSS_ITEM + RSS_FOOTER)
            print("Wrote item!")
            cur_write_position += len(RSS_ITEM) + 3
        i += 1
        if i == 100:
            sys.exit()
        time.sleep(5)



if __name__ == "__main__":
    main()