# SI507-FinalProject

### uniquename: yanghan

## Project Goal

*This project is going to scrape recent instagram posts from 5 users and cache them in a database. Then make two queries: one to fetch posts with more than 15 likes, and another to fetch posts with more than 1 tag. Noted that post owner's name should also be associated with the query results.

*It uses OAuth2 authorization to get data via Instagram API.

*It has 2 classes: InsPost and InsUser: as the names represent, the two classes separately process post and user instances for the data I cached from instagram.

*The two types of instances are inserted into two tables in the database called "yanghan_507finalproject". InsUser instances go to table "Users", while InsPost instances go to table "Posts".

*Once all data inserted into database, a flask app will run on the local server to show the results in html.


## To Run This Code
*First, please use ```pip3 install -r requirements.txt``` to install every necessary library.
*Second, create a database named "yanghan_507finalproject"
*Third, use ```python3 SI507F17_finalproject.py``` to run the main code and flask app
*Last, open the browser and you can view my two queries visually in the web browse at http://local:5000/
*Considering Instagram's strict limit, I uploaded my "secret_data.py" onto the Canvas in case it is needed.


## What the Result Looks Like
This is the result you are expected to see:
https://drive.google.com/open?id=1MQ1gmyi7XWZLFNVIIB3cYWuebX0DVm0U



## Limitations(IMPORTANT!)
Instagram only gives limited permissions for test apps using their API. They called it "Sandbox Mode". Apps in Sandbox mode are not visible to the general public, but instead are only visible to a limited set of up to 10 authorized 'sandbox users' who got the app owner's invitation and accepted to test.

Limitations include:

*Data is restricted to the 20 most recent media from each of those users.
*All apps have basic access to get the user's own data, but if I want to get extended access such as reading public content, liking, commenting, or managing friendships, Instagram required me to first submit the app for review. Since my app is just using for test this assignment, getting Instagram's approval is unrealistic.

More information please refer to: https://www.instagram.com/developer/sandbox/ and https://www.instagram.com/developer/authorization/

This is why I can't access to a lot of public data on Instagram. Occasionally I stepped into the public_content scope, it returns error message like this:
```{"code": 400, "error_type": "OAuthPermissionsException", "error_message": "This request requires scope=public_content, but this access token is not autho
rized with this scope. The user must re-authorize your application with scope=public_content to be granted this permissions."}```

In my project, I asked 5 of my Ins friends as test users and fetch their recent posts by using the endpoint "/users/self/media/recent" in the basic scope. These data is cached in file "cache_contents.json" for graders to use locally.

If the grader needs to test the OAuth2 authorization code ability in "SI507F17_finalproject_oauth.py", I provided a test account that is in my sandbox list for you to use. Before using it, please remove the existing "cache_contents.json"/"creds.json", and rename the "cache_contents_test.json"/"creds_test.json" as the former two files.


# Other Useful Links and References
*Instagram Api: https://www.instagram.com/developer/
*OAuth2 authorization is revised from Anand's facebook_oauth (which is based on Steve Oney's example) in section-week-9
