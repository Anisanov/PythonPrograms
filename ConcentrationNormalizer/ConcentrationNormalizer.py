# Alan Nisanov
# anisanov@berkeley.edu
# Description: Move BCA assay output Excel file into the ConcentrationNormalizer directory
# Once running the program will output volumes of buffer needed to dilute samples to the same specified concentration
# Dependencies: pandas, openpyxl

# Imports
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Reading ANY excel file in ConcetrationNormalizer Directory
file_list = glob.glob('*.xlsx')
for entry in file_list:
    df = pd.read_excel(entry)

# Slicing dataframe for BCA concentrations
BCA_matrix = df.iloc[[32,33,34,35,36,37,38,39],[1,2,3,4,5,6,7,8,9,10,11,12]]
BCA_matrix.columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
BCA_matrix.index = ["A", "B", "C", "D", "E", "F", "G", "H"]


# Calculating Average for each standard (Assuming standards are placed on first two columns)
BCA_matrix["Average"] = (BCA_matrix["1"] + BCA_matrix["2"]) / 2

# Calculating Average - Blank for Each standard (Assuming standard blanks are placed on H11 and H12)
AverageBlank = (BCA_matrix["11"]["H"] + BCA_matrix["12"]["H"]) / 2
BCA_matrix["Average - Blank"] = BCA_matrix["Average"] - AverageBlank

# Adding standard concentrations (ug/mL)
StandardConcentrations = np.array([2000, 1500, 1000, 750, 500, 250, 125, 25])

# Solving linear regression for standard curve
AvgMinusBlank = np.array(BCA_matrix["Average - Blank"].values).reshape((-1, 1))
#print(StandardConcentrations)
#print(AvgMinusBlank)
plt.scatter(AvgMinusBlank, StandardConcentrations)
plt.show()
model = LinearRegression().fit(AvgMinusBlank, StandardConcentrations)

print(model.coef_)
print(model.intercept_)
