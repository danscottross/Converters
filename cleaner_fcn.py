import pandas as pd
import os

# Ingest the file
def cleaner(filepath):

    filepath = filepath.replace("\"", "")

    filetype = os.path.splitext(filepath)[1]

    if filetype != '.txt':
        raise Exception("Wrong file type. Please upload a csv.")
        return
    else:
        pass

    with open(filepath, "r", encoding="utf8") as f:
        content = f.read()

    basename = os.path.basename(filepath)
    file_name = os.path.splitext(basename)[0]
    new_filename = file_name + "_new"
    file_directory = os.path.dirname(filepath)

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
    df.to_csv(f"{file_directory}\\{new_filename}.csv", index=False)