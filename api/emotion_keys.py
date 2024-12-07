from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['expressverse']
posts_collection = db['posts']

def find_unique_emotion_keys(posts_collection, sample_size=100):
    # Retrieve a sample of documents
    sample_docs = posts_collection.find({}, {"post_summary.emotions": 1}).limit(sample_size)
    
    # Set to store unique emotion keys
    emotion_keys = set()
    
    # Iterate through each document
    for doc in sample_docs:
        emotions = doc.get("post_summary", {}).get("emotions", {})
        
        # If emotions is a dictionary, extract keys
        if isinstance(emotions, dict):
            for key in emotions.keys():
                emotion_keys.add(f"post_summary.emotions.{key}")
        
        # If emotions is a list, check if it's an array of strings (emotions themselves)
        
    
    return emotion_keys

# Call the function and print the unique emotion keys
unique_emotion_keys = find_unique_emotion_keys(posts_collection)
print(len(unique_emotion_keys))
print("Unique Emotion Keys Found:")
for key in unique_emotion_keys:
    print(key)
