# Imports
import requests
from datetime import datetime
import time
import csv

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


    # Opening CSV file in write mode
    file = open('CrowdData.csv', 'w', newline = '')

    # Writing to CSV
    with file:

        # Loop Over specified interval for a specified number of readings and recording data
        while done == False:
            date, datapoint = CrowdMeter()
            file.write(str(date))
            file.write(',')
            file.write(str(datapoint))
            file.write(',')
            time.sleep(interval)
            counter += 1
            if counter > (readings - 1):
                done = True



# Run(interval, readings)
MeterRecorder(900, 96)