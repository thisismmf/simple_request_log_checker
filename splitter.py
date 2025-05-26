import os
import re

LOGS_DIR = "logs"
OUPUTS_DIR = "outputs"


def count_tokens(s: str) -> int:
    """Count tokens by splitting on whitespace."""
    return len(s.split())


def process_file(input_path: str, output_path: str):
    # 1) Read raw bytes and decode latin-1
    with open(input_path, "rb") as f:
        raw_data = f.read().decode("latin-1")

    # 2) Extract the [...] list block
    m = re.search(r"\[(.*)\]", raw_data, re.DOTALL)
    if not m:
        raise ValueError(f"No valid list found in {input_path}")
    list_content = m.group(1).strip()

    # 3) Manual list parsing (handles both ' and " and escapes)
    items = []
    current = []
    in_quotes = False
    quote_char = None
    escape = False

    for c in list_content:
        if escape:
            current.append(c)
            escape = False
        elif c == "\\":
            current.append(c)
            escape = True
        elif c in ('"', "'"):
            if not in_quotes:
                in_quotes = True
                quote_char = c
            elif c == quote_char:
                in_quotes = False
            current.append(c)
        elif c == "," and not in_quotes:
            items.append("".join(current).strip())
            current = []
        else:
            current.append(c)
    if current:
        items.append("".join(current).strip())

    # 4) Process each item: strip quotes, measure length & tokens
    processed = []
    max_len = 0
    max_tok = 0

    for it in items:
        if (it.startswith('"') and it.endswith('"')) or (it.startswith("'") and it.endswith("'")):
            it = it[1:-1]

        length = len(it)
        tokens = count_tokens(it)
        processed.append((it, length, tokens))

        if length > max_len:
            max_len = length
        if tokens > max_tok:
            max_tok = tokens

    # 5) Write out results in latin-1 encoding
    with open(output_path, "wb") as f_out:
        for idx, (it, length, tokens) in enumerate(processed, 1):
            block = (
                f"{idx}:\n"
                f"\"{it}\"\n"
                f"Length: {length}\n"
                f"Tokens: {tokens}\n\n"
            ).encode("latin-1")
            f_out.write(block)

        summary = (
            f"\nMaximum length: {max_len}\n"
            f"Maximum tokens: {max_tok}\n"
        ).encode("latin-1")
        f_out.write(summary)

    print(f"Processed {os.path.basename(input_path)} → {os.path.basename(output_path)}")


def main():
    os.makedirs(OUPUTS_DIR, exist_ok=True)

    # only top-level .json files
    for fname in os.listdir(LOGS_DIR):
        if not fname.lower().endswith(".json"):
            continue
        in_path = os.path.join(LOGS_DIR, fname)
        if not os.path.isfile(in_path):
            continue

        out_fname = "output_" + fname + ".txt"
        out_path = os.path.join(OUPUTS_DIR, out_fname)
        process_file(in_path, out_path)


if __name__ == "__main__":
    main()
