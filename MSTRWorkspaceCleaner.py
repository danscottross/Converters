import pandas as pd
import regex as re

with open(r"C:\Users\daniel.s.ross\Downloads\list documents.log", 'r') as f:
    log = f.read()

values = re.sub("' with ID: '", ", ", log)
values = re.sub(".+: '", "", values)
values = re.sub("'", "", values)

df = pd.DataFrame([line.split(",") for line in values.split("\n")]a
                  , columns=["Document Object", "ID"])

df = df.iloc[4:-1, :]
df.reset_index(drop=True, inplace=True)

print(df)
