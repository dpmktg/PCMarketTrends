import requests
import re
import json

from collections import Counter
from datetime import date, datetime, timedelta

today = date.today()
f = '%b %d, %Y'
d1 = today.strftime("%d-%m-%Y")
d2 = datetime.strptime(today.strftime('%b %d, %Y'),f)

apiKey = ''

i = 0

print('Please enter the Steam appID of the game you would like to look up')

appID = int(input())

url = requests.get("https://steamcommunity.com/games/"+str(appID))

htmltext = url.text

groupID = htmltext.split("OpenGroupChat( '")[1].split("'")[0]

membersUrl = requests.get("https://steamcommunity.com/gid/"+str(groupID)+"/memberslistxml/?xml=1")

membersText = membersUrl.text

name = membersText.split('<groupName>')[1].split('</')[0]

pattern = '(?<=<steamID64>)(\d+)(?=<)'

regex = re.findall(pattern, membersText)

for user in regex:

    steamLibrary = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+str(apiKey)+"&steamid="+str(user)+"&format=json&include_appinfo=true")
    libraryText = steamLibrary.text
    gamePattern = '"name":"(.*?)"'
    gameRegex = re.findall(gamePattern, libraryText)

    for game in gameRegex:
        with open(name + d1 + "library.txt", "a") as file:
            file.write(game + "\n")
    
    
    print(i,"/ 1000")
    i += 1

with open(name + d1 + "library.txt", "r") as file:
    contents = file.readlines()

gameTitles = [title.strip() for title in contents]

gameCounts = Counter(gameTitles)

sortedGames = sorted(gameCounts.items(), key=lambda x: x[1], reverse=True)

uniqueGames = list(dict(sortedGames).keys())

print(name)

with open(name + d1 + "sorted.txt", "w") as file:
    for game, count in sortedGames:
        if game in uniqueGames:
            file.write(f"{game} ({count})\n")
            uniqueGames.remove(game)
