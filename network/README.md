# Social Network
This is a social network web application built with Django, Python, HTML, CSS, and JavaScript. The application allows users to create posts, follow other users, and like posts.
## Features
### Authentication
- Users can register and login to the application.
- Users can reset their password if they forget it.
### Posts
- Users can create a new post by filling in a text area and submitting it.
- Users can edit their own posts by clicking an "Edit" button or link.
- Users can see all posts from all users on the "All Posts" page.
- Users can see posts from users they follow on the "Following" page.
- Posts are displayed with the username of the poster, the post content, the date and time of the post, and the number of likes.
### Likes
- Users can like and unlike posts by clicking a button or link.
- The number of likes on a post is updated asynchronously with JavaScript without requiring a reload of the entire page.
### Follows
- Users can follow and unfollow other users by clicking a button or link.
- The number of followers and following for a user is displayed on their profile page.
### Pagination
- Posts are displayed 10 per page.
- Users can navigate between pages using the "Previous" and "Next" buttons.
### Security
- Users can only edit their own posts, and not those of other users.
- Users cannot follow themselves.
## Credits
This application was created by me. It is based on the CS50W Project 4 specification.
