import tkinter as tk
from tkinter import messagebox
import random
import itertools
import operator

# 游戏版本
ver = "1.0"

# 难度设置
difficulty_levels = {
    "简单": {"range": (1, 9), "operators": ["+", "-", "*", "/"]},
    "中等": {"range": (1, 15), "operators": ["+", "-", "*", "/"]},
    "困难": {"range": (1, 20), "operators": ["+", "-", "*", "/"]}
}

# 当前难度
current_difficulty = "简单"

# 全局变量
numbers = []
entry = None
result_label = None
game_window = None
settings_window = None
about_window = None
start_window = None

# 随机生成四个数字
def generate_numbers():
    difficulty = difficulty_levels[current_difficulty]
    return [random.randint(difficulty["range"][0], difficulty["range"][1]) for _ in range(4)]

# 验证用户输入的表达式
def validate_expression(expression, numbers):
    try:
        # 替换乘除符号
        expression = expression.replace("×", "*").replace("÷", "/")
        # 检查表达式是否只包含给定的数字
        for num in numbers:
            if str(num) not in expression:
                return False
        # 计算表达式结果
        if eval(expression) == 24:
            return True
    except:
        pass
    return False

# 游戏界面
def start_game():
    global numbers, entry, result_label, game_window, start_window
    if game_window:  # 如果游戏窗口已存在，先销毁
        game_window.destroy()
    numbers = generate_numbers()
    
    # 创建游戏窗口
    game_window = tk.Toplevel(start_window)
    game_window.title("24点游戏")
    game_window.geometry("600x365")
    game_window.resizable(False, False)
    game_window.iconbitmap("icon.ico")  # 确保图标文件存在
    
    number_label = tk.Label(game_window, text=f"数字: {numbers[0]} {numbers[1]} {numbers[2]} {numbers[3]}", font=("楷体", 16))
    number_label.pack()
    
    entry = tk.Entry(game_window, font=("楷体", 14))
    entry.pack()
    
    check_button = tk.Button(game_window, text="检查答案", command=check_answer, height=2, width=15)
    check_button.pack(pady=10)
    
    result_label = tk.Label(game_window, text="", font=("楷体", 16))
    result_label.pack()
    
    restart_button = tk.Button(game_window, text="重新开始", command=restart_game, height=2, width=15)
    restart_button.pack(pady=10)
    
    # 添加提示按钮
    hint_button = tk.Button(game_window, text="提示", command=provide_hint, height=2, width=15)
    hint_button.pack(pady=10)
    
    # 添加返回按钮
    back_button = tk.Button(game_window, text="返回开始界面", command=back_to_start, height=2, width=15)
    back_button.pack(pady=10)

    start_window.withdraw()  # 隐藏开始界面

# 提供提示
def provide_hint():
    global numbers
    hint = generate_hint(numbers)
    if hint:
        result_label.config(text=f"提示: {hint}", fg="blue")
    else:
        result_label.config(text="未找到解题思路", fg="red")

# 生成逐步引导的提示
def generate_hint(nums):
    # 定义运算符和对应的函数
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }
    
    # 生成所有可能的数字排列
    for perm in itertools.permutations(nums):
        # 生成所有可能的运算符组合
        for ops_perm in itertools.product(ops.keys(), repeat=3):
            try:
                # 尝试计算表达式
                expr1 = f"({perm[0]} {ops_perm[0]} {perm[1]}) {ops_perm[1]} ({perm[2]} {ops_perm[2]} {perm[3]})"
                if eval(expr1) == 24:
                    return f"尝试使用 ({perm[0]} {ops_perm[0]} {perm[1]}) 和 ({perm[2]} {ops_perm[2]} {perm[3]})"
                expr2 = f"(({perm[0]} {ops_perm[0]} {perm[1]}) {ops_perm[1]} {perm[2]}) {ops_perm[2]} {perm[3]}"
                if eval(expr2) == 24:
                    return f"尝试使用 (({perm[0]} {ops_perm[0]} {perm[1]}) {ops_perm[1]} {perm[2]}) 和 {perm[3]}"
                expr3 = f"{perm[0]} {ops_perm[0]} (({perm[1]} {ops_perm[1]} {perm[2]}) {ops_perm[2]} {perm[3]})"
                if eval(expr3) == 24:
                    return f"尝试使用 {perm[0]} 和 (({perm[1]} {ops_perm[1]} {perm[2]}) {ops_perm[2]} {perm[3]})"
            except ZeroDivisionError:
                continue
    return None

