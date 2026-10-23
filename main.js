// Footer year
document.getElementById('year').textContent = new Date().getFullYear();

// If the PyScript order menu hasn't started in time, show a fallback message.
setTimeout(function () {
  if (document.body.dataset.ready) return;
  var note = document.getElementById('order-fallback');
  if (location.protocol === 'file:') {
    note.textContent = 'The order menu needs the site to run from a web server, not a double-clicked file (see README.txt). You can also message us to order.';
  }
  note.hidden = false;
  document.getElementById('place').textContent = 'Order menu unavailable';
}, location.protocol === 'file:' ? 3000 : 20000);
