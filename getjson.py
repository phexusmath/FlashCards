import requests
import json
import time

def scrape_and_combine(level="A1"):
    base_url = "https://api2.openrussian.org/api/wordlists/all"
    combined_entries = []
    start = 0
    total_count = 1  # Placeholder
    
    print(f"Starting scrape for level: {level}")

    while start < total_count:
        # Construct URL with current offset
        params = {
            'start': start,
            'level': level,
            'lang': 'en'
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Update the total count from the first response
            total_count = data['result']['total']
            entries = data['result']['entries']
            
            # Combine the entries list
            combined_entries.extend(entries)
            
            print(f"Fetched words {start} to {start + len(entries)} (Total: {total_count})")
            
            # Increment the offset for the next loop
            start += 50
            
            # Sleep briefly to be respectful to the API
            time.sleep(1) 
            
        except Exception as e:
            print(f"Error during scrape: {e}")
            break

    # Construct the final JSON object to match the original structure
    final_data = {
        "result": {
            "total": len(combined_entries),
            "entries": combined_entries
        },
        "error": None
    }

    # Save to file
    filename = f"{level.lower()}_combined.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"--- Success! ---")
    print(f"Saved {len(combined_entries)} words to {filename}")

if __name__ == "__main__":
    scrape_and_combine("A1")