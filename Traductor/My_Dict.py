# "": {"en": {"word": "", "pos": "", "gender": None}, "created": {"word": "", "pos": "", "gender": ""}},
# "en" English "ch" 中文 
# word 单词原型 
# pos 词类 noun adj adv v
# gender 词性 der-masculine die-feminine das-neuter 默认英语没有

# 按词性分类的字典，名词包含性别和复数形式信息（去掉英语部分）
import json

DICT_FILE = "My_Dict.json"

languages_dict = {
    "zh": {
        "noun": {
            "水": {"translation": "Aqua", "gender": "n", "plural": ""},
            
        },
        "adj": {
            "大": "",
            
        },
        "adv": {
            "快速地": "",
        },
        "v": {
            "吃": "",
        }
    },
    "created": {
        "noun": {
            "Aqua": {"translation": "水", "gender": "n", "plural": "Aquas"},
        },
        "adj": {
            "zuri": "大",
        },
        "adv": {
            "taza": "",
        },
        "v": {
            "taza": "",
        }
    }
}

# 打印整个字典
#print(languages_dict)

# 加载 JSON 数据
def load_dict():
    global languages_dict
    try:
        with open(DICT_FILE, "r", encoding="utf-8") as f:
            languages_dict = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        languages_dict = {}  # 如果 JSON 文件不存在，则创建一个空字典
    return languages_dict

# 保存到 JSON
def save_dict():
    with open(DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(languages_dict, f, ensure_ascii=False, indent=4)

# 添加单词（修改词典时自动保存）
def add_word(lang, category, word, translation, gender=None, plural=None):
    if lang not in languages_dict:
        languages_dict[lang] = {}
    if category not in languages_dict[lang]:
        languages_dict[lang][category] = {}

    languages_dict[lang][category][word] = {
        "translation": translation
    }
    if gender:
        languages_dict[lang][category][word]["gender"] = gender
    if plural:
        languages_dict[lang][category][word]["plural"] = plural

    save_dict()  # **每次修改后自动保存！**

# 删除单词（修改后自动保存）
def delete_word(lang, word):
    if lang in languages_dict:
        for category in languages_dict[lang]:  # 遍历所有类别
            if word in languages_dict[lang][category]:
                del languages_dict[lang][category][word]
                save_dict()  # **修改后保存**
                return True
    return False  # 如果找不到单词，返回 False

# **初始化：启动时加载 JSON**
load_dict()