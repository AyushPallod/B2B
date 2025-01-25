import pandas as pd

with open("C:/Users/Lenovo/Desktop/location.txt", 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

# Ensure the file has at least two lines
if len(lines) >= 2:
    # Extract the locations from the lines and replace '\' with '/'
    gst = lines[0].strip().replace('\\', '/')
    office = lines[1].strip().replace('\\', '/')
    
# Load the Excel file
# gst_file_path = "C:/Users/Lenovo/Downloads/122024_36ABSPP3929L1ZU_GSTR2B_21012025 (1).xlsx" # Replace with your file path
gst_file_path = gst
sheet_name = "B2B"  # Replace with the name of the sheet you want to import
gst_df = pd.read_excel(gst_file_path , sheet_name=sheet_name)

#gst no = Goods and Services Tax - GSTR-2B
#name = Unnamed: 1
#date = Unnamed: 4
#value = Unnamed: 5


# office_file_path = "C:/Users/Lenovo/Downloads/purchase (1).xls"  # Replace with your file path
office_file_path = office
sheet_name = "Sheet1"  # Replace with the name of the sheet you want to import
office_df = pd.read_excel(office_file_path, sheet_name=sheet_name)

#gst no = GSTIN
#name = Name
#date = InvoiceDate
#value = Payrupees

gst_df = gst_df[['Goods and Services Tax  - GSTR-2B' , 'Unnamed: 1' , 'Unnamed: 4' , 'Unnamed: 5']]
gst_df.rename(columns={'Goods and Services Tax  - GSTR-2B': 'GSTIN', 'Unnamed: 1': 'Name', 'Unnamed: 4': 'InvoiceDate', 'Unnamed: 5': 'Payrupees'}, inplace=True)
gst_df = gst_df.drop(range(5), axis=0)
office_df = office_df[['GSTIN', 'Name', 'InvoiceDate', 'Payrupees']]

gst_df = gst_df.groupby('GSTIN').agg( Name=('Name', 'first'), Payrupees=('Payrupees', 'sum')).reset_index()
office_df = office_df.groupby('GSTIN').agg( Name=('Name', 'first'), Payrupees=('Payrupees', 'sum')).reset_index()

# Merge the dataframes
merged_df = pd.merge(gst_df, office_df, on='GSTIN', suffixes=('_df1', '_df2'), how='outer')
# Subtract Payrupees values to calculate 'Difference'
merged_df['Difference'] = merged_df['Payrupees_df1'] - merged_df['Payrupees_df2']
# Fill NaN values in 'Difference' column with non-NaN values from either 'Payrupees_df1' or 'Payrupees_df2'
merged_df['Difference'] = merged_df['Difference'].fillna(merged_df['Payrupees_df1']).fillna(merged_df['Payrupees_df2'])
# Convert the 'Difference' column to absolute values
merged_df['Difference'] = merged_df['Difference'].abs()
# Print the resulting dataframe
print(merged_df.to_string())

threshold = 2
filtered_df = merged_df[merged_df['Difference'] > threshold]
filtered_df.rename(columns={'Name_df1': 'GST NAME', 'Name_df2': 'OFFICE NAME'}, inplace=True)
filtered_df
