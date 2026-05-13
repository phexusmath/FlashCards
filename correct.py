import os
import json
import requests
import time

# Folder where your "JSON-disguised-as-MP3" files are
AUDIO_FOLDER = "audio_files"

def fix_audio_files():
    if not os.path.exists(AUDIO_FOLDER):
        print(f"Error: Folder '{AUDIO_FOLDER}' not found.")
        return

    files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
    total = len(files)
    
    print(f"Found {total} files. Checking for JSON metadata...")

    for index, filename in enumerate(files, 1):
        filepath = os.path.join(AUDIO_FOLDER, filename)
        
        try:
            # 1. Read the file to see if it's JSON or actual MP3 data
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(1000) # Just read the beginning
            
            # 2. Check if it looks like the JSON you shared
            if '{"result":' in content:
                data = json.loads(content)
                real_url = data.get("result", {}).get("url")
                
                if real_url:
                    print(f"[{index}/{total}] Fixing {filename}...")
                    
                    # 3. Download the actual binary MP3 data
                    audio_response = requests.get(real_url)
                    
                    if audio_response.status_code == 200:
                        # 4. Overwrite the file with actual binary data
                        with open(filepath, "wb") as f_out:
                            f_out.write(audio_response.content)
                    else:
                        print(f"  [!] Failed to download audio for {filename}")
                else:
                    print(f"  [!] No URL found inside JSON for {filename}")

            else:
                # If it doesn't contain '{"result":', it's probably already a real MP3
                print(f"[{index}/{total}] Skipping {filename} (Already a real MP3)")

        except (json.JSONDecodeError, UnicodeDecodeError):
            # If it can't be read as text/JSON, it's a binary MP3. Skip it.
            print(f"[{index}/{total}] Skipping {filename} (Already binary data)")
        except Exception as e:
            print(f"[{index}/{total}] Error processing {filename}: {e}")

    print("\n--- Repair Complete! ---")
    print("Your 'audio_files' folder should now contain playable MP3s.")

if __name__ == "__main__":
    fix_audio_files()