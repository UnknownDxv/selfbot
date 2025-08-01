def text_to_emojis(text: str) -> list[str]:
    '''Convert text to actual emoji characters'''
    emoji_list = []
    for char in text.lower():
        if char.isalpha():
            emoji_list.append(chr(0x1F1E6 + ord(char) - ord('a')))
        elif char.isdigit():
            num_map = {
                "0": "0️⃣",
                "1": "1️⃣",
                "2": "2️⃣",
                "3": "3️⃣",
                "4": "4️⃣",
                "5": "5️⃣",
                "6": "6️⃣",
                "7": "7️⃣",
                "8": "8️⃣",
                "9": "9️⃣",
            }
            emoji_list.append(num_map[char])
        elif char == "!":
            emoji_list.append("❗")
        elif char == "?":
            emoji_list.append("❓")
    return emoji_list