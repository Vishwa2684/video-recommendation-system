import requests
import pandas as pd
import os

# Direct URL with parameters included
url = "https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"

# Make the GET request
try:
    response = requests.get(url)
    response.raise_for_status()
    
    data = dict(response.json())
    posts = data.get('posts', [])
    print("JSON data received successfully:")
    print(posts)
    df = pd.DataFrame(posts)
    df.to_csv('../data/viewed_posts.csv',index=False)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
