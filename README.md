# Recommendation System for filtering videos
--------------------------------------------------------------------
## Dataset APIs

**Get All Viewed Posts:**

```
https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
```

**Get All Liked Posts:**

```
https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
```


**Get All Inspired posts:**

```
https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
```

**Get All Rated posts:**

```
https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
```

**Get All Posts (Header required*):**

```
https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000
```

**Get All Users (Header required*):**

```
https://api.socialverseapp.com/users/get_all?page=1&page_size=1000
```

Authorization
For autherization pass Flic-Token as header in the API request:

**Header:**

```
"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
```

--------------------------------------------------------------------

## Stack
- Tensorflow
- PyMongo
- Pandas
- NumPy
- SciKit Learn for Label encoders

## Requirements
- *Personalization*: The recommendation algorithm should make personalized suggestions based on user history and engagement patterns.
- *Cold Start Problem Handling*: Include a mechanism to recommend videos for new users without prior interaction history (hint: you can use user mood here).
--------------------------------------------------------------------

## Findings
- The neural network-based recommendation system relies heavily on user preferences and engagement patterns.

- The heterogeneous nature of emotions in post summaries (emotions in both list and object form) poses a challenge for cleanly extracting emotional data. This requires further preprocessing and normalization to ensure that emotions are captured consistently.



## Approach
- The data preparation steps involved:
    - Loading the data from the endpoints provided in the README
    - Convert all dataframes into CSV and saved it in ['./data'](https://github.com/Vishwa2684/video-recommendation-system/tree/main/data)
    - Saved Posts and Users data in my MongoDB localhost database named the database as expressverse.
    - Prepared the data for collaborative filtering in [collaborative.py](https://github.com/Vishwa2684/video-recommendation-system/blob/main/model/collaborative.py) by joining liked_posts.csv and inspired_posts.csv by outer join and saved it in that directory.

- Then encode user id and post id

- In our problem post_id, user_id are categorical feature

- My model predicts the posts by considering user_id as an input along with view and like value of the post

- Then i built a simple neural network for collaborative filtering implementing matrix factorization

## Neural Network Architecture

The recommendation system utilizes a Matrix Factorization-based Collaborative Filtering model built using TensorFlow to predict user engagement with posts. Here's how the architecture works:

1. Input layers:
    The model uses three inputs:

    - User Input: The user ID, which indicates which user is interacting with the posts.
    - Post Input: The post ID, representing the post with which the user is interacting.
    - Interaction Input: This input contains two values that represent the - interaction types:
    - Whether the user liked the post (represented as 1).
    - Whether the user has viewed the post (represented as 0).

2. Embedding Layers:
    To represent users and posts in a more efficient way, both the user ID and post ID are passed through embedding layers. These embeddings transform the sparse categorical data into dense vector representations of users and posts.
    
    - User Embedding: This layer learns an embedding vector for each user.
    
    - Post Embedding: This layer learns an embedding vector for each post.

3. Combined Features:
    After embedding and flattening, the model combines the user embeddings, post embeddings, and interaction features (viewed/liked information) into a single vector. This combined vector is passed through the subsequent layers for prediction.

4. Hidden Layers:
    To learn non-linear patterns between the combined features, the model has two fully connected hidden layers:

    - The first hidden layer has 128 neurons with ReLU activation, followed by Dropout (50%) for regularization.
    - The second hidden layer has 64 neurons with ReLU activation and Dropout (30%) to prevent overfitting.

5. Output Layer:
    The final layer of the model is a Dense Layer with a softmax activation function. This layer outputs the predicted interaction scores for each post, which indicates the likelihood that the user will interact with the post.

6. Custom Loss Function (RMSE)
    The model uses Root Mean Squared Error (RMSE) as the loss function, which is calculated using the following formula:
        \text{RMSE}(y, \hat{y}) = \sqrt{\frac{\sum_{i=0}^{N - 1} (y_i - \hat{y}_i)^2}{N}}

The code of Matrix Factorization is present in [model/collaborative.py](https://github.com/Vishwa2684/video-recommendation-system/blob/main/model/collaborative.py)