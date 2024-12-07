## Validation script 

import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from pymongo import MongoClient

def load_validation_data(liked_posts_path, viewed_posts_path, categories, db):
    # Load and preprocess data similar to training script
    liked_posts = pd.read_csv(liked_posts_path)
    viewed_posts = pd.read_csv(viewed_posts_path)

    liked_posts['liked'] = 1
    viewed_posts['viewed'] = 1
    liked_posts = liked_posts[['post_id', 'user_id', 'liked']]
    viewed_posts = viewed_posts[['post_id', 'user_id', 'viewed']]

    merged = pd.merge(viewed_posts, liked_posts, on=['post_id', 'user_id'], how='outer')
    merged['liked'] = merged['liked'].fillna(0).astype(int)
    merged['viewed'] = merged['viewed'].fillna(0).astype(int)

    merged['category'] = merged['post_id'].map(lambda post_id: 
        categories[db['posts'].find_one({'id': post_id})['category']['id']])

    return merged

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

def main():
    # MongoDB and data configuration
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    db = client['expressverse']

    categories = {2: "Vible", 4: "E/ACC", 3: "The Igloo", 5: "Gratitube", 
                  18: "Startup College", 6: "InstaRama", 20: "OvaDrive", 
                  21: "Pumptok", 22: "SolTok", 13: "Flic"}

    # Load validation data
    validation_data = load_validation_data(
        "../data/liked_posts.csv", 
        "../data/viewed_posts.csv", 
        categories, 
        db
    )

    # Encode validation data (same as training script)
    user_encoder = LabelEncoder()
    post_encoder = LabelEncoder()

    validation_data['user_id_encoded'] = user_encoder.fit_transform(validation_data['user_id'])
    validation_data['post_id_encoded'] = post_encoder.fit_transform(validation_data['post_id'])

    # Path to saved model
    model_path = '../api/simple_content_based.h5'

    # Validate the model
    validate_model(model_path, validation_data, user_encoder, post_encoder)

if __name__ == "__main__":
    main()