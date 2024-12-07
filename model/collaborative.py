import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers #type:ignore
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from pymongo import MongoClient

def prepare_data(liked_posts, viewed_posts, categories, db):
    liked_posts['liked'] = 1
    viewed_posts['viewed'] = 1
    liked_posts = liked_posts[['post_id', 'user_id', 'liked']]
    viewed_posts = viewed_posts[['post_id', 'user_id', 'viewed']]

    merged = pd.merge(viewed_posts, liked_posts, on=['post_id', 'user_id'], how='outer')
    merged['liked'] = merged['liked'].fillna(0).astype(int)
    merged['viewed'] = merged['viewed'].fillna(0).astype(int)

    merged['category'] = merged['post_id'].map(lambda post_id: 
        categories[db['posts'].find_one({'id': post_id})['category']['id']])
    merged.to_csv('./dataset_for_collaborative.csv')
    return merged

def create_matrix_factorization_model(num_users, num_posts, embedding_dim=50):
    # User embedding
    user_input = layers.Input(shape=(1,), name='user_input')
    user_embedding = layers.Embedding(
        input_dim=num_users, 
        output_dim=embedding_dim, 
        embeddings_regularizer=regularizers.l2(1e-6),
        name='user_embedding'
    )(user_input)

    # Post embedding
    post_input = layers.Input(shape=(1,), name='post_input')
    post_embedding = layers.Embedding(
        input_dim=num_posts, 
        output_dim=embedding_dim, 
        embeddings_regularizer=regularizers.l2(1e-6),
        name='post_embedding'
    )(post_input)

    # Additional interaction features
    interaction_input = layers.Input(shape=(2,), name='interaction_input')

    # Flatten embeddings
    user_embedding_flat = layers.Flatten()(user_embedding)
    post_embedding_flat = layers.Flatten()(post_embedding)

    # Combine embeddings and interaction features
    combined = layers.concatenate([
        user_embedding_flat, 
        post_embedding_flat, 
        interaction_input
    ])

    # Hidden layers with dropout for regularization
    x = layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(1e-5))(combined)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(1e-5))(x)
    x = layers.Dropout(0.3)(x)

    # Output layer
    output = layers.Dense(num_posts, activation='softmax')(x)

    # Create model
    model = models.Model(
        inputs=[user_input, post_input, interaction_input], 
        outputs=output
    )

    # Custom loss function (improved RMSE)
    def custom_rmse(y_true, y_pred):
        return tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))

    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=custom_rmse,
        metrics=['accuracy']
    )

    return model

def main():
    # Your existing data loading and preprocessing
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)

    liked_posts = pd.read_csv("../data/liked_posts.csv")
    viewed_posts = pd.read_csv("../data/viewed_posts.csv")

    categories = {2: "Vible", 4: "E/ACC", 3: "The Igloo", 5: "Gratitube", 
                  18: "Startup College", 6: "InstaRama", 20: "OvaDrive", 
                  21: "Pumptok", 22: "SolTok", 13: "Flic"}
    db = client['expressverse']

    merged = prepare_data(liked_posts, viewed_posts, categories, db)

    # Encoding
    user_encoder = LabelEncoder()
    post_encoder = LabelEncoder()

    merged['user_id_encoded'] = user_encoder.fit_transform(merged['user_id'])
    merged['post_id_encoded'] = post_encoder.fit_transform(merged['post_id'])

    # Prepare inputs
    X_user = merged['user_id_encoded'].values
    X_post = merged['post_id_encoded'].values
    X_interaction = merged[['liked', 'viewed']].values
    y = tf.keras.utils.to_categorical(merged['post_id_encoded'])

    # Split data
    X_user_train, X_user_test, X_post_train, X_post_test, \
    X_interaction_train, X_interaction_test, \
    y_train, y_test = train_test_split(
        X_user, X_post, X_interaction, y, 
        test_size=0.2, random_state=42
    )

    # Create and train model
    model = create_matrix_factorization_model(
        num_users=len(user_encoder.classes_),
        num_posts=len(post_encoder.classes_)
    )

    # Early stopping and model checkpointing
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', 
        patience=10, 
        restore_best_weights=True
    )

    model.fit(
        [X_user_train, X_post_train, X_interaction_train], 
        y_train,
        validation_data=(
            [X_user_test, X_post_test, X_interaction_test], 
            y_test
        ),
        epochs=500,
        batch_size=32,
        callbacks=[early_stopping]
    )

    return model, user_encoder, post_encoder

if __name__ == "__main__":
    model, user_encoder, post_encoder = main()
    model.save('../api/simple_content_based.h5')