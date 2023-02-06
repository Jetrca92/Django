# Email Client

As a part of **CS50W** program, I had to build a front-end for an email client that makes API calls to send and receive emails. 
This is a single-page-app email client implemented using Django, JavaScript, HTML, and CSS. The application is contained in the file inbox.js.

## Features
### Send Mail
- When a user submits the email composition form, an email is sent to the recipient.
- A POST request is made to /emails passing in values for recipients, subject, and body.
- After the email is sent, the user's sent mailbox is loaded.
### Mailbox
- When a user visits their Inbox, Sent mailbox, or Archive, the appropriate mailbox is loaded.
- A GET request is made to /emails/<mailbox> to request the emails for a particular mailbox.
- The name of the mailbox is displayed at the top of the page.
- Each email is rendered in a box with the sender, subject, and timestamp displayed.
- If the email is unread, it appears with a white background, if read, with a gray background.
### View Email
- When a user clicks on an email, the content of that email is displayed.
- A GET request is made to /emails/<email_id> to request the email.
- The sender, recipients, subject, timestamp, and body of the email are displayed.
- The email is marked as read by sending a PUT request to /emails/<email_id>.
### Archive and Unarchive
- Allow users to archive and unarchive received emails.
- Inbox emails can be archived, Archive emails can be unarchived.
- Emails are archived or unarchived by sending a PUT request to /emails/<email_id>.
- After an email is archived or unarchived, the user's inbox is loaded.
### Reply
- Allow users to reply to an email.
- A "Reply" button is displayed when viewing an email.
- When the "Reply" button is clicked, the user is taken to the email composition form.
- The recipient field is pre-filled with the sender of the original email.
- The subject line is pre-filled with "Re: [original subject]" and the body of the email is pre-filled with a line indicating the original text of the email.
