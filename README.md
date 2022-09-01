# django_hillel_blog

I expect a link to the repository and a link to the deployed project (if you made this option)

Tech task:
Blog (again).
Functional:

User can register + login/logout
User can create posts (login required)
The user can publish posts or put them into blanks (the user can publish them later)
The user can modify their posts (login required, filter(owner=...))
Anonymous users can post comments
Comments are moderated before publication (field is_published + admin page)
The administrator receives an email notification about a new post or comment (to the console)
The user is notified of a new comment below the post with a link to the post (console) (start by sending an email when the comment is created)
There is a page with a list of all posts
There is a page with a list of user posts
There is a post page
There is a public profile page
There is a profile in which you can change your data
Pagination of posts and comments
The post has a title, a short description, a picture (optionally a link to an image or a real image file) and a full description
The comment has a username and text (just two text fields)
Fixture loremipsum
Admin panel with functionality
Feedback form with the admin (in the console)
Templates with styling
Different settings for development and production
Database query optimization
caching
Celery
Pythonanywhere or Heroku or DigitalOcean or whatever - deploy in production (without caching and task background) **

items with ** are optional, but desirable - the implementation of seler and caching can be done in a separate branch so that they would not be used when deploying to production
more instructions can be found here - https://djangogirls.org/resources/
keep in mind that on Pythonanywhere (and others) - redis and celery will not work (they need to be configured separately).
