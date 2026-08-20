const form = document.querySelector('#email-form');
const submitButton = document.querySelector('#submit-button');
const formError = document.querySelector('#form-error');
const bodyInput = document.querySelector('#body');
const results = document.querySelector('#results');
const reply = document.querySelector('#reply');

document.querySelector('#body').addEventListener('input', (event) => {
  document.querySelector('#char-count').textContent = `${event.target.value.length.toLocaleString()} / 10,000`;
});

function validate() {
  const values = Object.fromEntries(new FormData(form));
  const errors = {};
  if (!values.from.trim()) errors.from = 'Email address is required.';
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.from) || values.from.length > 254) errors.from = 'Enter a valid email address ( 최대 254 characters).'.replace(' 최대', 'Maximum');
  if (!values.subject.trim()) errors.subject = 'Subject is required.';
  else if (values.subject.length > 200) errors.subject = 'Subject must be 200 characters or fewer.';
  if (!values.body.trim()) errors.body = 'Email body is required.';
  else if (values.body.trim().length < 10) errors.body = 'Email body must be at least 10 characters.';
  else if (values.body.length > 10000) errors.body = 'Email body must be 10,000 characters or fewer.';
  document.querySelectorAll('.field-error').forEach((el) => { el.textContent = errors[el.dataset.errorFor] || ''; });
  return Object.keys(errors).length === 0;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault(); formError.textContent = '';
  if (!validate()) return;
  submitButton.disabled = true; submitButton.innerHTML = 'Generating response...'; results.hidden = true;
  try {
    const payload = Object.fromEntries(new FormData(form));
    const response = await fetch('/process-email', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok || !data.success) throw new Error(data.error || 'Request failed');
    document.querySelector('#summary').textContent = data.summary;
    reply.textContent = data.reply;
    results.hidden = false;
    results.scrollIntoView({behavior: 'smooth', block: 'start'});
  } catch { formError.textContent = "We couldn't generate a response right now. Please try again."; }
  finally { submitButton.disabled = false; submitButton.innerHTML = 'Generate response <span>→</span>'; }
});

document.querySelector('#copy-button').addEventListener('click', async () => {
  await navigator.clipboard.writeText(reply.textContent);
  const status = document.querySelector('#copy-status'); status.textContent = 'Reply copied!';
  setTimeout(() => { status.textContent = ''; }, 2500);
});
