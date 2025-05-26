import re

def remove_emojis(text):
    # Remove emojis by filtering out Unicode symbols in Emoji ranges
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


text = remove_emojis("\ud83c\udd95 | #\u062e\u0628\u0631_\u062c\u062f\u06cc\u062f\n\ud83d\udd38 | \u0628\u0644\u0648\u067e\u0631\u06cc\u0646\u062a\u200c\u0647\u0627\u06cc \u0644\u062c\u0646\u062f\u0631\u06cc \u0641\u0635\u0644 \u0647\u0634\u062a\u0645 :\n\u2734\ufe0f | dr-h - ???\n\u2734\ufe0f | kilo 141 - ???\n\u2734\ufe0f | zrg 20mm - ???\n\u2734\ufe0f | ppsh-41 - ???\n\u2734\ufe0f | butterfly knife - ???\n\ud83c\udd95 #news | #codm #s8 #ld\n\ud83c\udfae channel: @callofdutymobile")
print(text.encode('unicode_escape').decode('ascii'))