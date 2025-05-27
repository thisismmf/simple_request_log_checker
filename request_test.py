import os
import json
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# configuration
LOGS_DIR = "logs"
RESULTS_DIR = "results"
ERRORS_FILE = os.path.join(RESULTS_DIR, "errors.txt")
ERRORS_LOCK = threading.Lock()
URL = "http://192.168.10.62/predictions/ner/"
HEADERS = {
    'Authorization': 'Basic YWk6MTI1NDYzOTc4',
    'Content-Type': 'application/json'
}
SLEEP_SECONDS = 10


def process_file(input_path: str, output_path: str):
    # load input
    with open(input_path, "r", encoding="utf-8") as f:
        data_list = json.load(f)

    results = []

    # first, try sending all elements as one batch
    batch_payload = json.dumps(data_list, ensure_ascii=False)
    try:
        batch_resp = requests.post(URL, headers=HEADERS, data=batch_payload)
        batch_resp.raise_for_status()
        results.append(f"✔ Batch request successful for all {len(data_list)} elements\n")
        results.append(batch_resp.text + "\n")
    except Exception as batch_error:
        # batch request failed: fall back to individual requests
        print(f"Batch request failed: {batch_error}. Falling back to individual requests.")
        for idx, element in enumerate(data_list, start=1):
            payload = json.dumps([element], ensure_ascii=False)
            print(f"[{os.path.basename(input_path)}] → item {idx}/{len(data_list)}: sending…")
            try:
                resp = requests.post(URL, headers=HEADERS, data=payload)
                resp.raise_for_status()
                result_text = resp.text
            except Exception as e:
                result_text = f"Error: {e}"
                # record the error detail
                with ERRORS_LOCK:
                    with open(ERRORS_FILE, "a", encoding="utf-8") as ef:
                        ef.write(f"{os.path.basename(input_path)} : {result_text} : {payload}\n")
            results.append(f"{idx}:\n{result_text}\n\n")
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
    input_files = [
        os.path.join(LOGS_DIR, fname)
        for fname in os.listdir(LOGS_DIR)
        if fname.lower().endswith(".json") and os.path.isfile(os.path.join(LOGS_DIR, fname))
    ]

    # process files in parallel
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for input_path in input_files:
            output_fname = "result_" + os.path.basename(input_path) + ".txt"
            output_path = os.path.join(RESULTS_DIR, output_fname)
            futures.append(executor.submit(process_file, input_path, output_path))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing file: {e}")


if __name__ == "__main__":
    main()
