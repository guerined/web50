document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function view_email(email_id) {

  // Show email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#view-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  

  document.querySelector(`#view-view`).innerHTML='';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then( email => {
    
    const archivebtn = document.createElement('button');
    archivebtn.className = "btn btn-sm btn-outline-primary";
    if (email['archived']) {
      archivebtn.innerHTML = `Unarchive`;
      archivebtn.addEventListener('click', function() {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: false
          })
        });
        setTimeout(() => {load_mailbox('inbox')}, 200);
      });
    } else {
      archivebtn.innerHTML = `Archive`;
      archivebtn.addEventListener('click', function() {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: true
          })
        });
        setTimeout(() => {load_mailbox('inbox')}, 200);
      });
    }
    document.querySelector(`#view-view`).append(archivebtn);

    const fromdiv = document.createElement('div');
    fromdiv.innerHTML = `<strong>From:</strong> ${email['sender']}`;
    document.querySelector(`#view-view`).append(fromdiv);

    let i = 0;
    const todiv = document.createElement('div');
    todiv.innerHTML = `<strong>To: </strong>`;
    for (recipient in email['recipients']) {
      todiv.innerHTML = todiv.innerHTML + (email['recipients'][recipient]);
      i++;
      if (i<email['recipients'].length ) {
        todiv.innerHTML = todiv.innerHTML + ", ";
      }
    }
    document.querySelector(`#view-view`).append(todiv);

    const subjectdiv = document.createElement('div');
    subjectdiv.innerHTML = `<strong>Subject:</strong> ${email['subject']}`;
    document.querySelector(`#view-view`).append(subjectdiv);

    const datediv = document.createElement('div');
    datediv.innerHTML = `<strong>TimeStamp:</strong> ${email['timestamp']}`;
    document.querySelector(`#view-view`).append(datediv);

    const bodydiv = document.createElement('div');
    bodydiv.innerHTML = `<br> ${email['body']}`;
    document.querySelector(`#view-view`).append(bodydiv);

    const replybtn = document.createElement('button');
    replybtn.innerHTML = `Reply`;
    replybtn.className = "btn btn-sm btn-outline-primary";
    replybtn.addEventListener('click', ()=> reply_email(email['sender'], email['subject'], email['body'], email['timestamp']));
    document.querySelector(`#view-view`).append(replybtn);
  });

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

}

function reply_email(recipient, subject, body, timestamp) {

  compose_email();

  document.querySelector('#compose-recipients').value = recipient;
  document.querySelector('#compose-subject').value = `Re: ${subject}`;
  document.querySelector('#compose-body').value = `
  
On ${timestamp}, ${recipient} wrote: 
${body}`;

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#view-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

//Define what will happen when I submit the form

  document.querySelector('#compose-form').onsubmit = function() {
    
    //post email to API
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      //Print Result
      console.log(result);
      if (result['error'] == 'At least one recipient required.') {
        alert(result['error']);
      }
      if (result['message'] == 'Email sent successfully.') {
        load_mailbox('sent');
      }
    });
    //stop form from submitting
    return false;
  };

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#view-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the email using API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach( email => {
      let rowdiv = document.createElement('div');
      rowdiv.id = "email" + email["id"];
      if (email["read"]) {
        rowdiv.className = 'row email_list read';
      }
      else {
        rowdiv.className = 'row email_list';
      }
      if (mailbox == 'sent') {
        rowdiv.className = 'row email_list read';
      }
      rowdiv.style.cursor = "pointer";
      
      
      
      let emailsender = document.createElement('div');
      emailsender.className = 'col-2 sender';
      if (mailbox == 'inbox') {
        emailsender.innerHTML = email["sender"];
      }
      else if (mailbox == 'sent') {
        emailsender.innerHTML = email["recipients"]["0"];
      }
      rowdiv.append(emailsender);

      const emailtopic = document.createElement('div');
      emailtopic.className = 'col-8 topic';
      emailtopic.innerHTML = email["subject"];
      rowdiv.append(emailtopic);

      const emaildate = document.createElement('div');
      emaildate.className = 'col-2 date';
      emaildate.innerHTML = email["timestamp"];
      rowdiv.append(emaildate);

      rowdiv.addEventListener('click', ()=> view_email(email["id"]));

      document.querySelector(`#emails-view`).append(rowdiv);

    })
  })
}