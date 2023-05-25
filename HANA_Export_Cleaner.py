import csv
import pandas as pd

# Set the name of the target file saved to the Desktop
filename = input('Enter the name of the text file saved in the "Inputs" folder. '
                 'Do not include the file path or the file type:')
new_filename = filename + "_UPDATED"

# Ingest the file
with open(f"C:\\Users\\daniel.s.ross\\OneDrive - Accenture Federal Services\\Python Scripts\\Inputs\\{filename}.txt", "r", encoding="utf8") as f:
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

# Assign names to the nameless columns (were unintended delimit-ing was done
df.columns = ["col_"+str(i) if a is None else a for i, a in enumerate(df.columns)]

# Save the dataframe as a CSV
df.to_csv(f"C:\\Users\\daniel.s.ross\\OneDrive - Accenture Federal Services\\Python Scripts\\Outputs\\{new_filename}.csv", index=False)

print('Complete')
