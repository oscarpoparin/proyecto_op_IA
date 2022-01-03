import webbrowser
import pyautogui as at
import time

def send_menssage(contac, message):
    webbrowser.open(f"https://web.whatsapp.com/send?phone={contac}&text={message}")
    time.sleep(8)
    at.press('enter')