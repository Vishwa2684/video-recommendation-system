from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

import pandas as pd
from pymongo import MongoClient
import numpy as np
import random


# Setting up connection to the database
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client['expressverse']

# Loading dataset and model
df = pd.read_csv('../model/dataset_for_contbased.csv')
model = load_model('./simple_content_based.h5',custom_objects={
        'custom_rmse': lambda y_true, y_pred: tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))
    })

# Preparing encoders for users and posts
user_encoder = LabelEncoder()
df['user_id_encoded'] = user_encoder.fit_transform(df['user_id'])

post_encoder = LabelEncoder()
df['post_id_encoded'] = post_encoder.fit_transform(df['post_id'])

# Storing post embeddings (ensure the model generates embeddings)
post_embeddings = np.array(df['post_id_encoded'].tolist())  # Replace with actual embeddings if available

# Debug line
print('connected to mongodb and loaded model')


## FUNCTION TO VALIDATE THE MODEL

def validate_model(model_path, validation_data, user_encoder, post_encoder):
    # Load the saved model
    model = tf.keras.models.load_model(model_path, custom_objects={
        'custom_rmse': lambda y_true, y_pred: tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))
    })

    # Prepare validation data
    X_user = validation_data['user_id_encoded'].values
    X_post = validation_data['post_id_encoded'].values
    X_interaction = validation_data[['liked', 'viewed']].values
    y = tf.keras.utils.to_categorical(validation_data['post_id_encoded'])

    # Evaluate the model
    loss, accuracy = model.evaluate(
        [X_user, X_post, X_interaction], 
        y, 
        verbose=1
    )

    print(f"Validation Loss: {loss}")
    print(f"Validation Accuracy: {accuracy}")

    # Optional: Predict top-k recommendations
    predictions = model.predict([X_user, X_post, X_interaction])
    top_k_recommendations = np.argsort(predictions, axis=1)[:, -10:]
    
    # Convert back to original post IDs
    original_post_ids = post_encoder.inverse_transform(top_k_recommendations[0])
    print("Top 10 Recommended Post IDs:", original_post_ids)




app = Flask(__name__)

@app.get('/')
def greet():
    return {"message": "Hi there"}

@app.get('/feed')
def feed():
    try:
        # Get username from query parameters
        username = request.args.get('username')
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

            # Prepare input tensor for prediction
            input_tensor = np.array([[user_id_encoded[0], liked, viewed]])
            predicted_post_ids_encoded = model.predict(input_tensor)

            # Decode the predicted post_id
            predicted_post_ids = post_encoder.inverse_transform(predicted_post_ids_encoded.argmax(axis=1))
            predicted_post_id = int(predicted_post_ids[0])  # Convert numpy.int64 to int

            print("Predicted ID is:", predicted_post_id)

            # Fetch the corresponding post from the database
            response_post = db.posts.find_one({'id': predicted_post_id})

            # Ensure response is JSON serializable
            if response_post:
                response_post['_id'] = str(response_post['_id'])  # Convert ObjectId to string if needed
                return jsonify(response_post), 200
            else:
                return {'message': 'No post found for the predicted ID'}, 404
        else:
            # If username not found in the database, return a random selection of 10 posts
            random_posts = list(db.posts.aggregate([{"$sample": {"size": 10}}]))  # Random 10 posts
            for post in random_posts:
                post['_id'] = str(post['_id'])  # Convert ObjectId to string if needed
            return jsonify(random_posts), 200

    except Exception as e:
        print(f'{e.args[0]} at line number: {e.__traceback__.tb_lineno}')
        return {'message': 'An error occurred while processing your request'}, 500


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
