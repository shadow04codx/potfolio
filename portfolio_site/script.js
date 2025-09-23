
// Basic form handling for demo (no backend)
document.addEventListener('DOMContentLoaded', function(){
  const form = document.getElementById('contactForm');
  const status = document.getElementById('formStatus');
  form.addEventListener('submit', function(e){
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    if(!name || !email || !message){ status.textContent = 'Please fill all fields.'; return; }
    status.textContent = 'Thanks! This is a demo contact form — configure a backend to receive messages.';
    form.reset();
    setTimeout(()=> status.textContent = '', 5000);
  })
});
