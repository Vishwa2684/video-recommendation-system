reccom algo based on user preferences and engagement patterns

APIs
Get All Viewed Posts:

https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
Get All Liked Posts:

https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
Get All Inspired posts:

https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
Get All Rated posts:

https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
Get All Posts (Header required*):

https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000
Get All Users (Header required*):

https://api.socialverseapp.com/users/get_all?page=1&page_size=1000
Authorization
For autherization pass Flic-Token as header in the API request:

Header:

"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"


--------------------------------------------------------------------

PREPARED DATA WITH ALL THE FILES PRESENT IN PREP FOLDER

--------------------------------------------------------------------
PREPARED POST CATEGORIES
--------------------------------------------------------------------

## Requirements
- *Personalization*: The recommendation algorithm should make personalized suggestions based on user history and engagement patterns.
- *Cold Start Problem Handling*: Include a mechanism to recommend videos for new users without prior interaction history (hint: you can use user mood here).
--------------------------------------------------------------------

## findings
- have to build a rest api for model inference where
    - my input is: username, category_id and mood as query parameters
- i found out that emotions attribute in post summary is hetrogeneous. so im going to struggle with it

## Approach
- First i added all users and posts json data into a mongoDB database
- To build content based filtering system I have picked liked_posts and viewed_posts then joined both of those dataframes then I got the category of each post my mapping through every post id and querying it in Database to check it's category.
- Then the final CSV DataFrame is saved in the working directory.
- Then i built a simple neural network to which takes user id as input view as 0 because user haven't viewed it yet and like as 1 because user may like the following post.
- The neural network gives the output but there's one flaw in it. It gives same output for one user id input and it doesn't handle users who have not liked or seen anything in app.

- I got to fix this issue.

