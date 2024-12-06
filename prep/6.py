import requests
import pandas as pd
import os

# Direct URL with parameters included
url = "https://api.socialverseapp.com/users/get_all?page=1&page_size=1000"

# Make the GET request
try:
    response = requests.get(url,headers={
        "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
    })
    response.raise_for_status()
    
    data = dict(response.json())
    posts = data.get('users', [])
    print("JSON data received successfully:")
    print(posts)
    df = pd.DataFrame(posts)
    df.to_csv('../data/all_users.csv',index=False)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
