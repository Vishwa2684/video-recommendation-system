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

