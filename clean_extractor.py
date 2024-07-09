import pandas as pd

def custom_sort_key(patient_id):
    # Extract the numeric part of the ID
    num_part = int(patient_id.split('_')[1])
    
    # Map IDs to custom numerical values
    if num_part <= 6676:
        return num_part
    else:
        return num_part + 10000  # Ensures IDs from 6677 onwards come last

def clean_sorter(df):
    df.reset_index(drop=True, inplace=True)
    df.sort_values(by='Patient_ID', key=lambda col: col.apply(custom_sort_key), inplace= True)
    df.drop_duplicates(subset=['Patient_ID'], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)

def get_list_of_ids(df, miss, num= 6677):
    expected_patient_ids = ['Pat_' + str(i) for i in range(1, num)]
    missing_patient_ids = set(expected_patient_ids) - set(df['Patient_ID'])
    new_rows = [{'Patient_ID': pid, 'diagnosis': miss} for pid in missing_patient_ids]
    new_df = pd.DataFrame(new_rows)
    return new_df
