# Recommendation System for filtering videos
--------------------------------------------------------------------
## APIs
Get All Viewed Posts:

`https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if`

Get All Liked Posts:

```https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if```

Get All Inspired posts:

```https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if```

Get All Rated posts:

```https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if```

Get All Posts (Header required*):

```https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000```

Get All Users (Header required*):

```https://api.socialverseapp.com/users/get_all?page=1&page_size=1000```

Authorization
For autherization pass Flic-Token as header in the API request:

Header:

```"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"```

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

## findings
- The neural network-based recommendation system relies heavily on user preferences and engagement patterns.

- The heterogeneous nature of emotions in post summaries (emotions in both list and object form) poses a challenge for cleanly extracting emotional data. This requires further preprocessing and normalization to ensure that emotions are captured consistently.



## Approach
- The data preparation steps involved:
    - Loading the data from the endpoints provided in the README
    - Convert all dataframes into CSV and saved it in *'./data'*
    - Saved Posts and Users data in my MongoDB localhost database named the database as expressverse.
    - Prepared the data for collaborative filtering in *collaborative.py* by joining liked_posts.csv and inspired_posts.csv by outer join and saved it in that directory.


