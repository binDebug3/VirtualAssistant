import webbrowser

def website_opener(domain):
    try:
        url = "https://www." + domain
        webbrowser.open(url)
        return True
    except Exception as ex:
        print(ex)
        return False