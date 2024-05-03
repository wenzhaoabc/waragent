from src.agents.tools import ReadWebPage


def test_read_web_page():
    web_page = ReadWebPage('https://www.britannica.com/event/World-War-II/Forces-and-resources-of-the-European-combatants-1939')
    url = web_page.url
    print(web_page.run(url, ""))


if __name__ == '__main__':
    test_read_web_page()
