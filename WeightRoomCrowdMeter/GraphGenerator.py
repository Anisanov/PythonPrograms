# Imports
from time import strptime
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import matplotlib.dates

# Reading data from CrowdData.csv
RawData = []
with open('CrowdData.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        for x in row:
            RawData.append(x.split(','))

# Parsing Raw Data
strDates = RawData[:-1:2]
strDatapoints = RawData[1::2]

dates = []
datapoints = []
for x in strDates:
    dates.append(datetime.strptime(''.join(x), '%Y-%m-%d %H:%M:%S.%f'))


for x in strDatapoints:
    datapoints.append(int(''.join(x)))
    

# Generation of Graph
plt.style.use('seaborn-white')
plt.xlabel('Time')
plt.ylabel('People at the Gym')
plt.title('People at UCB Gym vs Time')
plt.gcf().autofmt_xdate()
plt.plot(dates, datapoints)
plt.savefig('CrowdMeterGraph.png')