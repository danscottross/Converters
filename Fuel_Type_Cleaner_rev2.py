# import libraries
import pandas as pd

# Set the name of the files that will and ingest the raw text file into memory
filename = input('Enter the name of the text file saved in the "Inputs" folder. '
                 'Do not include the file path or the file type:')
new_filename = filename + "_UPDATED"
with open(f"C:\\Users\\daniel.s.ross\\OneDrive - Accenture Federal Services\\Python Scripts\\Inputs\\{filename}.txt",
          "r", encoding="utf8") as f:
    content = f.read()

# Execute some high-level replacements to allow for cleaner data
content = content.replace(r"\n", " | ")
content = content.replace(r"\t", " ")
content = content.replace("\t", " ")

# Clean up the large spaces that are due to the txt formatting
space = '                                                        '
while len(space) > 1:
    content = content.replace(space, '')
    space = space[0:-1]

# Execute further replacements to clean up the data around semicolons
content = content.replace(" ;", ";")
content = content.replace("; ", ";")

# Generate the dataframe
df = pd.DataFrame([x.split(";") for x in content.split("\n")])

# Promote first row and column to the index and header
df.columns = df.iloc[0]
df = df[1:]
df.columns.values[0] = 'INDEX'
df = df.set_index('INDEX')

# Assign names to the nameless columns that were unintentionally delimited
df.columns = ["col_" + str(i) if a is None else a for i, a in enumerate(df.columns)]

# Consolidate all the unintentionally delimited columns into one description field
df['FULL_DESC'] = df[df.columns[df.columns.get_loc('FULL_DESC'):]].apply(
    lambda x: ' || '.join(x.dropna().astype(str)), axis=1)

df = df.loc[:, 'BUSINESS_UNIT':'FULL_DESC']

# Assign fuel types based on contents of description field
for index, row in df.iterrows():
    if str(row["FUEL_TYPE"]).lower() != "n/a":
        pass
    else:
        if 'hibrid' in str(row["FULL_DESC"]).lower() \
                or 'hybrid' in str(row["FULL_DESC"]).lower():
            if 'diesel' in str(row["FULL_DESC"]).lower():
                df.loc[index, "FUEL_TYPE"] = "DSL HY"
            elif 'phev' in str(row["FULL_DESC"]).lower() \
                    or 'plug-in' in str(row["FULL_DESC"]).lower():
                df.loc[index, "FUEL_TYPE"] = "GAS PH"
            else:
                df.loc[index, "FUEL_TYPE"] = "GAS HY"
        elif 'diesel' in str(row["FULL_DESC"]).lower() \
                or 'deesel' in str(row["FULL_DESC"])\
                or 'dsl' in str(row["FULL_DESC"]):
            df.loc[index, "FUEL_TYPE"] = "DSL DE"
        elif 'gas' in str(row["FULL_DESC"]).lower() \
                or 'petrol' in str(row["FULL_DESC"]).lower() \
                or 'v6' in str(row["FULL_DESC"]).lower() \
                or 'v8' in str(row["FULL_DESC"]).lower() \
                or 'fuel capacity' in str(row["FULL_DESC"]).lower() \
                or 'cylinder' in str(row["FULL_DESC"]).lower() \
                or 'cyl' in str(row["FULL_DESC"]).lower():
            df.loc[index, "FUEL_TYPE"] = "GAS DE"
        elif 'electric' in str(row["FULL_DESC"]).lower() \
                or 'tesla' in str(row["FULL_DESC"]).lower():
            df.loc[index, "FUEL_TYPE"] = "ELE DE"
        elif 'fee' in str(row["FULL_DESC"]).lower() \
                or 'charges' in str(row["FULL_DESC"]).lower() \
                or 'tax' in str(row["FULL_DESC"]).lower() \
                or 'monthly subscription' in str(row["FULL_DESC"]).lower():
            df.loc[index, "FUEL_TYPE"] = "N/A - Fee"
        elif 'test' in str(row["FULL_DESC"]).lower():
            df.loc[index, "FUEL_TYPE"] = "N/A - Test"
        elif 'office suppl' in str(row["FULL_DESC"]).lower() \
                or 'cell phone' in str(row["FULL_DESC"]).lower() \
                or 'office chair' in str(row["FULL_DESC"]).lower():
            df.loc[index, "FUEL_TYPE"] = "N/A - Test"
        else:
            df.loc[index, "FUEL_TYPE"] = "N/A - Undetected"

# Trim dataframe to only include useful information
df = df.iloc[:, :12]

# Save the dataframe as a CSV
df.to_csv(f"C:\\Users\\daniel.s.ross\\OneDrive - Accenture Federal Services\\"
          f"Python Scripts\\Outputs\\{new_filename}.csv", index=False)

print('Complete')
