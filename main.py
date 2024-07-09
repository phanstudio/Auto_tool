import pyautogui
from pyautogui import Point
import pyperclip
import os
import json

exit_position = Point(x=1773, y=712)
placement_position = Point(x=471, y=944)

def save_output(dict, sys_name):
    info_path = f'work_stuff/{sys_name}_output.json'
    existing_data = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as existing_file:
            existing_data = json.load(existing_file)
    
    existing_data.update(dict)
    with open(info_path, 'w') as f:
        json.dump(existing_data, f, indent= 2)

def get_pos(call_times=1, mess=''):
    if call_times < 1:
        raise ValueError("call_times should be above 0")
    pos = []
    for _ in range(call_times):
        if call_times == 1:
            input('\nPlace cursor at the position of the %s, and then press enter \n' % (mess))
            pos = pyautogui.position()
        else:
            input('\nPlace cursor at the right positions, and then press enter \n')
            pos.append(pyautogui.position())
    return pos

def compare_points(x:Point, y:Point, diff = 0):
    def add(x,y):
        return (x + y)
    if x == None or y == None: return False
    return abs(add(*x) - add(*y)) < diff

def check_loading(icon, multplier= 1):
    icon_position = pyautogui.locateCenterOnScreen(icon, confidence=0.9)
    if icon_position == None:
        return False
    pyautogui.sleep(multplier)
    return True

def r_click(xy:Point):
    current_position = pyautogui.position()
    pyautogui.click(*xy)
    pyautogui.moveTo(*current_position)


class GptAutomation:
    def __init__(self) -> None:
        self.output = {}
        self.loader_position = Point(x=1568, y=948)
        self.input_position = Point(x=798, y=931)
        self.tab_value = 1
        self.name = 'gpt'
        self.error = False
        self.check_img = '.\Auto_tool\src\loading_bar.png'
    
    def initial(self, prompt, _id):
        self.id = _id
        self.prompt = prompt
        r_click(self.input_position)
        pyperclip.copy(prompt)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
    
    def checking(self):
        try:
            return check_loading(self.check_img)
        except:
            self.error = True
    
    def finish_copy(self):
        try:
            pyautogui.moveTo(*placement_position)
            self.copy_position = pyautogui.locateCenterOnScreen('.\work_stuff\copy_icon.png', confidence=0.9)
            r_click(self.copy_position)
            self.output[self.id] = pyperclip.paste()
        except:
            self.output[self.id] = ""

class GeminiAutomation:
    def __init__(self) -> None:
        self.output = {}
        self.loader_position = Point(x=1614, y=931)
        self.input_position = Point(x=712, y=943)
        self.tab_value = 2
        self.name = 'gemini'
        self.error = False
        self.check_img = '.\Auto_tool\src\g_loading_bar.png'
    
    def initial(self, prompt, _id):
        self.id = _id
        self.prompt = prompt
        r_click(self.input_position)
        pyperclip.copy(self.prompt)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
    
    def checking(self):
        try:
            return check_loading(self.check_img)
        except:
            self.error = True
    
    def finish_copy(self):
        try:
            pyautogui.sleep(1)
            r_click(exit_position)
            pyautogui.sleep(2)
            pyautogui.hotkey('ctrl', 'end')
            pyautogui.sleep(1)
            self.copy_position = pyautogui.locateCenterOnScreen('.\Auto_tool\src\g_copy_icon.png', confidence=0.9)
            r_click(self.copy_position)
            pyautogui.press('down', 2)
            pyautogui.press('enter')
            pyautogui.sleep(1)
            self.output[self.id] = pyperclip.paste()
        except:
            self.output[self.id] = ""

class PerplexityAutomation:
    def __init__(self) -> None:
        self.output = {}
        self.input_position = Point(x=626, y=925) 
        self.copy_position = Point(x=1167, y=400)
        self.tab_value = 3
        self.name = 'perplexity'
        self.error = False
        self.check_img = '.\Auto_tool\src\p2_loading_bar.png'
    
    def initial(self, prompt, _id):
        self.id = _id
        self.prompt = prompt
        r_click(self.input_position)
        pyperclip.copy(self.prompt)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
    
    def checking(self):
        try:
            return check_loading(self.check_img)
        except:
            self.error = True
    
    def finish_copy(self):
        try:
            r_click(exit_position)
            pyautogui.sleep(1)
            pyautogui.hotkey('ctrl', 'end')
            pyautogui.sleep(1)
            pyautogui.hotkey('ctrl', 'end')
            r_click(self.copy_position)
            self.output[self.id] = pyperclip.paste()
        except:
            self.output[self.id] = ""

v = 0
s = (10 * v)
e = (10 * (v+1))

response = pyautogui.confirm("Are you ready?",
                                        title="System", buttons=['yes', 'no'])
if response == 'yes':
    info_path = 'work_stuff/prompts.json'
    existing_data = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as existing_file:
            existing_data = json.load(existing_file)
    
    prompts = existing_data.items()
    automation_list = [PerplexityAutomation(), GptAutomation(), GeminiAutomation()]
    error = False
    
    for k, i in list(prompts)[s: e]:
        # initializing
        pyautogui.sleep(1)
        r_click(exit_position)
        for j in automation_list:
            pyautogui.hotkey('ctrl', str(j.tab_value), interval=0.2)
            pyautogui.sleep(1)
            j.initial(i, k)
            pyautogui.sleep(1)
        
        # Checking
        check_list = automation_list.copy()
        for _ in range(200):
            for j in check_list:
                pyautogui.hotkey('ctrl', str(j.tab_value))
                pyautogui.sleep(1)
                if j.checking() == False: 
                    check_list.remove(j)
                    break
            if check_list == []:
                break
        
        for j in automation_list:
            if j.error:
                error = True
                break
        
        if error: break
        
        for j in automation_list:
            pyautogui.hotkey('ctrl', str(j.tab_value))
            pyautogui.sleep(1)
            j.finish_copy()

    for j in automation_list:
        save_output(j.output, j.name)
