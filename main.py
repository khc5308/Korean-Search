import json
import re

_cho  = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
_jung = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
_jong = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"

def __search(word:str):
    result = []
    if re.fullmatch(r'[a-z\s]+', word.lower()):
        print("english")
    elif re.fullmatch(r'[ㄱ-ㅎ가-힣\s]+', word):
        print("한국어")
        try:
            ch = cho(word)
            with open('tag.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            print(f"{e}\n")
            return None
        
        for i,j,k in zip(data["tag"],data["split"],data["cho"]):
            # 초성검색
            try: 
                if ch == word: 
                    if (ch in k) and k.startswith(ch):
                        result.append(i)
                #그냥 검색
                elif (word in i) or (split_hangul(word) in j):
                    result.append(i)
                else:
                    pass

                if len(result) > 5:
                    break
            except:
                print(Exception)
                return None

        print("결과")
        return result
    else:
        return "_"

# 안녕 > ㅇㅏㄴㄴㅕㅇ
def split_hangul(word:str):
    len_jung, len_jong = len(_jung), len(_jong)
    result=[]

    for i in word:
        # 초성 하나만 있을 때, 그대로 반환 ex) ㅅ > ㅅ
        if re.fullmatch(r'[가-힣]+', i):
            # 이 외
            try:
                c_number = ord(i) - ord("가")
                
                jong_num = c_number % len_jong
                jung_num = (c_number // len_jong) % len_jung
                cho_num  = (c_number // len_jong) // len_jung
                result.append(_cho[cho_num])
                result.append( _jung[jung_num])
                result.append(_jong[jong_num])
            except:
                print(f"append Exception {i} {Exception}")
        else:
            result.append(i)
    return "".join(result)

# ㅇㅏㄴㄴㅕㅇ > 안녕
def split_to_full(word):
    
    result = ""
    temp = []
    try:
        for i in word:
            temp.append(i)
            # 초성, 중성, 종성을 3개씩 모았을 때
            if len(temp) == 3:
                if temp[1] == " ":
                    result += temp[0]
                    temp = []
                else: 
                    cho, jung, jong = temp
                    temp = []  # 초기화
                    # 조합
                    cho_index = _cho.index(cho)
                    jung_index = _jung.index(jung)
                    jong_index = _jong.index(jong) if jong in _jong else 0
                    # 유니코드 조합
                    code_point = ord("가") + (cho_index * 588) + (jung_index * 28) + jong_index
                    result += chr(code_point)
    
        return result
    except:
        print(Exception)
        return None

# (안녕, 안ㄴ) > True
def hangul_include(big_str:str,small_str):
    try:
        result =  ( all(item in split_hangul(big_str) for item in split_hangul(small_str)) )
        return result
    except:
        print(Exception)
        return None

# 안녕 > ㅇㄴ 
def cho(word:str):
    len_jung, len_jong = len(_jung), len(_jong)
    re=[]
    for i in word:
        if ord("가") <= ord(i) <= ord("힣"): 
            re.append(_cho[((ord(i) - ord("가")) // len_jong) // len_jung])
        else:
            re.append(i)
    return "".join(re)

# dkssud > 안녕
def qwert_to_hangul(word:str):
    qwert_di = {
        "q" : "ㅂ", 
        "w" : "ㅈ",
        "e" : "ㄷ",
        "r" : "ㄱ",
        "t" : "ㅅ",
        "y" : "ㅛ",
        "u" : "ㅕ",
        "i" : "ㅑ",
        "o" : "ㅐ",
        "p" : "ㅔ",
        "a" : "ㅁ",
        "s" : "ㄴ",
        "d" : "ㅇ",
        "f" : "ㄹ",
        "g" : "ㅎ",
        "h" : "ㅗ",
        "j" : "ㅓ",
        "k" : "ㅏ",
        "l" : "ㅣ",
        "z" : "ㅋ",
        "x" : "ㅌ",
        "c" : "ㅊ",
        "v" : "ㅍ",
        "b" : "ㅠ",
        "n" : "ㅜ",
        "m" : "ㅡ",
        " " : " "
    } 
    result = ""
    for i in word:
        result += qwert_di[i]
    return result

# 테스트
print(__search("섹스"))