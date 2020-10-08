import requests
import csv
import sys
import time

# start timer
tic = time.perf_counter()

# initialise lists
decimal = []
byte_list = []

# accept output file from cmd argument
file_name = sys.argv[1]
# accept scoreboard code from cmd argument
shared_secret = sys.argv[2]

# fetch csv from scoreboard
r = requests.get(url="**************" + shared_secret)

# decode contents
scsv = r.content.decode("utf-8")
# split into rows
temp = scsv.splitlines()
# open contents with csv reader
csv = csv.reader(temp)
# put csv into array
array = [row for row in csv]

# loop through array and put scores into decimal
for row in reversed(array[1:]):
    for cell in row[0:150]:
        decimal.append(int(cell))


## DECODE

for number in decimal:
    # convert back to binary
    # this comes out as a string because, python
    binary = format(number, '032b')
    # split out each byte
    # python list indexing is not inclusive
    byte_0 = binary[0:8]
    byte_1 = binary[8:16]
    byte_2 = binary[16:24]
    byte_3 = binary[24:32]
    # append bytes to the list
    try:
        #convert 'strings' back to ints again
        byte_list.append(int(byte_0, 2))
        byte_list.append(int(byte_1, 2))
        byte_list.append(int(byte_2, 2))
        byte_list.append(int(byte_3, 2))
    except:
        # if something goes wrong, still recover the binary
        byte_list.append(byte_0)
        byte_list.append(byte_1)
        byte_list.append(byte_2)
        byte_list.append(byte_3)

# convert ints to bytes
out = bytes(byte_list)
# open output file
try:
    file_out = open(file_name, 'wb')
except:
    sys.exit("Error creating output file")
# write bytes to file
file_out.write(out)
try:
    # decode bytes to text
    print(out.decode('utf-8'))
except:
    # unless it's not text, then say so
    print("Doesn't look like a text file...")

# stop timer
toc = time.perf_counter()
workTime = str(round((toc - tic), 2))

# print completion message
print("Done! Decoded " + str(len(out)) + " bytes in " + workTime + "seconds.")
