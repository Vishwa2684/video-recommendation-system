# Video Recommendation System

## Overview
A sophisticated recommendation system designed to provide personalized video suggestions using machine learning techniques.

## Technology Stack
- **Machine Learning:** TensorFlow
- **Backend:** Flask
- **Database:** PyMongo
- **Data Processing:** 
  - Pandas
  - NumPy
  - SciKit Learn

## Key Requirements
1. **Personalization**
   - Generate recommendations based on individual user history and engagement patterns
   - Provide tailored content suggestions

2. **Cold Start Problem Handling**
   - Implement mechanisms to recommend videos for new users
   - Utilize user mood and initial interactions as recommendation signals

## Dataset APIs

### Authentication
**Header Authentication**
```
"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
```

### Available Endpoints
| Endpoint | Description | URL |
|----------|-------------|-----|
| Viewed Posts | Retrieve viewed posts | `https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=...` |
| Liked Posts | Retrieve liked posts | `https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=...` |
| Inspired Posts | Retrieve inspired posts | `https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=...` |
| Rated Posts | Retrieve rated posts | `https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=...` |
| All Posts | Retrieve all posts (header required) | `https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000` |
| All Users | Retrieve all users (header required) | `https://api.socialverseapp.com/users/get_all?page=1&page_size=1000` |

## Neural Network Architecture

### Model Components
1. **Input Layers**
   - User Input (User ID)
   - Post Input (Post ID)
   - Interaction Input (Like/View status)

2. **Embedding Layers**
   - User Embedding: Dense vector representation of users
   - Post Embedding: Dense vector representation of posts

3. **Feature Processing**
   - Combine user embeddings, post embeddings, and interaction features
   - Pass through hidden layers for non-linear pattern learning

4. **Neural Network Structure**
   - First Hidden Layer: 128 neurons with ReLU activation
     - Dropout (50%) for regularization
   - Second Hidden Layer: 64 neurons with ReLU activation
     - Dropout (30%) to prevent overfitting
   - Output Layer: Softmax activation for interaction score prediction

5. **Loss Function**
   Root Mean Squared Error (RMSE):
   ### $RMSE(y, \hat{y}) = \sqrt{\frac{\sum_{i=0}^{N - 1} (y_i - \hat{y}_i)^2}{N}}$

## Data Preparation

### Initial Setup
1. Create a `data` folder
2. Run preparation scripts:
   ```bash
   cd prep
   python 1.py
   python 2.py
   python 3.py
   python 4.py
   python 5.py
   python 6.py
   ```

### Data Processing Steps
- Save Posts and Users data in MongoDB (database: expressverse)
- Prepare collaborative filtering data by joining liked_posts.csv and inspired_posts.csv
- Encode user and post IDs
- Implement categorical feature handling

## Model Training and Validation

### Training the Model
```bash
cd model
python collaborative.py
```

### Validating Model Performance
```bash
python collaborative_val.py
```

## API Usage

### Running the API
```bash
cd api
python api.py
```

### API Initialization Process
1. **Model Loading**
   - Load pre-trained recommendation model (simple_content_based.h5)
   - Initialize custom RMSE loss function

2. **Dataset Preparation**
   - Load dataset from `../model/dataset_for_contbased.csv`
   - Preprocess and encode user/post IDs

3. **Encoder Preparation**
   - Apply LabelEncoder to user and post IDs
   - Create encoded columns for model input

4. **Post Embeddings Preparation**
   ```python
   post_embeddings = np.array(df['post_id_encoded'].tolist())
   ```
   - Create NumPy array of post embeddings
   - Currently uses encoded post IDs as placeholders
   - Can be replaced with pre-trained embeddings if available

5. **MongoDB Connection Setup**
   ```python
   uri = "mongodb://localhost:27017/"
   client = MongoClient(uri)
   db = client['expressverse']
   ```
   - Connects to local MongoDB instance
   - Selects 'expressverse' database
   - Accesses users and posts collections

### API Endpoints

#### Recommendation Feed Endpoints
| Endpoint | Description | URL |
|----------|-------------|-----|
| Basic Feed | Get recommendations for a user | `http://localhost:8080/feed?username=your_username` |
| Category-Specific Feed | Get recommendations for a specific category | `http://localhost:8080/feed?username=your_username&category_id=category_id_user_want_to_see` |
| Mood-Based Feed | Get recommendations based on user mood | `http://localhost:8080/feed?username=your_username&category_id=category_id_user_want_to_see&mood=user_current_mood` |

#### Endpoint Parameters
- `username`: Required parameter identifying the user
- `category_id`: Optional parameter to filter recommendations by content category
- `mood`: Optional parameter to personalize recommendations based on user's current emotional state

### Key Initialization Steps
1. Load recommendation model
2. Prepare dataset with encoded IDs
3. Set up MongoDB connection
4. Prepare post embeddings
5. Initialize recommendation generation logic

The API is designed to provide personalized content recommendations by:
- Analyzing user interaction history
- Considering user mood and preferences
- Utilizing machine learning embeddings
- Filtering by content categories

## Key Findings
- Neural network recommendation system relies heavily on user preferences
- Challenges exist in processing heterogeneous emotional data in post summaries
- Requires advanced preprocessing and normalization techniques

## Contribution
Feel free to contribute, report issues, or suggest improvements!