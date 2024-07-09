import pandas as pd
import os

df = pd.read_csv(r'Auto_tool/resampled_XAIData_copy.csv')
diseases = df.pop('disease')
level = [' absent',' low', ' moderate', ' high', ' very high']
for i in range(len(level)):
    df = df.replace(i+1, level[i])

def save_chunks_as_csv(df, chunk_size=50, num= None, prefix='chunk'):
    """
    Splits a DataFrame into chunks and saves each chunk as a separate CSV file.
    
    Parameters:
    - df: The DataFrame to split.
    - chunk_size: Number of rows in each chunk.
    - prefix: Prefix for the filenames.
    """
    path = 'Auto_tool/chunks'
    if not os.path.exists(r'work_stuff/chunks'):
        os.mkdir(path)
    num_chunks = len(df) // chunk_size + (len(df) % chunk_size > 0)
    num_chunks = num if num != None else num_chunks
    for i in range(num_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, len(df))
        chunk_df = df.iloc[start:end]
        filename = f"{prefix}_{i}.csv"
        chunk_df.to_csv(f'{path}/{filename}', index=False)
        print(f"Saved chunk {i} to {filename}")

save_chunks_as_csv(df, 50)