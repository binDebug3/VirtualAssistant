import wikipedia
import wolframalpha
from Lila import config, interface

def tell_me_about(topic):
    try:
        return wikipedia.summary(topic, sentences=3)
    except Exception as ex:
        print(ex)
        return False

def compute_math(question):
    try:
        client = wolframalpha.Client(config.wolframalpha_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except Exception as ex:
        print(ex)
        interface.output("Sorry sir I couldn't solve that problem. Please try again.", "error")
        return None
