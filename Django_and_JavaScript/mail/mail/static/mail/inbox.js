document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //send email
  document.querySelector('#compose-form').onsubmit = ()=>{
    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;
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
      if ("message" in result) {  
        console.log('success')
        //if is success send to sent view
        load_mailbox('sent');
      }
      if ("error" in result) {
        console.log('error')
        //if is not success show the error
        document.querySelector('#result').innerHTML = result['error']
      }
      console.log(result);
    })
    .catch(error => {
      console.log(error);
    });
    return false;
  };

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
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
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    //take who send the email
    emails.forEach(element => {
      if (mailbox === "inbox") {
        senders = element.sender;
      }
      else if (mailbox === "archive") {
        senders = element.sender;
      } 
      //then is sent
      else {
        senders = element.recipients;
      }
      if (mailbox === "inbox") {
        if (element.read){
          read = true;
        } 
        else{
          read = false;
        } 
      } else{
        read = false;
      }
      //create the view of mails
      let mail = document.createElement("div");
      mail.className = `card`;
      mail.style.border="solid 1px black"
      mail.style.cursor="pointer"
      mail.style.borderRadius="15px"
      if (read){
        mail.style.backgroundColor="lightgray"
      }
      else{
        mail.style.backgroundColor="white"
      }
      mail.innerHTML = `<div class="card-body" id="item-${element.id}">
        <h5 class="card-title">${element.subject}</h5>
        <h6> send by: ${senders} </h6>
        <br>
        <h6> at: ${element.timestamp} </h6>
        <br>
        ${element.body.slice(0, 100)}
        </div>`;
      document.querySelector("#emails-view").appendChild(mail);
      

      //see an email
      mail.addEventListener("click", () => {
        let id = element.id
        console.log(`you are clicking the email ${id} in ${mailbox} `)
        
        //consult the email        
        fetch(`/emails/${id}`)
        .then((response) => response.json())
        .then((email) => {
          console.log(email);
          //Remove all the mails
          document.querySelector("#emails-view").innerHTML = "";
          let item = document.createElement("div");
          item.className = `card`;
          item.style.backgroundColor="ghostwhite"
          item.style.border="solid 1px dodgerblue"
          item.style.borderRadius="15px"
          item.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">
              <h3> Subject: ${email.subject} </h3>    
              <h5> Send by: ${email.sender} | To: ${email.recipients} </h5>
              <h6> At: ${email.timestamp}</h6>
              <br> ${email.body}
            </div>`;
          //add the email
          document.querySelector("#emails-view").appendChild(item);
          
          if (mailbox == "sent"){
            return;
          }
          let archive = document.createElement("btn");
          archive.className = `btn btn-success`;

          //archive
          archive.addEventListener("click", () => {
            fetch(`/emails/${id}`, {
              method: "PUT",
              body: JSON.stringify({
                archived: !email.archived,
              }),
            });
            if (archive.innerText === "Archive") {
              archive.className = `btn btn-danger`;
              archive.innerText = "Unarchive";
            }
            else {
              archive.innerText = "Archive";
            }
            //if archive, go to mailbox 
            load_mailbox('inbox')
          });
          if (!email.archived){
            archive.textContent = "Archive";
          } 
          else {
            archive.className = `btn btn-danger`;
            archive.textContent = "Unarchive";
          } 

          document.querySelector("#emails-view").appendChild(archive);
          let reply = document.createElement("btn");
          reply.className = `btn btn-warning`;
          reply.textContent = "Reply";
          
          //reply
          reply.addEventListener("click", () => {
            compose_email();
            if ( !(email.subject.startsWith("Re: "))){
              email.subject = `Re: ${email.subject}`;
            } 
            document.querySelector("#compose-recipients").value = email.sender;
            document.querySelector("#compose-subject").value = email.subject;
            pre_fill = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n`;
            document.querySelector("#compose-body").value = pre_fill;          
          });

          //read
          document.querySelector("#emails-view").appendChild(reply);
          fetch(`/emails/${id}`, {
            method: "PUT",
            body: JSON.stringify({
              read: true,
            }),
          });
        
        });
        //end show email
      });
    //end for each
    });
  //end then
  });
}


