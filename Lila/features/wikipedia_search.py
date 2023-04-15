import wikipedia

def tell_me_about(topic):
    try:
        return wikipedia.summary(topic, sentences=3)
    except Exception as ex:
        print(ex)
        return False
