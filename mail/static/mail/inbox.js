document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-submit').addEventListener('click', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#open-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#open-email-view').style.display = 'none';

  document.querySelector('#open-email-view').innerHTML = '';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  let background = 'white'

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      if (email.read == true) {
        background = 'gainsboro'
      }
      else {
        background = 'white'
      }
      const listed_email = document.createElement('div');
      listed_email.setAttribute('style', `border: grey 1px solid; padding: 5px; background:${background}; width:100%; border-radius: 6px`);
      listed_email.className = 'listed_email';
      // listed_email.innerHTML =  
      if (mailbox == 'sent') {
        listed_email.innerHTML = 
        `<table>
          <tr>
            <td style='font-size:medium; font-weight:bold; width: 25%'>${email.recipients}</td>
            <td style='font-size:small; width:65%'>${email.subject}</td>
            <td style='font-size:small; width: 15%'>${email.timestamp}</td>
          </tr>  
        </table>`;
      }
      else {
        listed_email.innerHTML = 
        `<table>
          <tr>
            <td style='font-size:medium; font-weight:bold; width: 25%'>${email.sender}</td>
            <td style='font-size:small; width:65%'>${email.subject}</td>
            <td style='font-size:small; width: 15%'>${email.timestamp}</td>
          </tr>  
        </table>`;
      }
      listed_email.addEventListener('click', () => open_email(email.id, mailbox));
      document.querySelector('#emails-view').append(listed_email);
    })
    console.log(emails)
  })
}

function send_mail(event) {
  event.preventDefault()

  compose_form = document.querySelector('form');
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  console.log(recipients)
    
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  });
}  

function open_email(email_id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#open-email-view').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    let archive = 'Archive';
    if (email.archived == true) {
      archive = 'Unarchive';
    }
    let email_html = document.createElement('div');
    email_html.setAttribute('style', 'border: grey');
    email_html.className = 'email';
    if (mailbox === 'sent'){
      email_html.innerHTML = 
        `<h3>${email.subject}</h3>
        <h5 style='font-weight:bold'>${email.sender}</h5>
        <p style='font-size:small'>sent to: ${email.recipients} on ${email.timestamp}</p> 
        <p id='sent-email-body' style='margin-top: 20px'>${email.body}</p>`;
    }
    else {
      email_html.innerHTML = 
        `<h3>${email.subject}</h3>
        <h5 style='font-weight:bold'>${email.sender}</h5>
        <p style='font-size:small'>sent to: ${email.recipients} on ${email.timestamp}</p> 
        <button id=reply-btn>Reply</button>
        <button id=archive-btn>${archive}</button>
        <p id='email-body'>${email.body}</p>`;

    }
     
    document.querySelector('#open-email-view').append(email_html);
    if (mailbox != 'sent') {
      document.querySelector('#archive-btn').addEventListener('click', () => Archive(email_id, email.archived));
      document.querySelector('#reply-btn').addEventListener('click', () => Reply(email));   
    }
  });
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

}

function Reply(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#open-email-view').style.display = 'none';

  // fill in proper values
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  document.querySelector('#compose-subject').value = `Re:${email.subject}`;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
}

function Archive(email_id, archived) {
  let archive = true;

  if (archived == true){
    archive = false;
  }

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archive
    })
  });
  
  console.log('successfully archived or unarchived')
  setTimeout(() => {load_mailbox('inbox');}, 100);
}