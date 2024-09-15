# Penn Labs Backend Challenge

## Documentation

### Design Choices

I created models for Clubs, Users, and Tags, with a table for users "favoriting" clubs to and a table for clubs "using" tags. This way, I could represent the many-to-many relationships.

For the relationship between clubs and tags, I chose to joined load the tags whenever querying for clubs because each club only has a few tags, so loading them in with their clubs using a joined load wouldn't be too data-intensive. Additionally, I needed the name of each tag of a club, and a joined load would allow me to immediately access the name of each tag via a Python list.

On the other hand, I chose to lazy load the users who favorited a club because I didn't need a python list of Uuers who favorited the club with a bunch of information I didn't need like username. I just needed the count of users who favorited the club. So, I designed my own query that did the joining and counting within a SQL statement, which would be a lot more time and efficient.

Next, I also lazy loaded the clubs whenever querying for tags because I didn't need a python list of clubs who used a certain tag with a bunch of information I didn't need. I just needed the count of clubs with a tag. So, like before, I designed my own query that did the joining and counting within a SQL statement.

Finally, I lazy loaded the clubs whenever querying for users because I decided that the clubs a user favorited was private information, so I wouldn't be accessing that information if queried for a user.

For efficient searching, I made the name attribute in the clubs model an index. So, when the clubs are queries based on their name, SQL is a lot faster.

For querying for users, I decided that the clubs a user liked was private information because that information could potentially be used to track down the user. So, I only provided the username when querying for users.

### Endpoints

Clubs
`GET /api/clubs`
Retrieves a list of all clubs with their details and favorite counts.

`POST /api/clubs`
Creates a new club. Requires code, name, description, and tags in the request body.

`PATCH /api/clubs`
Updates an existing club. Requires code, newCode, newName, newDescription, and newTags in the request body.

`GET /api/clubs/search`
Searches for clubs by name. Requires name in the request body.

`GET /api/user`
Retrieves user information. Requires username in the request body.

`POST /api/user/favorite`
Adds a club to a user's favorites. Requires username and code in the request body.

`GET /api/tags`
Lists all tags with the number of associated clubs.


## Questions

1. To implement signup, login, and logout features, I’d set up the POST /signup route where users provide their credentials. I’d hash the passwords using bcrypt before storing them in the database to ensure security. For login via POST /login, I'd compare the hashed password with the stored hash and, if valid, issue a session or JWT token for user authentication. The POST /logout route would handle logging out by invalidating the session or token. To protect against security threats, it’s crucial to store passwords securely, use parameterized queries to prevent SQL injection, and apply rate limiting to guard against brute force attacks. Implementing OAuth 2.0 for third-party logins and using JWT for managing sessions can further enhance the system’s robustness.

2. For allowing users to post comments about clubs, I’d design a database schema with three main tables: Users, Clubs, and Comments. The Comments table would track individual comments, including a parent_comment_id to facilitate threaded replies. This setup allows us to link comments to both users and clubs, and support a hierarchical comment structure where users can reply to each other’s comments. By establishing these relationships, we ensure that comments are appropriately associated with their respective users and clubs while supporting comment chains.

3. For routes that receive a lot of traffic, such as GET /clubs and GET /club/<id>, implementing caching can significantly improve performance. I would use Flask-Caching or Django-Redis to cache responses, with Redis as the backend for efficient data retrieval. It’s important to set up cache expiration to avoid serving outdated information, and to manage cache invalidation when data changes, such as when new comments are posted. For in-memory caching, cachetools can be used, and requests-cache is useful for caching external API calls. This approach helps reduce the load on the database and speeds up response times for frequently accessed routes.
