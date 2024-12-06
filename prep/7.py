import json
import pandas as pd

def extract_post_features(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Prepare a list to store extracted features
    post_features = []
    
    # Iterate through each post in the JSON
    for post in data.get('posts', []):  # Adjust key if needed
        post_id = post.get('id')
        category_id = post.get('category', {}).get('id')
        title = post.get('title')
        video_link = post.get('video_link')
        
        # Extract emotions from post_summary
        emotions = post.get('post_summary', {}).get('emotions', {})
        print(type(emotions))
        # Create a row for each emotion
        for emotion in emotions:
            post_features.append({
                'id': post_id,
                'category_id': category_id,
                'title': title,
                'video_link': video_link,
                'emotion': emotion
            })
    
    # Create a DataFrame
    df = pd.DataFrame(post_features)
    
    return df

# Usage example
json_file_path = '../data/all_posts.json'
df = extract_post_features(json_file_path)

# Save to CSV
df.to_csv('../data/posts_features.csv', index=False)

# Display first few rows to verify
print(df.head())
