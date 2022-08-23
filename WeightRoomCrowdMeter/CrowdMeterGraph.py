# Imports
import requests
from datetime import datetime
import time
import matplotlib.pyplot as plt

# Defining CrowdMeter function
def CrowdMeter():

    # Time
    my_date = datetime.now()
    my_date_iso = datetime.utcnow().isoformat()


    # Request
    url = 'https://api.density.io/v2/spaces/spc_863128347956216317/count'
    headers = {'authorization' : 'Bearer shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e'}
    x = requests.get(url, params={'time': my_date_iso}, headers=headers)

    # Parsing Request for Crowd Data
    count = x.text.split(':')
    people = int(count[1].replace("}",""))
    return my_date,people

# Defining Function to Record Crowd Data
def MeterRecorder(interval, readings):

    # Time and Number of people Variables
    done = False
    counter = 0
    dates = []
    datapoints = []

    # Loop Over specified interval for a specified number of readings
    while done == False:
        date, datapoint = CrowdMeter()
        datapoints.append(datapoint)
        dates.append(date)
        time.sleep(interval)
        counter += 1
        if counter > (readings - 1):
            done = True

    # Generation of Graph
    plt.style.use('seaborn-white')
    plt.xlabel('Time')
    plt.ylabel('People at the Gym')
    plt.title('People at UCB Gym vs Time')
    plt.plot(dates, datapoints)
    plt.savefig('CrowdMeterGraph.png')

# Run(interval, readings)
MeterRecorder(5, 3)