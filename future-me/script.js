/* ============================================================
   Future Me — script.js
   Vanilla JS: storage, rendering, countdowns, theme, quotes
============================================================ */

const STORAGE_KEY = 'futureMe.messages';
const THEME_KEY = 'futureMe.theme';

const QUOTES = [
  { text: 'The best time to plant a tree was 20 years ago. The second best time is now.', author: 'Chinese Proverb' },
  { text: 'Your future is created by what you do today, not tomorrow.', author: 'Robert Kiyosaki' },
  { text: 'The future belongs to those who believe in the beauty of their dreams.', author: 'Eleanor Roosevelt' },
  { text: 'Yesterday is history, tomorrow is a mystery, today is a gift.', author: 'Anonymous' },
  { text: 'Time you enjoy wasting is not wasted time.', author: 'Marthe Troly-Curtin' },
  { text: 'The secret of getting ahead is getting started.', author: 'Mark Twain' },
  { text: "Believe you can and you're halfway there.", author: 'Theodore Roosevelt' },
  { text: 'What lies behind us and what lies before us are tiny matters compared to what lies within us.', author: 'Ralph Waldo Emerson' },
  { text: 'Every moment is a fresh beginning.', author: 'T.S. Eliot' },
  { text: 'Small steps every day lead to big changes over time.', author: 'Anonymous' },
  { text: 'Be patient with yourself. Growth takes time.', author: 'Anonymous' },
  { text: 'The future depends on what you do today.', author: 'Mahatma Gandhi' },
  { text: 'Dream big. Start small. Act now.', author: 'Robin Sharma' },
  { text: 'You are never too old to set another goal or to dream a new dream.', author: 'C.S. Lewis' },
  { text: 'Write it on your heart that every day is the best day in the year.', author: 'Ralph Waldo Emerson' },
];

const PARTICLE_COLORS = ['#6c5ce7', '#fd79a8', '#00b894', '#fdcb6e', '#74b9ff', '#a29bfe'];

/* ----------------------------
   DOM references
---------------------------- */
const themeToggle = document.getElementById('themeToggle');
const quoteText = document.getElementById('quoteText');
const quoteAuthor = document.getElementById('quoteAuthor');
const newQuoteBtn = document.getElementById('newQuoteBtn');
const capsuleForm = document.getElementById('capsuleForm');
const nameInput = document.getElementById('nameInput');
const messageInput = document.getElementById('messageInput');
const dateInput = document.getElementById('dateInput');
const messagesContainer = document.getElementById('messagesContainer');
const emptyState = document.getElementById('emptyState');
const totalCount = document.getElementById('totalCount');
const lockedCount = document.getElementById('lockedCount');
const unlockedCount = document.getElementById('unlockedCount');
const toast = document.getElementById('toast');

/* ----------------------------
   State
---------------------------- */
let messages = loadMessages();
let quoteRotationTimer = null;
let toastTimer = null;

/* ============================================================
   Storage helpers
============================================================ */
function loadMessages() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (err) {
    console.error('Could not read saved capsules:', err);
    return [];
  }
}

function saveMessages() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
}

/* ============================================================
   Theme
============================================================ */
function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem(THEME_KEY, next);
}

/* ============================================================
   Quotes
============================================================ */
function showQuote(animate) {
  const quote = QUOTES[Math.floor(Math.random() * QUOTES.length)];

  if (!animate) {
    quoteText.textContent = `"${quote.text}"`;
    quoteAuthor.textContent = `— ${quote.author}`;
    return;
  }

  quoteText.classList.add('fade');
  quoteAuthor.classList.add('fade');

  setTimeout(() => {
    quoteText.textContent = `"${quote.text}"`;
    quoteAuthor.textContent = `— ${quote.author}`;
    quoteText.classList.remove('fade');
    quoteAuthor.classList.remove('fade');
  }, 250);
}

function startQuoteRotation() {
  clearInterval(quoteRotationTimer);
  quoteRotationTimer = setInterval(() => showQuote(true), 12000);
}

/* ============================================================
   Utilities
============================================================ */
function generateId() {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`;
}

function pad(num) {
  return String(num).padStart(2, '0');
}

function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function formatDate(dateLike) {
  return new Date(dateLike).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function getTimeParts(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  return {
    days: Math.floor(totalSeconds / 86400),
    hours: Math.floor((totalSeconds % 86400) / 3600),
    minutes: Math.floor((totalSeconds % 3600) / 60),
    seconds: totalSeconds % 60,
  };
}

function getProgress(createdAt, unlockAt) {
  const created = new Date(createdAt).getTime();
  const unlock = new Date(unlockAt).getTime();
  if (unlock <= created) return 100;
  const pct = ((Date.now() - created) / (unlock - created)) * 100;
  return Math.min(100, Math.max(0, pct));
}

function setMinDate() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const yyyy = tomorrow.getFullYear();
  const mm = pad(tomorrow.getMonth() + 1);
  const dd = pad(tomorrow.getDate());
  dateInput.min = `${yyyy}-${mm}-${dd}`;
}

/* ============================================================
   Toast notifications
============================================================ */
function showToast(text, type = 'success') {
  toast.textContent = text;
  toast.className = `toast show ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3500);
}

