
      function toggleMessenger() {
          const modal = document.getElementById('messenger-modal');
          if (modal.style.display === 'none' || modal.style.display === '') {
              modal.style.display = 'block';
          } else {
              modal.style.display = 'none';
          }
      }
  
      function openChat(contactId) {
          document.getElementById('contact-list').style.display = 'none';
          document.getElementById('chat-box').style.display = 'block';
          loadMessages(contactId);
      }
  
      function loadMessages(contactId) {
          const messagesDiv = document.getElementById('messages');
          messagesDiv.innerHTML = '<p>Loading messages...</p>';
  
          setTimeout(() => {
              messagesDiv.innerHTML = `<p>Chat ${contactId}</p>`;
              messagesDiv.innerHTML += '<p>Message 1</p><p>Message 2</p>';
          }, 500);
      }
  
      function sendMessage(event) {
          if (event.key === 'Enter') {
              const messageInput = document.getElementById('message-input');
              const message = messageInput.value;
              messageInput.value = '';
  
              const messagesDiv = document.getElementById('messages');
              messagesDiv.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
          }
      }
