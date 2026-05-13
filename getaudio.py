import requests
import urllib.parse
import os
import time
import json

# Settings
JSON_FILE = "a1_combined.json"  # The file created by the previous script
OUTPUT_FOLDER = "audio_files"
AUDIO_BASE_URL = "https://api.openrussian.org/audio/ru/"

def download_all_audio():
    # 1. Load your combined JSON
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {JSON_FILE} not found. Run the JSON scraper first!")
        return

    entries = data.get("result", {}).get("entries", [])
    total = len(entries)
    
    # 2. Create the output folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created folder: {OUTPUT_FOLDER}")

    print(f"Starting download of {total} audio files...")

    # 3. Iterate and download
    for index, entry in enumerate(entries, 1):
        accented_word = entry.get("accented")
        bare_word = entry.get("bare")

        if not accented_word:
            continue

        # URL encode the accented word (handles characters like ')
        encoded_word = urllib.parse.quote(accented_word)
        file_url = f"{AUDIO_BASE_URL}{encoded_word}"
        
        # Clean filename: use the 'bare' word to avoid filesystem issues with '
        filename = os.path.join(OUTPUT_FOLDER, f"{bare_word}.mp3")

        # Skip if already downloaded (handy if the script crashes)
        if os.path.exists(filename):
            print(f"[{index}/{total}] Skipping {bare_word} (already exists)")
            continue

        try:
            response = requests.get(file_url, stream=True)
            
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"[{index}/{total}] Downloaded: {bare_word}")
            else:
                print(f"[{index}/{total}] [!] Failed: {bare_word} (Status: {response.status_code})")

            # Be nice to the server - wait half a second between downloads
            time.sleep(0.5)

        except Exception as e:
            print(f"[{index}/{total}] [!] Error downloading {bare_word}: {e}")

    print("\n--- All Done! ---")
    print(f"Files are located in the '{OUTPUT_FOLDER}' directory.")

if __name__ == "__main__":
    download_all_audio()