/* ============================================================
   Form validation & submission
============================================================ */
function clearFieldErrors() {
  capsuleForm.querySelectorAll('.field-error').forEach((el) => el.remove());
  capsuleForm.querySelectorAll('.error').forEach((el) => el.classList.remove('error'));
}

function showFieldError(field, text) {
  field.classList.add('error');
  const span = document.createElement('span');
  span.className = 'field-error';
  span.textContent = text;
  field.insertAdjacentElement('afterend', span);
}

function handleFormSubmit(event) {
  event.preventDefault();
  clearFieldErrors();

  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  const dateValue = dateInput.value;
  let valid = true;

  if (!name) {
    showFieldError(nameInput, 'Please enter your name.');
    valid = false;
  }

  if (!message) {
    showFieldError(messageInput, 'Please write a message to your future self.');
    valid = false;
  }

  if (!dateValue) {
    showFieldError(dateInput, 'Please choose an unlock date.');
    valid = false;
  } else {
    const unlockDate = new Date(`${dateValue}T00:00:00`);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (unlockDate <= today) {
      showFieldError(dateInput, 'Please choose a date in the future.');
      valid = false;
    }
  }

  if (!valid) return;

  const newCapsule = {
    id: generateId(),
    name,
    message,
    createdAt: new Date().toISOString(),
    unlockAt: new Date(`${dateValue}T00:00:00`).toISOString(),
    revealed: false,
  };

  messages.push(newCapsule);
  saveMessages();
  renderAll();
  capsuleForm.reset();
  showToast('Your message has been sealed for the future! 🔒', 'success');
}

/* ============================================================
   Rendering
============================================================ */
function getSortedMessages() {
  const locked = messages
    .filter((m) => !m.revealed)
    .sort((a, b) => new Date(a.unlockAt) - new Date(b.unlockAt));

  const unlocked = messages
    .filter((m) => m.revealed)
    .sort((a, b) => new Date(b.unlockAt) - new Date(a.unlockAt));

  return [...locked, ...unlocked];
}

function lockedCardTemplate(msg) {
  const remaining = Math.max(0, new Date(msg.unlockAt).getTime() - Date.now());
  const { days, hours, minutes, seconds } = getTimeParts(remaining);
  const progress = getProgress(msg.createdAt, msg.unlockAt);

  return `
    <div class="capsule-card is-locked" data-id="${msg.id}">
      <div class="capsule-header">
        <div class="capsule-name">🔒 ${escapeHTML(msg.name)}</div>
        <span class="capsule-badge locked">Locked</span>
      </div>
      <div class="capsule-date">Unlocks on ${formatDate(msg.unlockAt)}</div>
      <div class="capsule-locked-body">
        <div class="capsule-lock-icon">🔒</div>
        <div class="capsule-countdown">
          <div class="countdown-unit">
            <span class="countdown-value" data-unit="days">${pad(days)}</span>
            <span class="countdown-label">Days</span>
          </div>
          <div class="countdown-unit">
            <span class="countdown-value" data-unit="hours">${pad(hours)}</span>
            <span class="countdown-label">Hrs</span>
          </div>
          <div class="countdown-unit">
            <span class="countdown-value" data-unit="minutes">${pad(minutes)}</span>
            <span class="countdown-label">Min</span>
          </div>
          <div class="countdown-unit">
            <span class="countdown-value" data-unit="seconds">${pad(seconds)}</span>
            <span class="countdown-label">Sec</span>
          </div>
        </div>
        <div class="progress-bar-track">
          <div class="progress-bar-fill" style="width:${progress}%"></div>
        </div>
        <div class="progress-label">
          <span class="progress-percent">${Math.round(progress)}% there</span>
          <span>Sealed ${formatDate(msg.createdAt)}</span>
        </div>
        <p class="capsule-hint">This capsule stays sealed until the big day arrives.</p>
      </div>
      <div class="capsule-actions">
        <button class="btn-delete" data-action="delete" type="button">Delete</button>
      </div>
    </div>
  `;
}

function unlockedCardTemplate(msg) {
  return `
    <div class="capsule-card is-unlocked" data-id="${msg.id}">
      <div class="capsule-header">
        <div class="capsule-name">💌 ${escapeHTML(msg.name)}</div>
        <span class="capsule-badge unlocked">Unlocked</span>
      </div>
      <div class="capsule-date">Unlocked on ${formatDate(msg.unlockAt)}</div>
      <div class="capsule-unlocked-body">
        <div class="capsule-unlocked-tag">🎉 This message is now open!</div>
        <div class="capsule-message">${escapeHTML(msg.message)}</div>
      </div>
      <div class="capsule-actions">
        <button class="btn-delete" data-action="delete" type="button">Delete</button>
      </div>
    </div>
  `;
}