# 检查答案
def check_answer():
    global numbers, entry, result_label
    user_expression = entry.get()
    if validate_expression(user_expression, numbers):
        result_label.config(text="恭喜，你赢了！", fg="green")
    else:
        result_label.config(text="再试一次！", fg="red")

# 重新开始游戏
def restart_game():
    global game_window
    game_window.destroy()
    start_game()

# 返回开始界面
def back_to_start():
    global game_window
    if game_window:
        game_window.destroy()
    start_window.deiconify()  # 显示开始界面

# 设置界面
def open_settings():
    global settings_window, start_window
    if settings_window:
        settings_window.lift()  # 提升现有设置窗口到最前面
        return
    settings_window = tk.Toplevel(start_window)
    settings_window.title("设置")
    settings_window.geometry("300x200")
    settings_window.resizable(False, False)
    settings_window.iconbitmap("icon.ico")  # 确保图标文件存在
    
    difficulty_label = tk.Label(settings_window, text="难度设置", font=("宋体", 14))
    difficulty_label.pack(pady=10)
    
    # 难度选择
    difficulty_var = tk.StringVar()
    difficulty_var.set(current_difficulty)
    difficulty_options = ["简单", "中等", "困难"]
    difficulty_menu = tk.OptionMenu(settings_window, difficulty_var, *difficulty_options)
    difficulty_menu.pack(pady=10)
    
    # 保存设置按钮
    save_button = tk.Button(settings_window, text="保存设置", command=lambda: save_settings(difficulty_var))
    save_button.pack(pady=10)

# 保存设置
def save_settings(difficulty_var):
    global current_difficulty, settings_window
    current_difficulty = difficulty_var.get()
    messagebox.showinfo("设置已保存", f"难度: {current_difficulty}")
    settings_window.destroy()
    start_window.deiconify()  # 显示开始界面

# 关于界面
def open_about():
    global about_window, start_window
    if about_window:
        about_window.lift()  # 提升现有关于窗口到最前面
        return
    about_window = tk.Toplevel(start_window)
    about_window.title("关于")
    about_window.geometry("300x200")
    about_window.resizable(False, False)
    about_window.iconbitmap("icon.ico")  # 确保图标文件存在
    
    about_label = tk.Label(about_window, text="24点游戏", font=("宋体", 16))
    about_label.pack(pady=10)
    
    version_label = tk.Label(about_window, text=f"版本: {ver}", font=("宋体", 14))
    version_label.pack(pady=10)
    
    author_label = tk.Label(about_window, text="作者: LJT", font=("宋体", 14))
    author_label.pack(pady=10)

# 退出程序
def exit_program():
    start_window.destroy()

# 创建开始界面
def create_start_window():
    global start_window
    start_window = tk.Tk()
    start_window.title("24点游戏 - 开始界面")
    start_window.geometry("400x300")
    start_window.resizable(False, False)
    start_window.iconbitmap("icon.ico")  # 确保图标文件存在
    
    start_label = tk.Label(start_window, text="欢迎来到24点游戏！", font=("宋体", 20))
    start_label.pack(pady=20)
    
    start_button = tk.Button(start_window, text="开始游戏", command=start_game, height=2, width=15)
    start_button.pack(pady=10)

    # 创建一个frame来包含设置和关于按钮
    buttons_frame = tk.Frame(start_window)
    buttons_frame.pack(fill=tk.X, padx=10, pady=5)
    
    settings_button = tk.Button(buttons_frame, text="设置", command=open_settings, height=2, width=7)
    settings_button.pack(side=tk.LEFT, padx=10)
    
    about_button = tk.Button(buttons_frame, text="关于", command=open_about, height=2, width=7)
    about_button.pack(side=tk.RIGHT, padx=10)  # 将关于按钮放置在设置按钮的右侧
    
    # 添加退出按钮
    exit_button = tk.Button(start_window, text="退出", command=exit_program, height=2, width=15)
    exit_button.pack(pady=10)

# 立即创建开始界面
create_start_window()

# 进入主循环
start_window.mainloop()