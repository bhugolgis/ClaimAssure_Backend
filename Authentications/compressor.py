

import pandas as pd

import os




input_file_path = "C:/Users/jafar.khan/Downloads/Images/"

output_file_path = "C:/Users/jafar.khan/Downloads/Images/"



excel_file_list = os.listdir(input_file_path)

df = pd.DataFrame()



#Run a for loop to loop through each file in the list

for excel_files in excel_file_list:
    if excel_files.endswith(".xls"):
        df1 = pd.read_excel(input_file_path+excel_files)
        df = df.append(df1)





df.to_excel(output_file_path+"Consolidated_file.xlsx")