function cardTemplate(msg) {
  return msg.revealed ? unlockedCardTemplate(msg) : lockedCardTemplate(msg);
}

function updateStats() {
  const total = messages.length;
  const unlocked = messages.filter((m) => m.revealed).length;
  totalCount.textContent = total;
  unlockedCount.textContent = unlocked;
  lockedCount.textContent = total - unlocked;
}

function renderAll() {
  const sorted = getSortedMessages();

  if (sorted.length === 0) {
    messagesContainer.innerHTML = '';
    emptyState.classList.add('visible');
  } else {
    emptyState.classList.remove('visible');
    messagesContainer.innerHTML = sorted.map(cardTemplate).join('');
  }

  updateStats();
}

/* ============================================================
   Reveal animation & particles
============================================================ */
function createParticles(card) {
  const container = document.createElement('div');
  container.className = 'particles';

  for (let i = 0; i < 16; i++) {
    const particle = document.createElement('span');
    particle.className = 'particle';

    const angle = Math.random() * Math.PI * 2;
    const distance = 60 + Math.random() * 90;
    particle.style.setProperty('--tx', `${Math.cos(angle) * distance}px`);
    particle.style.setProperty('--ty', `${Math.sin(angle) * distance}px`);
    particle.style.background = PARTICLE_COLORS[Math.floor(Math.random() * PARTICLE_COLORS.length)];
    particle.style.animationDelay = `${Math.random() * 0.2}s`;

    container.appendChild(particle);
  }

  card.appendChild(container);
  setTimeout(() => container.remove(), 1300);
}

/* ============================================================
   Countdown tick (runs every second)
============================================================ */
function tick() {
  const now = Date.now();

  messages.forEach((msg) => {
    if (msg.revealed) return;

    const card = messagesContainer.querySelector(`[data-id="${msg.id}"]`);
    if (!card) return;

    const remaining = new Date(msg.unlockAt).getTime() - now;

    if (remaining <= 0) {
      msg.revealed = true;
      saveMessages();

      const temp = document.createElement('div');
      temp.innerHTML = unlockedCardTemplate(msg);
      const newCard = temp.firstElementChild;
      newCard.classList.add('revealing');

      card.replaceWith(newCard);
      createParticles(newCard);
      updateStats();

      showToast(`💌 A message for ${escapeHTML(msg.name)} just unlocked!`, 'success');
      return;
    }

    const { days, hours, minutes, seconds } = getTimeParts(remaining);
    const dayEl = card.querySelector('[data-unit="days"]');
    const hourEl = card.querySelector('[data-unit="hours"]');
    const minEl = card.querySelector('[data-unit="minutes"]');
    const secEl = card.querySelector('[data-unit="seconds"]');

    if (dayEl) dayEl.textContent = pad(days);
    if (hourEl) hourEl.textContent = pad(hours);
    if (minEl) minEl.textContent = pad(minutes);
    if (secEl) secEl.textContent = pad(seconds);

    const progress = getProgress(msg.createdAt, msg.unlockAt);
    const fill = card.querySelector('.progress-bar-fill');
    const percentLabel = card.querySelector('.progress-percent');
    if (fill) fill.style.width = `${progress}%`;
    if (percentLabel) percentLabel.textContent = `${Math.round(progress)}% there`;
  });
}

/* ============================================================
   Delete handling (click once to confirm)
============================================================ */
function handleContainerClick(event) {
  const btn = event.target.closest('[data-action="delete"]');
  if (!btn) return;

  const card = btn.closest('.capsule-card');
  const id = card.dataset.id;

  if (!btn.classList.contains('confirming')) {
    btn.classList.add('confirming');
    btn.textContent = 'Click again to confirm';
    btn._confirmTimeout = setTimeout(() => {
      btn.classList.remove('confirming');
      btn.textContent = 'Delete';
    }, 3000);
    return;
  }

  clearTimeout(btn._confirmTimeout);
  messages = messages.filter((m) => m.id !== id);
  saveMessages();

  card.classList.add('removing');
  card.addEventListener('animationend', () => renderAll(), { once: true });
  showToast('Capsule deleted.', 'success');
}

/* ============================================================
   Init
============================================================ */
function init() {
  initTheme();
  setMinDate();
  showQuote(false);
  startQuoteRotation();
  renderAll();

  themeToggle.addEventListener('click', toggleTheme);
  newQuoteBtn.addEventListener('click', () => {
    showQuote(true);
    startQuoteRotation();
  });
  capsuleForm.addEventListener('submit', handleFormSubmit);
  messagesContainer.addEventListener('click', handleContainerClick);

  setInterval(tick, 1000);
}

init();
