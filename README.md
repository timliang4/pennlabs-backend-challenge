# Penn Labs Backend Challenge

## Documentation

Fill out this section as you complete the challenge!

## Installation

1. Click the green "use this template" button to make your own copy of this repository, and clone it. Make sure to create a **private repository**.
2. Change directory into the cloned repository.
3. Install `pipx`
   - `brew install pipx` (macOS)
   - See instructions here https://github.com/pypa/pipx for other operating systems
4. Install `poetry`
   - `pipx install poetry`
5. Install packages using `poetry install`.

## File Structure

- `app.py`: Main file. Has configuration and setup at the top. Add your [URL routes](https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing) to this file!
- `models.py`: Model definitions for SQLAlchemy database models. Check out documentation on [declaring models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) as well as the [SQLAlchemy quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart) for guidance
- `bootstrap.py`: Code for creating and populating your local database. You will be adding code in this file to load the provided `clubs.json` file into a database.

## Developing

0. Determine how to model the data contained within `clubs.json` and then complete `bootstrap.py`
1. Activate the Poetry shell with `poetry shell`.
2. Run `python3 bootstrap.py` to create the database and populate it.
3. Use `flask run` to run the project.
4. Follow the instructions [here](https://www.notion.so/pennlabs/Backend-Challenge-862656cb8b7048db95aaa4e2935b77e5).
5. Document your work in this `README.md` file.

## Submitting

Follow the instructions on the Technical Challenge page for submission.

## Installing Additional Packages

Use any tools you think are relevant to the challenge! To install additional packages
run `poetry add <package_name>` within the directory. Make sure to document your additions.

## Documentation

### Endpoints

Clubs
GET /api/clubs

Retrieves a list of all clubs with their details and favorite counts.
POST /api/clubs

Creates a new club. Requires code, name, description, and tags in the request body.
PATCH /api/clubs

Updates an existing club. Requires code, newCode, newName, newDescription, and newTags in the request body.
GET /api/clubs/search

Searches for clubs by name. Requires name in the request body.
Users
GET /api/user

Retrieves user information. Requires username in the request body.
POST /api/user/favorite

Adds a club to a user's favorites. Requires username and code in the request body.
Tags
GET /api/tags
Lists all tags with the number of associated clubs.
Error Handling
The API returns error messages in JSON format with a descriptive message.
Utility Functions
jsonifyErrorMsg(msg)

Returns a JSON response with an error message.
isListOfStrings(x)

Checks if the input is a list of strings.

## Questions

1. To implement signup, login, and logout features, I’d set up the POST /signup route where users provide their credentials. I’d hash the passwords using bcrypt before storing them in the database to ensure security. For login via POST /login, I'd compare the hashed password with the stored hash and, if valid, issue a session or JWT token for user authentication. The POST /logout route would handle logging out by invalidating the session or token. To protect against security threats, it’s crucial to store passwords securely, use parameterized queries to prevent SQL injection, and apply rate limiting to guard against brute force attacks. Implementing OAuth 2.0 for third-party logins and using JWT for managing sessions can further enhance the system’s robustness.

2. For allowing users to post comments about clubs, I’d design a database schema with three main tables: Users, Clubs, and Comments. The Comments table would track individual comments, including a parent_comment_id to facilitate threaded replies. This setup allows us to link comments to both users and clubs, and support a hierarchical comment structure where users can reply to each other’s comments. By establishing these relationships, we ensure that comments are appropriately associated with their respective users and clubs while supporting comment chains.

3. For routes that receive a lot of traffic, such as GET /clubs and GET /club/<id>, implementing caching can significantly improve performance. I would use Flask-Caching or Django-Redis to cache responses, with Redis as the backend for efficient data retrieval. It’s important to set up cache expiration to avoid serving outdated information, and to manage cache invalidation when data changes, such as when new comments are posted. For in-memory caching, cachetools can be used, and requests-cache is useful for caching external API calls. This approach helps reduce the load on the database and speeds up response times for frequently accessed routes.
