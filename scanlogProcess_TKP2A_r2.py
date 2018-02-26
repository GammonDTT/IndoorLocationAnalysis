import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


# Styles
plt.style.use("ggplot")


# Import into dataframes
rawLogdf = pd.read_csv("C:/Users/jeremiahto/OneDrive/Gammon/Innovation/Digital Transformation/Project/20170901 Indoor Positioning/LabourTracking/20171215 Trial at TKP2A/scanlog/20180220CPR.csv",
                       header=0,
                       index_col=1)
# RPI006df = pd.read_csv("C:/Users/jeremiahto/OneDrive/Gammon/Innovation/Digital Transformation/Project/20170901 Indoor Positioning/LabourTracking/IndoorPositioningRecords/scanlog_0000000007e30f08.csv", names=["project", "scannerId", "datetime", "beaconAddr", "beaconRssi"], index_col=2)
rawLogdf.index = pd.to_datetime(rawLogdf.index, dayfirst=True)
rawLogdf = rawLogdf.sort_index()
rawLogdf.head()


# Parameters
scannerList = ["0000000092c5c041", "00000000db73dcea", "0000000007e30f08"]  #RPI-001,005,006
scannerThresRev = [-100, -100, -100]
startTime = pd.to_timedelta("00:00:00")  # To be adjusted if required
tolerance = pd.to_timedelta("00:00:21")  # The series of reading will still be considered as one continuous unit if the gap between reading does not exceed this value

rmCount = 0  # Initialise room count to zero at starttime
cprContent = []  # Chiller Plant Room (cpr)
startDate = pd.to_datetime(input("Please provide the start date: [yyyy-mm-dd] ")) + startTime
endDate = pd.to_datetime(input("Please provide the end date: [yyyy-mm-dd] ")) + pd.to_timedelta("1 day") + startTime



def countAsContinuous(beaconAddr, tolerance, uniqTime, cprContent, timenow):
    # Check if the data should be counted as one continuous reading
    rvIndexLast = None
    cprContentRv = cprContent[::-1]
    for i in range(len(cprContentRv)):
        if beaconAddr in cprContentRv[i]:
            rvIndexLast = i
            break
    if rvIndexLast == None:
        return False
    else:
        timeLastAppear = uniqTime[len(cprContent)-rvIndexLast-1]
        #print("timenow = {}".format(timenow))  # Debugging only
        #print("timeLastAppear = {}".format(timeLastAppear))  # Debugging only
        if timenow - timeLastAppear > tolerance:
            return False
        else:
            return True


# Filter beacons
Logdf = rawLogdf[rawLogdf.beaconAddr.isin(["f9:79:bd:be:99:bf", "c8:03:83:4f:aa:42"])]  # Only for filtering certain beacons, not required in production
Logdf = Logdf[startDate:endDate]

'''
row
[0] datetime
[1] id
[2] project
[3] scannerId
[4] beaconRssi
[5] beaconAddr
'''

uniqTime = sorted(list(set(Logdf.index)))
uniqAddrGate = []


for i in range(len(uniqTime)):  # Reading at the gate at all the recorded times in the dataframe
    nowLogdf = Logdf[Logdf.index == uniqTime[i]]
    nowUniqAddrGate = list(set(nowLogdf.beaconAddr))
    uniqAddrGate.append(nowUniqAddrGate)
    if len(cprContent) < 1:
        cprContent.append(nowUniqAddrGate)
    else:
        for beaconAddr in nowUniqAddrGate:
            if not countAsContinuous(beaconAddr = beaconAddr, tolerance = tolerance, uniqTime = uniqTime, cprContent = cprContent, timenow = uniqTime[i]):
                cprContent.append(cprContent[-1][:])
                if beaconAddr in cprContent[-1]:
                    cprContent[-1].remove(beaconAddr)
                else:
                    cprContent[-1].append(beaconAddr)
                #print(cprContent)

cprContentCount = []
for i in range(len(cprContent)):
    cprContentCount.append(len(cprContent[i]))

summarydf = pd.DataFrame({"Gate Reading": uniqAddrGate,
                         "Beacons in Room": cprContent,
                         "Room Beacon Count": cprContentCount}, index = uniqTime)
summarydf.to_csv("C:\\Users\\jeremiahto\\OneDrive\\Gammon\\Innovation\\Digital Transformation\\Project\\20170901 Indoor Positioning\\LabourTracking\\20171215 Trial at TKP2A\\scanlog\\20180221\\summarydf.csv")
summarydf.plot.bar()
plt.show()

