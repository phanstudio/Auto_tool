import re
import pandas as pd
from io import StringIO
import os
import json
import numpy as np
import clean_extractor as ce

def replace_chars(text, replacements):
    """Helper function to replace characters in text."""
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def extract(pattern, text):
    clean_data = re.findall(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not clean_data:
        raise ValueError('Not correct')
    csv_data = '\n'.join(clean_data)
    file_like_object = StringIO(csv_data)
    return pd.read_csv(file_like_object)

def load_output(sys_name):
    info_path = f'work_stuff/{sys_name}_output.json'
    existing_data = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as existing_file:
            existing_data = json.load(existing_file)
    return existing_data

def save_output(model, df, empty=False):
    model = model if not empty else f'{model}_empty'
    output_path = f'Auto_tool/{model}_output.xlsx'
    df.to_excel(output_path, index=False)
    print(f'Saved to {output_path}')

def process_text(text):
    text = replace_chars(text, {
        'PatientID': 'Patient_ID',
        '\\r\\n': '\r\n',
        ' ': '',
        'DengueFever': 'None',
        'TyphoidFever(Both)': 'Both',
        'TyphoidFever': 'Typhoid Fever'
    })
    return text

def extract_single_csv(text):
    text = process_text(text)
    pattern = '^Patient_ID,diagnosis\r?\n(?:Pat_\d+,(?:Malaria|None|Both|Typhoid Fever)\r?\n?)+'
    return extract(pattern, text)

def extract_single_csv(text:str) -> pd.DataFrame:
    text = text.replace('PatientID', 'Patient_ID').replace('\\r\\n', '\r\n').replace(' ', '')
    text = text.replace('DengueFever', 'None').replace('TyphoidFever(Both)', 'Both').replace('TyphoidFever', 'Typhoid Fever')
    pattern = '^Patient_ID,diagnosis\r?\n(?:Pat_\d+,(?:Malaria|None|Both|Typhoid Fever)\r?\n?)+'
    return extract(pattern, text)

def extract_multi_csv(text) -> pd.DataFrame:
    pattern = r'^Patient_ID,ABDOMINAL PAINS,BITTER TASTE IN MOUTH,CHILLS AND RIGORS,CONSTIPATION,FATIGUE,FEVER,HIGH GRADE FEVER,STEPWISE RISE FEVER,GENERALIZED BODY PAIN,HEADACHES,LETHARGY,MUSCLE AND BODY PAIN,diagnosis\r?\n(?:Pat_\d+,(?:.*?\r?\n)+?)+'
    df = extract(pattern, text)

    if len(df['diagnosis'][~pd.isna(df['diagnosis'])]) > 0:
        df['diagnosis'][~pd.isna(df['diagnosis'])] = df['diagnosis'][~pd.isna(df['diagnosis'])].str.strip()
    df['MUSCLE AND BODY PAIN'] = df['MUSCLE AND BODY PAIN'].str.strip()

    condition_mask = df['MUSCLE AND BODY PAIN'].isin(['Malaria', 'Both', 'Typhoid Fever', 'None'])
    df.loc[condition_mask, 'diagnosis'] = df.loc[condition_mask, 'MUSCLE AND BODY PAIN']
    df = df[['Patient_ID','diagnosis']]
    return df


existing_data = load_output('gemini')
df1 = pd.DataFrame()
for i in range(len(existing_data)):
    text = existing_data[str(i)]
    try:
        df2 = extract_single_csv(text)
    except:
        try:
            df2 = extract_multi_csv(text)
        except:
            continue
    df1 = pd.concat([df1, df2], ignore_index=True)

df1 = df1[df1['diagnosis'] != 'diagnosis']
ce.clean_sorter(df1)
empty_df = ce.get_list_of_ids(df1, np.NaN, 101)

# For checking if they are missing Patient values
df1 = pd.concat([df1, empty_df], ignore_index=True)
ce.clean_sorter(df1)

save_output('gemini', df1)
save_output('gemini', empty_df, True)