from transformers import AutoTokenizer
local_path = "/Users/mohammadmahdi/Documents/LifeWeb/ai_modules/ner"
tok = AutoTokenizer.from_pretrained(local_path)
text = "\ud83c\udd95 | #\u062e\u0628\u0631_\u062c\u062f\u06cc\u062f\n\ud83d\udd38 | \u0628\u0644\u0648\u067e\u0631\u06cc\u0646\u062a\u200c\u0647\u0627\u06cc \u0644\u062c\u0646\u062f\u0631\u06cc \u0641\u0635\u0644 \u0647\u0634\u062a\u0645 :\n\u2734\ufe0f | dr-h - ???\n\u2734\ufe0f | kilo 141 - ???\n\u2734\ufe0f | zrg 20mm - ???\n\u2734\ufe0f | ppsh-41 - ???\n\u2734\ufe0f | butterfly knife - ???\n\ud83c\udd95 #news | #codm #s8 #ld\n\ud83c\udfae channel: @callofdutymobile"
tokens = tok(text, add_special_tokens=True)
print("Tokens:", len(tokens["input_ids"]))