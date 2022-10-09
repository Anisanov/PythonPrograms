# Alan Nisanov
# anisanov@berkeley.edu
# Description: Move BCA assay output Excel file into the ConcentrationNormalizer directory
# Once running the program will output volumes of buffer needed to dilute samples to the same specified concentration
# Dependencies: pandas, openpyxl, sklearn

# Imports
import pandas as pd
import glob
import numpy as np
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

# Solving linear regression for standard curve
AvgMinusBlank = np.array(BCA_matrix["Average - Blank"].values).reshape((-1, 1))
StandardConcentrations = np.array([2000, 1500, 1000, 750, 500, 250, 125, 25])
model = LinearRegression().fit(AvgMinusBlank, StandardConcentrations)
slope = float(model.coef_)
intercept = float(model.intercept_)

# Deleting uneeded columns in BCA matrix
BCA_matrix = BCA_matrix.drop(['Average'], axis=1)
BCA_matrix = BCA_matrix.drop(['Average - Blank'], axis=1)

# Converting absorbances to concentrations using the standard curve
concentration_matrix = (slope * BCA_matrix) + intercept

# User input for dilution
dilution = float(input("Specify dilution for final solution (eg, 5x dilution input '5'): \n"))
Dconcentration_matrix = dilution * concentration_matrix

# User input for final mass
mass = float(input("\nSpecify micrograms for final solution (eg, 80 ug input '80')\n"))
Mconcentration_matrix = (mass / Dconcentration_matrix) * 1000

# User input for final volume
volume = float(input("\nSpecify a volume in uL for final solution (eg, 60 uL ug input '60')\n\n"))
Vconcentration_matrix = volume - Mconcentration_matrix

# Adding Labels to each sample from excel file
Label_Matrix = df.iloc[[32,33,34,35,36,37,38,39],[14,15,16,17,18,19,20,21,22,23,24,25]]
Label_Matrix.columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
Label_Matrix.index = ["A", "B", "C", "D", "E", "F", "G", "H"]
Label_Matrix = Label_Matrix.replace(np.nan, "-")

# Iterating over each cell of Label dataframe to record indicies for samples
ii = []
jj = []
labels = []
for i in range(Label_Matrix.shape[0]): # iterate over rows
    for j in range(Label_Matrix.shape[1]): # iterate over columns
        label = Label_Matrix.iat[i, j] # get cell value
        if label == '-':
            continue
        else:
            ii.append(i)
            jj.append(j)
            labels.append(label)

# Slicing concentration matricies to display uL of sample needed and uL of PBS needed
sampleVols = []
PBSVols = []
for (i, j) in zip(ii, jj):
    sampleVol = Mconcentration_matrix.iat[i, j]
    PBSVol = Vconcentration_matrix.iat[i, j]
    sampleVols.append(sampleVol)
    PBSVols.append(PBSVol)
output = pd.DataFrame(list(zip(labels, sampleVols, PBSVols)), columns=['Sample', 'uL of Sample', 'uL of PBS'])

# Averaging duplicate samples
output = output.groupby('Sample').mean().reset_index()
output = output.set_index('Sample')

# Displaying Output
print(output)