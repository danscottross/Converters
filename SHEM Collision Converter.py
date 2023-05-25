import pandas as pd
import numpy as np
from datetime import date

#input_file = input("Please enter the file path of the SHEM Collision Data you would like to transform: ")
input_file = r"C:\Users\daniel.s.ross\Downloads\SHEM Collision Data Extract 23-02-01.xlsx"

df = pd.read_excel(input_file, header=1)

location_dict = {"GENEVA (TNF)": "GENEVA"
    , "USUN GENEVA": "GENEVA"
    , "AIT KAOHSIUNG": "KAOHSIUNG"
    , "AIT TAIPEI": "TAIPEI"
    , "BAGHDAD DIPLOMATIC SUPPORT CENTER (BDSC)": "APO BAGHDAD DIPL SVC CENTER"
    , "HAGUE, THE": "THE HAGUE"
    , "JERUSALEM, EMBASSY": "JERUSALEM"
    , "PORT AU PRINCE": "PORT-AU-PRINCE"
    , "PORT OF SPAIN": "PORT-OF-SPAIN"
    , "TEL AVIV, EBO": "TEL AVIV"
    , "N'DJAMENA": "N''DJAMENA"
                 }

def convert_location(original_post):
    if original_post in location_dict:
        return location_dict[original_post]
    else:
        return original_post

def convert_date(original_date):
    datetime_date = np.datetime64(original_date)
    year = pd.to_datetime(datetime_date).year
    month = pd.to_datetime(datetime_date).month
    day = pd.to_datetime(datetime_date).day
    new_date = str(year) + str(month).zfill(2) + str(day).zfill(2)
    return new_date

def convert_armor(original_armor):
    if original_armor == "Classified":
        return 'NULL'
    else:
        return original_armor

df['Post Name'] = df['Post Name'].apply(convert_location)
df['OV Armor'] = df['OV Armor'].apply(convert_armor)
df['Date of Mishap'] = df['Date of Mishap'].apply(convert_date)
df['Event ID'] = df['Event ID'].astype(str)

df['SQL Statement'] = "INSERT INTO FMIS_NLG.SHEM_COLLISION_DATA VALUES('" + df['Post Name'] + "', '" + df['Event ID'] + "', '" + df['Date of Mishap'] + "', '" + df['Mishap Class'] + "', '" + df['OV Armor'] + "', NULL, NULL, NULL);"

min_date = min(df['Date of Mishap'])

output = '\n'.join(df['SQL Statement'].tolist())

output_file = fr"C:\Users\daniel.s.ross\Downloads\SHEM_Upload {date.today()}.txt"

query = f"""SELECT *
-- DELETE 
FROM FMIS_NLG.SHEM_COLLISION_DATA
WHERE MISHAP_DATE >= TO_DATE'({min_date}')
ORDER BY MISHAP_DATE ASC
;

"""

with open(output_file, "w") as f:
    f.write(query)
    f.write(output)