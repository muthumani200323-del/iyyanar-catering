/* Sri Iyyanar Catering Service - page behaviour (plain JavaScript, no libraries) */
(function () {
  'use strict';

  var DEFAULT_NUM = '917395830160';

  function $(id) { return document.getElementById(id); }
  function all(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }
  function chosen(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : DEFAULT_NUM;
  }

  /* Build the WhatsApp and SMS links for a message */
  function links(waEl, smsEl, msg, num) {
    var enc = encodeURIComponent(msg);
    waEl.href = 'https://wa.me/' + num + '?text=' + enc;
    if (smsEl) smsEl.href = 'sms:+' + num + '?&body=' + enc;
  }

  function copyText(text, noteEl, okText, failText) {
    function fallback() { noteEl.textContent = failText; }
    try { navigator.clipboard.writeText(text).then(function () { noteEl.textContent = okText; }, fallback); }
    catch (e) { fallback(); }
  }

  /* ---------- About pop-up ---------- */
  var about = $('about-pop');
  if (about && $('about-link')) {
    $('about-link').addEventListener('click', function (e) {
      e.preventDefault();
      about.hidden = !about.hidden;
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') about.hidden = true; });
    document.addEventListener('click', function (e) {
      if (!about.hidden && !about.contains(e.target) && e.target !== $('about-link')) about.hidden = true;
    });
  }

  /* ---------- Copy a phone number ---------- */
  all('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var num = btn.getAttribute('data-copy');
      var note = $('copynote');
      copyText(num, note, num + ' copied', 'Could not copy automatically. Select the number and copy it.');
    });
  });

  /* ---------- Function chips (tap one, or type your own) ---------- */
  var chips = $('fn-chips');
  var fnInput = $('b-event');
  if (chips && fnInput) {
    var mark = function () {
      var v = fnInput.value.trim();
      all('.fn-chip').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-v') === v); });
    };
    chips.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.fn-chip') : null;
      if (!b) return;
      fnInput.value = b.getAttribute('data-v');
      mark();
    });
    fnInput.addEventListener('input', mark);
  }

  /* ---------- Booking form ---------- */
  var bookForm = $('bookform');
  if (bookForm) {
    var dateEl = $('b-date');
    var today = new Date();
    dateEl.min = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
    var bookMsg = '';

    bookForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = $('b-name').value.trim();
      var phone = $('b-phone').value.replace(/\D/g, '');
      var date = dateEl.value;
      var guests = $('b-guests').value;
      var err = $('b-err');
      if (!name) { err.textContent = 'Enter your name.'; $('b-name').focus(); return; }
      if (phone.length < 10) { err.textContent = 'Enter a 10 digit mobile number so we can call you back.'; $('b-phone').focus(); return; }
      if (!date) { err.textContent = 'Choose the function date.'; dateEl.focus(); return; }
      if (!guests || Number(guests) < 1) { err.textContent = 'Enter the number of guests.'; $('b-guests').focus(); return; }
      err.textContent = '';

      var food = document.querySelector('input[name="food"]:checked').value;
      var deliv = document.querySelector('input[name="deliv"]:checked').value;
      var fn = fnInput.value.trim() || 'Not mentioned';
      var venue = $('b-venue').value.trim();
      var notes = $('b-notes').value.trim();

      var lines = [
        'Booking request - Sri Iyyanar Catering Service',
        'Name: ' + name,
        'Mobile: ' + phone,
        'Function: ' + fn,
        'Date: ' + date,
        'Guests: ' + guests,
        'Food: ' + food,
        'Door delivery: ' + deliv
      ];
      if (venue) lines.push('Venue / address: ' + venue);
      if (notes) lines.push('Notes: ' + notes);
      bookMsg = lines.join('\n');

      $('b-msg').textContent = bookMsg;
      links($('b-wa'), $('b-sms'), bookMsg, chosen('sendto'));
      var box = $('b-ready');
      box.hidden = false;
      box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

      // Save the booking in the database too (runs in the background; the buttons work even if it fails).
      try {
        fetch(bookForm.getAttribute('data-url'), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': bookForm.querySelector('input[name="csrfmiddlewaretoken"]').value
          },
          credentials: 'same-origin',
          body: JSON.stringify({
            name: name, phone: phone, function: fn, date: date, guests: Number(guests),
            food: food, delivery: deliv, venue: venue, notes: notes, send_to: chosen('sendto')
          })
        });
      } catch (x) { /* ignore */ }
    });

    $('b-copy').addEventListener('click', function () {
      copyText(bookMsg, $('b-note'),
        'Message copied. Paste it in WhatsApp or SMS to ' + chosen('sendto').slice(2) + '.',
        'Could not copy automatically. Select the message above and copy it.');
    });
    all('input[name="sendto"]').forEach(function (r) {
      r.addEventListener('change', function () { if (bookMsg) links($('b-wa'), $('b-sms'), bookMsg, chosen('sendto')); });
    });
  }

  /* ---------- Review form: star picker ---------- */
  var starBox = $('r-stars');
  var revForm = $('revform');
  if (starBox && revForm) {
    var rating = 0;
    var starBtns = [];
    for (var i = 1; i <= 5; i++) {
      (function (n) {
        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = '★';
        b.setAttribute('role', 'radio');
        b.setAttribute('aria-checked', 'false');
        b.setAttribute('aria-label', n + ' out of 5');
        b.addEventListener('click', function () {
          rating = n;
          $('r-rating').value = n;
          starBtns.forEach(function (s, idx) {
            s.classList.toggle('on', idx < n);
            s.setAttribute('aria-checked', String(idx + 1 === n));
          });
        });
        starBox.appendChild(b);
        starBtns.push(b);
      })(i);
    }
    revForm.addEventListener('submit', function (e) {
      var err = $('r-err');
      if (!rating) { e.preventDefault(); err.textContent = 'Choose a star rating.'; starBtns[0].focus(); return; }
      if (!$('r-text').value.trim()) { e.preventDefault(); err.textContent = 'Write a few words about your experience.'; $('r-text').focus(); return; }
      err.textContent = '';
    });
  }

  /* ---------- Admin tools (only present when an admin is logged in) ---------- */
  var galOpen = $('gal-open'), galForm = $('gal-form');
  if (galOpen && galForm) {
    galOpen.addEventListener('click', function () { galForm.hidden = !galForm.hidden; });
    $('g-cancel').addEventListener('click', function () { galForm.hidden = true; });
  }
  all('form[data-confirm]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      if (!window.confirm(f.getAttribute('data-confirm'))) e.preventDefault();
    });
  });
})();
