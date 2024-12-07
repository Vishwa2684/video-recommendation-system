from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model #type:ignore
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

import pandas as pd
from pymongo import MongoClient
import numpy as np

# Setting up connection to the database (You can also use your mongo cloud URI)
uri = "mongodb://localhost:27017/" 
client = MongoClient(uri)
db = client['expressverse']

#############################################################################
# Loading dataset and model
df = pd.read_csv('../model/dataset_for_collaborative.csv')
model = load_model('./simple_content_based.h5', custom_objects={
    'custom_rmse': lambda y_true, y_pred: tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))
})

# Preparing encoders for users and posts
user_encoder = LabelEncoder()
df['user_id_encoded'] = user_encoder.fit_transform(df['user_id'])

post_encoder = LabelEncoder()
df['post_id_encoded'] = post_encoder.fit_transform(df['post_id'])

# Storing post embeddings (ensure the model generates embeddings)
post_embeddings = np.array(df['post_id_encoded'].tolist())  # Replace with actual embeddings if available
#############################################################################
print('connected to mongodb and loaded model')

app = Flask(__name__)

@app.get('/')
def greet():
    return {"message": "Hi there"}

#############################################################################

@app.get('/feed')
def feed():
    try:
        # Get parameters from query
        username = request.args.get('username')
        category_id = int(request.args.get('category_id')) if request.args.get('category_id') else None
        mood = request.args.get('mood')

        if not username:
            return {'message': 'Username is required'}, 400

        # Try to fetch user_id from the database
        user = db.users.find_one({'username': username})

        if user:
            user_id = user['id']
            liked = 1
            viewed = 0

            # Check if the user_id exists in the encoder
            if user_id not in user_encoder.classes_:
                # If user_id is not found in the encoder, return random posts
                random_posts = list(db.posts.aggregate([{"$sample": {"size": 10}}]))  # Random 10 posts
                for post in random_posts:
                    post['_id'] = str(post['_id'])  # Convert ObjectId to string if needed
                return jsonify(random_posts), 200

            # Encode user_id
            user_id_encoded = user_encoder.transform([user_id])

            # Prepare input tensors for the model (separate inputs for each required feature)
            user_input = np.array([user_id_encoded[0]])  # Shape (1,)
            post_input = np.zeros((1,))  # Placeholder for post ID input (unused for prediction here)
            interaction_input = np.array([[liked, viewed]])  # Shape (1, 2)

            # Make predictions
            predicted_post_scores = model.predict([user_input, post_input, interaction_input])

            # Get top 10 recommended post IDs
            top_k_indices = np.argsort(predicted_post_scores, axis=1)[:, -10:]  # Top 10 indices
            predicted_post_ids = post_encoder.inverse_transform(top_k_indices[0])  # Decode indices
            predicted_post_ids_list = predicted_post_ids.tolist()
            print(predicted_post_ids_list)
            # Base query to search for posts
            query = {"id": {"$in": predicted_post_ids_list}}

            # Apply filters based on the category_id and mood (first filtering)
            if category_id and mood:
                query["$and"] = [
                    {"category.id": category_id},
                    {"$or": [{"post_summary.emotions.mood": mood}, {"post_summary.emotions.emotions_conveyed": mood}]}
                ]
            elif category_id:
                query["category.id"] = category_id
            elif mood:
                query["$or"] = [
                    {"post_summary.emotions.mood": mood},
                    {"post_summary.emotions.emotions_conveyed": mood}
                ]

            # Fetch filtered posts based on the query
            recommended_posts = list(db.posts.find(query))

            # Now, check if the number of recommended posts is less than 10
            num_recommended = len(recommended_posts)
            if num_recommended < 10:
                # Fetch additional random posts if needed to fill the gap
                random_posts = list(db.posts.aggregate([{"$sample": {"size": 10 - num_recommended}}]))
                recommended_posts.extend(random_posts)

            # Ensure response is JSON serializable
            for post in recommended_posts:
                post['_id'] = str(post['_id'])  # Convert ObjectId to string if needed

            return jsonify(recommended_posts), 200
        else:
            # If username not found in the database, return a random selection of 10 posts
            random_posts = list(db.posts.aggregate([{"$sample": {"size": 10}}]))  # Random 10 posts
            for post in random_posts:
                post['_id'] = str(post['_id'])  # Convert ObjectId to string if needed
            return jsonify(random_posts), 200

    except Exception as e:
        print(f'{e.args[0]} at line number: {e.__traceback__.tb_lineno}')
        return {'message': 'An error occurred while processing your request'}, 500

#############################################################################

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
