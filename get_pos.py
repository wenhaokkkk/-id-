import pyautogui
import time

print("请将鼠标移动到需要测量的位置...")
time.sleep(3)  # 等待用户将鼠标移动到目标位置
while True:
    print(pyautogui.position())
    time.sleep(1)