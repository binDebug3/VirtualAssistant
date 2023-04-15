import webbrowser
import re
from urllib import parse, request


domain = input("Enter the video name:")
video = parse.urlencode({'search_query': domain})
print("Video:", video)

result = request.urlopen("http://www.youtube.com/results?" + video)
search_results = re.findall(r'href=\"\/watch\?v=(.{4})', result.read().decode())
print(search_results)

url = "http://www.youtube.com/watch?v="+str(search_results)
webbrowser.open_new(url)
