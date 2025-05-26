import os
import json
import time
import requests

# configuration
LOGS_DIR = "logs"
RESULTS_DIR = "results"
URL = "http://192.168.10.62/predictions/ner/"
HEADERS = {
    'Authorization': 'Basic YWk6MTI1NDYzOTc4',
    'Content-Type': 'application/json'
}
SLEEP_SECONDS = 10


def process_file(input_path: str, output_path: str):
    """Read a JSON list from input_path, send each item to the NER endpoint,
    collect responses, and write them out to output_path."""
    # load input
    with open(input_path, "r", encoding="utf-8") as f:
        data_list = json.load(f)

    results = []
    for idx, element in enumerate(data_list, start=1):
        payload = json.dumps([element], ensure_ascii=False)
        print(f"[{os.path.basename(input_path)}] → item {idx}/{len(data_list)}: sending…")
        try:
            resp = requests.post(URL, headers=HEADERS, data=payload)
            resp.raise_for_status()
            result_text = resp.text
        except Exception as e:
            result_text = f"Error: {e}"

        results.append(f"{idx}:\n{result_text}\n\n")

        # wait before next request
        if idx < len(data_list):
            print(f"Sleeping for {SLEEP_SECONDS} seconds…")
            time.sleep(SLEEP_SECONDS)

    # write output
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.writelines(results)

    print(f"✔ Done with {os.path.basename(input_path)} → {output_path}")


def main():
    # ensure results directory exists
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # list all .json files directly under logs/
    for fname in os.listdir(LOGS_DIR):
        if not fname.lower().endswith(".json"):
            continue
        input_path = os.path.join(LOGS_DIR, fname)
        if not os.path.isfile(input_path):
            continue

        # build output filename: e.g. foo.json → foo.json.txt
        output_fname = "result_" + fname + ".txt"
        output_path = os.path.join(RESULTS_DIR, output_fname)

        process_file(input_path, output_path)


if __name__ == "__main__":
    main()
