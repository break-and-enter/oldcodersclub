import webbrowser
from urllib.parse import quote
import pyautogui
import time

with open('phones.txt', 'r') as phones_file:
    phones_and_names_list = phones_file.readlines()

screen_width, screen_height = pyautogui.size()

for row in phones_and_names_list:
    row_list = row.split(',')
    phone = row_list[0].strip()
    name =  row_list[1].strip()

    message = f'Здравствуйте {name}! У нас началась распродажа! Скидки до -30%!'
    encoded_message = quote(message)

    webbrowser.open(f'https://web.whatsapp.com/send?phone={phone}&text={encoded_message}')
    time.sleep(15)

    pyautogui.click(screen_width/2, screen_height/2)

    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.hotkey('command', 'w')    # Для windows 'ctrl', 'w'