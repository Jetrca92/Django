document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submit handler
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    event.preventDefault(); // prevent load

    // and then do your stuff
    send_email();
    load_mailbox('sent');
    return false;

  });

  // Go to email-view when click on email
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Querry the API for latest emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails)

    // ... do something else with emails ...
    emails.forEach(display_email);
    });
  }


function send_email() {
  
  // Save data from form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send mail via POST
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });   
}

function display_email(emails) {
  
  // Append ul element with bootstraps class
  const ul = document.createElement('ul');
  ul.setAttribute("class", "list-group");
  document.querySelector('#emails-view').append(ul);

  // Append li elements for each email with bootstraps class
  const li = document.createElement('li');

  // Set different css to .read if true/false
  if (emails.read) {
    li.setAttribute("class", "list-group-item");
  }
  else {
    li.setAttribute("class", "list-group-item active");
  }  
  li.innerHTML = `<b>${emails.sender}</b>  ${emails.subject}   ${emails.timestamp}`;
  li.setAttribute("style", "cursor: pointer")
  li.addEventListener('click', function() {
    console.log('This element has been clicked!');
    view_email(emails);
  });
  document.querySelector('.list-group').append(li);
}

function view_email(emails) {

  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  //Append ul element with bootstraps class
  const ul = document.createElement('ul');
  ul.setAttribute("class", "list-group list-group-flush");
  ul.setAttribute("id", "head");
  document.querySelector('#email-view').append(ul);

  const head = document.createElement('li');
  head.setAttribute("class", "list-group-item");
  head.innerHTML = `<b>From: </b>${emails.sender}<br>
  <b>To: </b>${emails.recipients}<br>
  <b>Subject: </b>${emails.subject}<br>
  <b>Timestamp: </b>${emails.timestamp}<br>
  <p><button class="btn btn-sm btn-outline-primary" id="reply">Reply</button></p>`
  document.querySelector('#head').append(head);



}