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

    // Display each email
    emails.forEach(email => {
      console.log(email);
      display_email(email);
    });
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
  //li.setAttribute("style", "cursor: auto"); ???
  li.addEventListener('click', function() {
    
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
    // Print email
    console.log(email);

    // ... do something else with email ...
    // Append ul element with bootstraps class
    const ul = document.createElement('ul');
    ul.setAttribute("class", "list-group list-group-flush");
    ul.setAttribute("id", "head");
    document.querySelector('#email-view').append(ul);

    // Display head of an email
    const head = document.createElement('li');
    head.setAttribute("class", "list-group-item");
    head.innerHTML = `<b>From: </b>${email.sender}<br>
    <b>To: </b>${email.recipients}<br>
    <b>Subject: </b>${email.subject}<br>
    <b>Timestamp: </b>${email.timestamp}<br>
    <p><button class="btn btn-sm btn-outline-primary" id="reply">Reply</button></p>`
    document.querySelector('#head').append(head);

    // Display body of an email
    const body = document.createElement('li');
    body.setAttribute("class", "list-group-item");
    body.innerHTML = `${email.body}`;
    document.querySelector('#head').append(body);
  });
    
    // Change to read
    fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

    // Archieve / Remove from the Archieve button
    const p = document.createElement('button');
    p.setAttribute("class", "btn btn-sm btn-outline-primary")
    p.innerHTML = email.archived ? "Unarchive" : "Archive"
    p.addEventListener('click', function() {
      console.log('clicked!');
    })
    document.querySelector('#head').append(p);

    //Clear previous emails from innerHTML
    document.querySelector('#head').innerHTML = '';
    
}

function archive(email) {
  email = email
  if (email.archive) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archive: false
      })
    })
  }
  else {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archive: true
      })
    })
  }
  view_email(email);
}