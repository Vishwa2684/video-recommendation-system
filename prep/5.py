import requests
import pandas as pd
import requests
import pandas as pd
import os
import json

# Direct URL with parameters included
url = "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
output_dir = "../data/"
csv_path = os.path.join(output_dir, "all_posts.csv")
json_path = os.path.join(output_dir, "all_posts.json")

# Make the GET request
try:
    # Request with headers
    response = requests.get(
        url,
        headers={
            "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
        },
    )
    response.raise_for_status()
    
    # Parse JSON response
    data = response.json()
    posts = data.get('posts', [])
    print("JSON data received successfully:")
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save JSON response to a file
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON data saved to {json_path}")
    
    # Convert posts to DataFrame and save as CSV
    if posts:
        df = pd.DataFrame(posts)
        df.to_csv(csv_path, index=False)
        print(f"CSV data saved to {csv_path}")
    else:
        print("No posts data to save.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except ValueError as ve:
    print(f"Data processing error: {ve}")
