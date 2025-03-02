import tkinter as tk
from tkinter import messagebox
import My_Dict  # 导入你的词典文件

# 重新加载词典
def reload_dict():
    global languages_dict
    languages_dict = My_Dict.load_dict()

# 根据单词获取冠词
def get_article(word, lang):
    if word in languages_dict[lang]["noun"]:
        gender = languages_dict[lang]["noun"][word]["gender"]
        return {"m": "Der", "f": "Die", "n": "Das"}.get(gender, "")
    return ""

# 翻译函数
def translate(word, lang):
    if lang in languages_dict and "noun" in languages_dict[lang] and word in languages_dict[lang]["noun"]:
        translation = languages_dict[lang]["noun"][word]["translation"]
        article = get_article(word, lang)
        return f"{article} {translation}".strip()
    else:
        ask_for_translation(word, lang)
        return "该单词不在字典中，请添加后重试。"

# 弹出窗口，输入新翻译
def ask_for_translation(word, lang):
    def save_translation():
        new_translation = entry_translation.get()
        new_gender = gender_var.get()
        new_plural = entry_plural.get()
        new_category = category_var.get()

        if not new_translation:
            messagebox.showwarning("警告", "翻译不能为空！")
            return

        # 确保子字典存在
        if lang not in languages_dict:
            languages_dict[lang] = {}
        if new_category not in languages_dict[lang]:
            languages_dict[lang][new_category] = {}

        # 存入词典
        languages_dict[lang][new_category][word] = {
            "translation": new_translation
        }
        if new_category == "noun" and new_gender != "none":  # 仅名词需要性别
            languages_dict[lang][new_category][word]["gender"] = new_gender
        if new_category == "noun" and new_plural:
            languages_dict[lang][new_category][word]["plural"] = new_plural

        # 保存到 My_Dict.json
        My_Dict.languages_dict = languages_dict  # 更新 My_Dict.py 中的词典
        My_Dict.save_dict()  # 保存数据到 JSON

        messagebox.showinfo("成功", f"已添加：{word} → {new_translation}")
        add_window.destroy()
        reload_dict()  # 重新加载最新的字典数据

    # 创建新窗口
    add_window = tk.Toplevel(root)
    add_window.title("添加新翻译")
    add_window.geometry("800x500")

    tk.Label(add_window, text=f"添加 '{word}' 的翻译：", font=("Arial", 12)).pack(pady=5)
    entry_translation = tk.Entry(add_window, font=("Arial", 12))
    entry_translation.pack(pady=5)

    # 选择词类（名词、动词、形容词等）
    category_var = tk.StringVar(value="noun")  # 默认是名词
    tk.Label(add_window, text="选择词类：", font=("Arial", 12)).pack()
    tk.Radiobutton(add_window, text="名词", variable=category_var, value="noun").pack()
    tk.Radiobutton(add_window, text="动词", variable=category_var, value="verb").pack()
    tk.Radiobutton(add_window, text="形容词", variable=category_var, value="adj").pack()
    tk.Radiobutton(add_window, text="副词", variable=category_var, value="adv").pack()

    # 仅名词才显示性别和复数形式
    gender_var = tk.StringVar(value="none")  # 默认无性别
    gender_frame = tk.Frame(add_window)  # 用于动态显示性别选项
    tk.Label(gender_frame, text="选择性别：", font=("Arial", 12)).pack()
    tk.Radiobutton(gender_frame, text="阳性 (der)", variable=gender_var, value="m").pack()
    tk.Radiobutton(gender_frame, text="阴性 (die)", variable=gender_var, value="f").pack()
    tk.Radiobutton(gender_frame, text="中性 (das)", variable=gender_var, value="n").pack()
    tk.Radiobutton(gender_frame, text="无性别", variable=gender_var, value="none").pack()

    # 复数形式（仅适用于名词）
    plural_frame = tk.Frame(add_window)  # 用于动态显示复数形式输入框
    tk.Label(plural_frame, text="输入复数形式：", font=("Arial", 12)).pack()
    entry_plural = tk.Entry(plural_frame, font=("Arial", 12))
    entry_plural.pack(pady=5)

    # 动态显示性别和复数
    def toggle_gender_and_plural():
        if category_var.get() == "noun":
            gender_frame.pack(pady=5)
            plural_frame.pack(pady=5)
        else:
            gender_frame.pack_forget()
            plural_frame.pack_forget()

    category_var.trace("w", lambda *args: toggle_gender_and_plural())  # 根据词类选择显示或隐藏性别和复数

    toggle_gender_and_plural()  # 初始化时确定显示状态

    tk.Button(add_window, text="保存", font=("Arial", 12), command=save_translation).pack(pady=10)


root = tk.Tk()
root.title("塔萨通用语翻译器Ver/EA.20250302")
root.geometry("900x500")

label = tk.Label(root, text="请输入单词：", font=("Arial", 14))
label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

language_var = tk.StringVar(value="zh")
tk.Label(root, text="选择输入语言：", font=("Arial", 14)).pack(pady=5)
tk.Radiobutton(root, text="中文", variable=language_var, value="zh", font=("Arial", 12)).pack()
tk.Radiobutton(root, text="帝国通用语", variable=language_var, value="created", font=("Arial", 12)).pack()

frame = tk.Frame(root)  # 限制 `result_label` 的大小
frame.pack(fill="both", expand=True)

result_label = tk.Label(frame, text="翻译结果：", font=("Arial", 14), height=3, wraplength=400)
result_label.pack(pady=10)

def show_translation():
    word = entry.get()
    lang = language_var.get()
    translated_word = translate(word, lang)
    result_label.config(text=f"翻译结果：\n{translated_word}")

translate_button = tk.Button(root, text="翻译", font=("Arial", 14), command=show_translation)
translate_button.pack(pady=20)

languages_dict = My_Dict.load_dict()
root.mainloop()
