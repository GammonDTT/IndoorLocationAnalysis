import time
import datetime
import re

## MESSAGE TO BE SENT

# Data to be sent
scannerId = "001"
now = int(time.time())  # Integer i.e. correct to number of seconds
beaconAddr = "c8:03:83:4f:aa:42"
beaconAddr12 = "".join(beaconAddr.split(":"))  # Remove the ":"
beaconRssi =-100
beaconRssi3 = "{:03d}".format(abs(beaconRssi))  # Removed negative sign, force 3 chars

# sendMsg format: 3 chars of scannerId, "&<", 10 chars of timestamp (seconds from epoch), 12 chars of beaconAddr12, 3 chars of beaconRssi, ">&"
sendMsg = scannerId + "&<" + str(now) + beaconAddr12 + beaconRssi3 + ">&"
print(sendMsg)
print(len(sendMsg))


## MESSAGE TO BE RECEIVED AND PARSED
# Define Regex
msgRegex = re.compile(r'^(\d{3})&<(\d{10})(\w{12})(\d{3})>&$')
regexMatch = msgRegex.search(sendMsg)

# Reassemble data
projectNum = "J3628"
scannerId_ = regexMatch.group(1)
now_ = datetime.datetime.fromtimestamp(int(regexMatch.group(2)))

beaconAddr_ = str()
for i in range(6):
    beaconAddr_ += regexMatch.group(3)[2*i:2*i+2]
    beaconAddr_ += ":"

beaconRssi_ = int(regexMatch.group(4))*-1

msgReceived = {"project": projectNum,
               "scannerId": scannerId_,
                "datetime": str(now_),
                "beaconAddr": beaconAddr_,
                "beaconRssi": beaconRssi_}

print(msgReceived)