
import re
message ='Мне сколько раз повторять что на этой неделе не будет? Мне сколько раз повторять что на этой неделе не будет?'


message = (message or "").lower()

words = re.findall(r"[а-яё]+", message)  # достаём только русские слова

print(len(words))