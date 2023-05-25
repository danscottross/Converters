import csv
import pandas as pd

# Set the name of the files that will and ingest the raw text file into memory
filename = input('Enter the name of the text file saved in the "Inputs" folder. '
                 'Do not include the file path or the file type:')
new_filename = filename + "withFUEL_TYPE"

df = pd.read_csv(f"C:\\Users\\daniel.s.ross\\OneDrive - Accenture Federal Services\\Python Scripts\\Inputs\\{filename}.csv")

"""
# Assign names to the nameless columns (were unintended delimit-ing was done
df.columns = ["col_"+str(i) if a is None else a for i, a in enumerate(df.columns)]

# Consolidate all the unintended delimited columns into one description field
df['PD_DESCRIPTION'] = df[df.columns[5:]].apply(
    lambda x: ' || '.join(x.dropna().astype(str)), axis=1)
"""

# Create a temporary column to house all request information
df.insert(loc=12, column='FULL_DESC', value="")
df['FULL_DESC'] = df['LINE_DESC'] + ' || ' + df['ARIBA_AWARD_DESCRIPTION']

# Create FUEL_TYPE field and assign fuel types based on contents of description field
# df.insert(loc=10, column='FUEL_TYPE', value="")
for index, row in df.iterrows():
    if 'hibrid' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'hybrid' in str(df.loc[index, 'FULL_DESC']).lower():
        df.loc[index, 'FUEL_TYPE'] = "Hybrid"
    elif 'diesel' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'deesel' in str(df.loc[index, 'FULL_DESC']):
        df.loc[index, 'FUEL_TYPE'] = "DSL DE"
    elif 'gas' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'petrol' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'v6' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'v8' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'fuel capacity' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'cylinder' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'cyl' in str(df.loc[index, 'FULL_DESC']).lower():
        df.loc[index, 'FUEL_TYPE'] = "GAS DE"
    elif 'electric' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'tesla' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'phev' in str(df.loc[index, 'FULL_DESC']).lower():
        df.loc[index, 'FUEL_TYPE'] = "Electric"
    elif 'fee' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'charges' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'tax' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'monthly subscription' in str(df.loc[index, 'FULL_DESC']).lower():
        df.loc[index, 'FUEL_TYPE'] = "N/A - Fee"
    elif 'test' in str(df.loc[index, 'FULL_DESC']).lower():
        df.loc[index, 'FUEL_TYPE'] = "N/A - Test"
        # elif 'hilux' in str(df.loc[index, 'FULL_DESC']).lower() \
        #         or 'hi-lux' in str(df.loc[index, 'FULL_DESC']).lower():
        #     df.loc[index, 'FUEL_TYPE'] = "Toyota Hilux"
        # elif 'hiace' in str(df.loc[index, 'FULL_DESC']).lower():
        #     df.loc[index, 'FUEL_TYPE'] = "Toyota HiAce"
        # elif 'land cruiser' in str(df.loc[index, 'FULL_DESC']).lower():
        #     df.loc[index, 'FUEL_TYPE'] = "Toyota Land Cruiser"
        # elif 'land cruiser' in str(df.loc[index, 'FULL_DESC']).lower():
        #     df.loc[index, 'FUEL_TYPE'] = "Toyota Land Cruiser"
    elif 'office suppl' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'cell phone' in str(df.loc[index, 'FULL_DESC']).lower() \
            or 'office chair' in str(df.loc[index, 'FULL_DESC']).lower():
        df.loc[index, 'FUEL_TYPE'] = "N/A - Test"
    else:
        df.loc[index, 'FUEL_TYPE'] = "N/A - Undetected"

# Trim dataframe to only include useful information
df = df.iloc[:, :12]

# Save the dataframe as a CSV
df.to_csv(f"C:\\Users\\daniel.s.ross\\OneDrive - Accenture Federal Services\\Python Scripts\\Outputs\\{new_filename}.csv", index=False)

print('Complete')
