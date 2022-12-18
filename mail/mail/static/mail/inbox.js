document.addEventListener('DOMContentLoaded', function () {

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

  // Querry the API for latest emails
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      // Display each email
      emails.forEach(email => {
        console.log(email);
        display_email(email);
      });
    });

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`; 
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

function display_email(email) {

  // Append ul element with bootstraps class
  const ul = document.createElement('ul');
  ul.setAttribute("class", "list-group");
  document.querySelector('#emails-view').append(ul);

  // Append li elements for each email with bootstraps class
  const li = document.createElement('li');

  // Set different css to .read if true/false
  if (email.read) {
    li.setAttribute("class", "list-group-item clickable");
  }
  else {
    li.setAttribute("class", "list-group-item active clickable");
  }

  // Display clickable list of emails
  li.innerHTML = `<b>${email.sender}</b>  ${email.subject}   ${email.timestamp}`;
  li.addEventListener('click', function () {
    view_email(email);
  });
  document.querySelector('.list-group').append(li);
}

function view_email(email) {

  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // GET request of email by id
  fetch(`/emails/${email.id}`)
    .then(response => response.json())
    .then(email => {

      // Display email
      document.querySelector("#email-view").innerHTML = `
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <b>From: </b>${email.sender}<br>
          <b>To: </b>${email.recipients}<br>
          <b>Subject: </b>${email.subject}<br>
          <b>Timestamp: </b>${email.timestamp}<br>
          <p><button class="btn btn-sm btn-outline-primary" id="reply">Reply</button></p>
        </li>
        <li class="list-group-item">
          ${email.body}
        </li>      
      </ul>`
      // Archieve / Unarchieve button
      const btn_archive = document.createElement('button');
      btn_archive.setAttribute("class", "btn btn-sm btn-outline-primary");
      btn_archive.innerHTML = email.archived ? "Unarchive" : "Archive";
      document.querySelector("#email-view").append(btn_archive);
      btn_archive.addEventListener('click', function () {
        archive(email); 
      });
    });
      

  // Change to read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function archive(email) {
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !email.archived
    })
  })
  .then(() => { load_mailbox('inbox')})  
}