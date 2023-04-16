from Lila import config

import pyjokes
import requests
import json
import logging
import webbrowser


def get_xkcd():
    """
    Fetches the latest XKCD comic and opens it in a new browser tab.
    :return: None
    """
    # Fetch the latest XKCD comic URL
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    latest_comic_url = comic_data['img']

    # Open the latest XKCD comic in a new browser tab
    webbrowser.open_new_tab(latest_comic_url)


def get_headlines():
    url = (config.news_url + 'top-headlines?'
           'country=us&'
           'apiKey=' + config.news_api)
    news = requests.get(url).text
    news_dict = json.loads(news)
    articles = news_dict['articles']

    try:
        return articles
    except Exception as ex:
        logging.error("Error in get_news function: " + str(ex))
        return False


def parse_news(articles):
    output = ["Here are some of the stories you asked for: "]
    transitions = ["First we have", "Here is another story.", "Next we we have", "Also,", "Finally,"]
    try:
        for i, article in enumerate(articles):
            output.append(transitions[i])
            output.append(article['title'] + ". ")
            output.append("Here's a quick summary.")
            output.append(article['description'])
            if i >= 4:
                break
        return " ".join(output)
    except Exception as ex:
        logging.error("Error in parse_news function: " + str(ex))
        return False


def getNewsUrl():
    return config.news_url


def tell_joke():
    return pyjokes.get_joke()
