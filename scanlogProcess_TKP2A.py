import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Styles
plt.style.use("ggplot")


# Import into dataframes
# TODO crawl through the folder, add RPI-001
RPI005df = pd.read_csv("C:/Users/jeremiahto/OneDrive/Gammon/Innovation/Digital Transformation/Project/20170901 Indoor Positioning/LabourTracking/IndoorPositioningRecords/scanlog_00000000db73dcea.csv", names=["project", "scannerId", "datetime", "beaconAddr", "beaconRssi"], index_col=2)
RPI006df = pd.read_csv("C:/Users/jeremiahto/OneDrive/Gammon/Innovation/Digital Transformation/Project/20170901 Indoor Positioning/LabourTracking/IndoorPositioningRecords/scanlog_0000000007e30f08.csv", names=["project", "scannerId", "datetime", "beaconAddr", "beaconRssi"], index_col=2)
combscandf = RPI005df.append(RPI006df).sort_index()  # TODO add RPI001df
# print(combscandf["2018-02-05":"2018-02-06"])


# Parameters
scannerList = ["0000000092c5c041", "00000000db73dcea", "0000000007e30f08"]  #RPI-001,005,006
scannerThresRev = [-70, -70, -70]

starttime = "00:00:00"
startDate = pd.to_datetime(input("Please select start date [yyyy-mm-dd] for plot: ")) + pd.to_timedelta(starttime)
endDate = pd.to_datetime(input("Please select end date [yyyy-mm-dd] for plot: ")) + pd.to_timedelta("1 day") + pd.to_timedelta(starttime)
tolerance = pd.to_timedelta("00:00:21")  # The series of reading will still be considered as one continuous unit if the gap between reading does not exceed this value

rmCount = 0  # Initialise room count to zero at starttime
uniqTime = []
cprContent = []  # Chiller Plant Room (cpr)
cprContentCount = []


def countAsContinuous(beaconAddr, tolerance, uniqTime, cprContent, timenow):
    # TODO what if beaconAddr is not in cprContent?
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
        if timenow - timeLastAppear > tolerance:
            return False
        else:
            return True

# datetime, project, scannerId, beaconAddr, beaconRssi
for row in combscandf[startDate:endDate].itertuples():  # TODO How to rule out case when there is a reading on the negative gate going out  - ignore negative gates for now
    if row[4] >= scannerThresRev[scannerList.index(row[2])]:
        if len(uniqTime) < 1:
            # if scannerPolarity[scannerList.index(row[2])]:
            uniqTime.append(row[0])
            cprContent.append([row[3]])
        elif row[0] == uniqTime[-1]: # TODO continuous single scan, continuous but one missing
            if row[3] not in cprContent[-1]:
                cprContent[-1].append(row[3])
            else:  # TODO and not countAsContinuous:
                cprContent[-1].remove(row[3])
        else:  # if continuous
            uniqTime.append(row[0])
            cprContent.append(cprContent[-1])
            if row [3] not in cprContent[-1]:  # TODO and not countAsContinuous:
                cprContent[-1].append(row[3])
            else:  # TODO and not countAsContinuous:
                cprContent[-1].remove(row[3])

for row in cprContent:
    cprContentCount.append(len(row))

outputdf = pd.DataFrame({"dateTime": uniqTime,
                        "beaconPresent": cprContent,
                        "beaconCount": cprContentCount})

outputdf.set_index("dateTime")

# print(RPI005df["2018-02-05":"2018-02-06"])
# print(RPI006df["2018-02-05":"2018-02-06"])

# RPI005df.plot()
# plt.show()
