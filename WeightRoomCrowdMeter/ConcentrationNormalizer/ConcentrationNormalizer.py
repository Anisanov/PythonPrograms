# Imports
import pandas as pd

# Reading BCA output Excel File
filename = input('Input Excel File name below: \n')
df = pd.read_excel(filename)
print(df)