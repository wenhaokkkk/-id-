import pyautogui
import pyperclip
import time

def main():
    try:
        with open("target_ids.txt", "r", encoding="utf-8") as f:
            target_ids = f.read().splitlines()
    except FileNotFoundError:
        print("未找到字典文件！")
        return

    print("准备开始！请在 5 秒内将游戏窗口切换到最前...")
    time.sleep(5)

    # 替换为你实际输入框的坐标
    input_box_pos = (800, 600)  

    for name in target_ids:
        if not name.strip():
            continue
            
        print(f"正在尝试 ID: {name} ...", end=" ")

        # 节点 1: 点击对话框
        pyautogui.click(input_box_pos[0], input_box_pos[1])
        pyautogui.press('backspace', presses=6, interval=0.05) 
        
        # 节点 2: 输入 ID
        pyperclip.copy(name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        
        # 节点 3: 第一次回车 (提交名字)
        pyautogui.press('enter')
        time.sleep(0.8) # 留出弹窗动画时间

        # 节点 4: 第二次回车 (确认使用并向服务器发送)
        pyautogui.press('enter')
        
        # 【关键等待】等待服务器校验并加载新页面，时间可视你的网络延迟微调
        time.sleep(2.0) 

        # 分支判断：是否显示了“设定角色”页面
        try:
            # 寻找成功页面的特征图
            is_success = pyautogui.locateOnScreen('success_page.png', confidence=0.8)
        except Exception:
            is_success = None

        if is_success:
            # 状态转移: 设定角色 -> exit
            print(f"\n🎉 成功！检测到设定角色页面，抢注 ID: {name}。程序已停止。")
            break 
        else:
            # 状态转移: 失败 -> 第三次回车 -> 循环回起点
            print("❌ 被占用")
            # 此时屏幕上是那个红色的“该名字已被使用”弹窗，敲击回车关闭它
            pyautogui.press('enter')
            # 稍微停顿一下，防止连续输入导致游戏判定恶意按键
            time.sleep(0.5)

if __name__ == "__main__":
    main()