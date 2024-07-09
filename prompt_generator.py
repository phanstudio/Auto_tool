import pandas as pd
import os, json

def save_prompts(num, prompt):
    def update_dict(existing_data):
        if num not in existing_data:
            current_data = {num: prompt}
            stacked_data = existing_data.copy()
            stacked_data.update(current_data)
            return stacked_data
        else:
            existing_data[num] = prompt
            return existing_data
    info_path = 'work_stuff/prompts.json'
    existing_data = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as existing_file:
            existing_data = json.load(existing_file)
    
    existing_data = update_dict(existing_data)
    with open(info_path, 'w') as f:
        json.dump(existing_data, f, indent= 2)

def prompt_generator(sym, num:int):
    with open('work_stuff/prompt_list.txt', 'r') as f:
        data = f.read().split('\n')
    prompt = f'{data[(num%len(data))]} \n{sym}'
    return prompt

prompt_num = 2
for i in range(len(os.listdir('Auto_tool/chunks'))):
    df = pd.read_csv(f'work_stuff/chunks/chunk_{i}.csv')
    df['diagnosis'] = None
    symptoms = df.to_csv(index= False).replace('None', '')
    prompt = prompt_generator(symptoms, prompt_num)
    save_prompts(i, prompt)
