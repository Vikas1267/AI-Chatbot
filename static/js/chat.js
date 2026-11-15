/* ═══════════════════════════════════════════
   ARIA Chat — chat.js
   Clean, minimal frontend logic
═══════════════════════════════════════════ */

'use strict';

// ── Session ──────────────────────────────────────────────────────────────────
let sessionId = sessionStorage.getItem('aria_session_id');
if (!sessionId) {
  sessionId = 'sess_' + Math.random().toString(36).slice(2) + Date.now().toString(36);
  sessionStorage.setItem('aria_session_id', sessionId);
}

// ── DOM refs ─────────────────────────────────────────────────────────────────
const messagesEl      = document.getElementById('messages');
const typingEl        = document.getElementById('typingIndicator');
const quickRepliesEl  = document.getElementById('quickReplies');
const userInputEl     = document.getElementById('userInput');
const sendBtnEl       = document.getElementById('sendBtn');
const clearBtnEl      = document.getElementById('clearBtn');
const exportBtnEl     = document.getElementById('exportBtn');
const themeBtnEl      = document.getElementById('themeBtn');
const moonIconEl      = document.getElementById('moonIcon');
const sunIconEl       = document.getElementById('sunIcon');

// ── Theme ─────────────────────────────────────────────────────────────────────
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  if (theme === 'light') {
    moonIconEl.style.display = 'none';
    sunIconEl.style.display  = '';
  } else {
    moonIconEl.style.display = '';
    sunIconEl.style.display  = 'none';
  }
}

(function initTheme() {
  const saved = localStorage.getItem('aria_theme') || 'dark';
  applyTheme(saved);
})();

themeBtnEl.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  localStorage.setItem('aria_theme', next);
});

// ── Helpers ───────────────────────────────────────────────────────────────────
function formatTime(date) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

// ── Display message ───────────────────────────────────────────────────────────
// No intent badge, no confidence bar — just avatar (bot), bubble, timestamp
function displayMessage(text, sender) {
  const row = document.createElement('div');
  row.className = `message-row ${sender}`;

  if (sender === 'bot') {
    const avatar = document.createElement('div');
    avatar.className = 'bot-avatar';
    avatar.textContent = '✦';
    row.appendChild(avatar);
  }

  const wrap = document.createElement('div');
  wrap.className = 'bubble-wrap';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;

  const ts = document.createElement('div');
  ts.className = 'timestamp';
  ts.textContent = formatTime(new Date());

  wrap.appendChild(bubble);
  wrap.appendChild(ts);
  row.appendChild(wrap);

  messagesEl.appendChild(row);
  scrollToBottom();
}

function displayError(msg) {
  displayMessage(msg || 'Something went wrong. Please try again.', 'bot');
}

// ── Typing indicator ──────────────────────────────────────────────────────────
function showTyping()  { typingEl.style.display = 'flex'; scrollToBottom(); }
function hideTyping()  { typingEl.style.display = 'none';  }

// ── Send message ──────────────────────────────────────────────────────────────
let isSending = false;

async function sendMessage(text) {
  text = (text || userInputEl.value).trim();
  if (!text || isSending) return;

  isSending = true;
  userInputEl.value = '';
  autoResize();

  // Hide quick replies after first send
  quickRepliesEl.style.display = 'none';

  displayMessage(text, 'user');

  // Random typing delay 600–1200 ms for realism
  const delay = 600 + Math.random() * 600;
  showTyping();
  await new Promise(r => setTimeout(r, delay));
  hideTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    displayMessage(data.response || '(no response)', 'bot');
  } catch (err) {
    console.error('Chat error:', err);
    displayError("I'm having trouble connecting right now. Please try again.");
  } finally {
    isSending = false;
  }
}

// ── Input auto-resize ─────────────────────────────────────────────────────────
function autoResize() {
  userInputEl.style.height = 'auto';
  userInputEl.style.height = Math.min(userInputEl.scrollHeight, 140) + 'px';
}

userInputEl.addEventListener('input', autoResize);

userInputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

sendBtnEl.addEventListener('click', () => sendMessage());

// ── Quick replies ─────────────────────────────────────────────────────────────
quickRepliesEl.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    sendMessage(chip.dataset.query);
  });
});

// ── Clear chat ────────────────────────────────────────────────────────────────
clearBtnEl.addEventListener('click', () => {
  messagesEl.innerHTML = '';
  hideTyping();
  quickRepliesEl.style.display = 'flex';
  showWelcome();
});

// ── Export chat ───────────────────────────────────────────────────────────────
exportBtnEl.addEventListener('click', () => {
  const rows = messagesEl.querySelectorAll('.message-row');
  if (!rows.length) return;

  const lines = ['ARIA Chat Export', '='.repeat(40), ''];
  rows.forEach(row => {
    const sender = row.classList.contains('user') ? 'You' : 'ARIA';
    const bubble = row.querySelector('.bubble');
    const ts     = row.querySelector('.timestamp');
    if (bubble) {
      lines.push(`[${ts ? ts.textContent : ''}] ${sender}: ${bubble.textContent}`);
    }
  });

  const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `aria-chat-${new Date().toISOString().slice(0,10)}.txt`;
  a.click();
  URL.revokeObjectURL(url);
});

// ── Welcome message ───────────────────────────────────────────────────────────
function showWelcome() {
  displayMessage("Hi! I'm ARIA. How can I help you today? 😊", 'bot');
}

// ── Init ──────────────────────────────────────────────────────────────────────
showWelcome();
