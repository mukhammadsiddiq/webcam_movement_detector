import pandas as pd
import glob

# Initialize Excel writer
excel_writer = pd.ExcelWriter('dataset.xlsx', engine='xlsxwriter')

# Read CSV files and save each as a separate sheet in Excel
datasets = glob.glob("dataset_csv/*.csv")
for i, file in enumerate(datasets):
    df = pd.read_csv(file)
    sheet_name = f'Sheet_{i+1}'  # Create a unique sheet name
    df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
excel_writer.close()  # Save and close the Excel writer
