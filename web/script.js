// =========================================================
// WORKSPACE SWITCHING
// =========================================================
const navItems = document.querySelectorAll('.nav-item[data-workspace]');
const workspaces = document.querySelectorAll('.workspace');

navItems.forEach((item) => {
  item.addEventListener('click', () => {
    const target = item.dataset.workspace;

    navItems.forEach((n) => n.classList.remove('is-active'));
    item.classList.add('is-active');

    workspaces.forEach((w) => w.classList.remove('is-active'));
    const targetWorkspace = document.getElementById(`workspace-${target}`);
    if (targetWorkspace) targetWorkspace.classList.add('is-active');
  });
});

// =========================================================
// AGENT STATUS (drives sidebar mark + right rail label + colors)
// =========================================================
const agentMark = document.querySelector('.agent-mark');
const agentStateLabel = document.getElementById('agentStateLabel');
const statusRailDot = document.querySelector('.status-rail-dot');
const chatStatusDot = document.querySelector('.status-dot');

const STATE_COLORS = {
  idle: 'var(--state-idle)',
  working: 'var(--state-working)',
  completed: 'var(--state-completed)',
  attention: 'var(--state-attention)',
  error: 'var(--state-error)',
};

const STATE_LABELS = {
  idle: 'Idle',
  working: 'Working',
  completed: 'Completed',
  attention: 'Needs attention',
  error: 'Error',
};

function setAgentState(state) {
  const color = STATE_COLORS[state] || STATE_COLORS.idle;

  if (agentMark) {
    agentMark.style.color = color;
    agentMark.setAttribute('data-state', state);
    agentMark.title = `Agent status: ${STATE_LABELS[state]}`;
  }
  if (statusRailDot) {
    statusRailDot.style.background = color;
    statusRailDot.style.boxShadow = `0 0 8px ${color}`;
  }
  if (agentStateLabel) {
    agentStateLabel.textContent = STATE_LABELS[state] || 'Idle';
  }
  if (chatStatusDot) {
    chatStatusDot.style.background = color;
    chatStatusDot.style.boxShadow = `0 0 8px ${color}`;
  }
}

setAgentState('idle');

// =========================================================
// Chat: Real
// =========================================================
function addAIMessage(message) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "msg msg-agent";
  div.textContent = message;
  
  chat.appendChild(div);
}

function addUSerMessage(message) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "msg msg-agent";
  div.textContent = message;
  chat,appendChild(div);
}

async function SendMessage(message) {
  addUSerMessage(message);
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: message
    })
  });
  
  const data = await response.json();
  addAIMessage(data.response);
}

// =========================================================
// CHAT: fake send flow
// =========================================================
const chatEmpty = document.getElementById('chatEmpty');
const chatThread = document.getElementById('chatThread');
const thinkingRow = document.getElementById('thinkingRow');
const chatBody = document.getElementById('chatBody');
const composerInput = document.getElementById('composerInput');
const sendBtn = document.getElementById('sendBtn');

const FAKE_REPLIES = [
  "Got it. I'll keep working on that in the background.",
  "Noted — I'll flag anything relevant as soon as I see it.",
  "Done. Let me know if you want me to go deeper on any part of it.",
  "On it. I'll check back with what I find.",
];

function autoGrow() {
  composerInput.style.height = 'auto';
  composerInput.style.height = `${Math.min(composerInput.scrollHeight, 140)}px`;
}
composerInput.addEventListener('input', autoGrow);

function scrollChatToBottom() {
  chatBody.scrollTop = chatBody.scrollHeight;
}

function appendMessage(role, text) {
  const msg = document.createElement('div');
  msg.className = `msg msg-${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.textContent = text;
  msg.appendChild(bubble);
  chatThread.appendChild(msg);
}

function sendMessage() {
  const text = composerInput.value.trim();
  if (!text) return;

  chatEmpty.hidden = true;
  chatThread.hidden = false;

  appendMessage('user', text);
  composerInput.value = '';
  autoGrow();
  scrollChatToBottom();

  setAgentState('working');
  thinkingRow.hidden = false;
  scrollChatToBottom();

  setTimeout(() => {
    thinkingRow.hidden = true;
    const reply = FAKE_REPLIES[Math.floor(Math.random() * FAKE_REPLIES.length)];
    appendMessage('agent', reply);
    setAgentState('completed');
    scrollChatToBottom();

    setTimeout(() => setAgentState('idle'), 2200);
  }, 1100);
}

sendBtn.addEventListener('click', sendMessage);
composerInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// =========================================================
// VOICE: state cycling on mic click
// =========================================================
const orb = document.getElementById('orb');
const voiceStatus = document.getElementById('voiceStatus');
const micBtn = document.getElementById('micBtn');

const VOICE_LABELS = {
  ready: 'Ready',
  listening: 'Listening',
  thinking: 'Thinking',
  speaking: 'Speaking',
};

let voiceState = 'ready';
let voiceTimers = [];

function clearVoiceTimers() {
  voiceTimers.forEach((t) => clearTimeout(t));
  voiceTimers = [];
}

function setVoiceState(state) {
  voiceState = state;
  orb.setAttribute('data-state', state);
  voiceStatus.textContent = VOICE_LABELS[state] || 'Ready';
}

micBtn.addEventListener('click', () => {
  clearVoiceTimers();

  if (voiceState === 'ready') {
    setVoiceState('listening');
    setAgentState('working');

    voiceTimers.push(setTimeout(() => {
      setVoiceState('thinking');
    }, 1800));

    voiceTimers.push(setTimeout(() => {
      setVoiceState('speaking');
      setAgentState('completed');
    }, 3200));

    voiceTimers.push(setTimeout(() => {
      setVoiceState('ready');
      setAgentState('idle');
    }, 5200));
  } else {
    setVoiceState('ready');
    setAgentState('idle');
  }
});

// =========================================================
// ANALYSIS: Add Tracker modal
// =========================================================
const addTrackerBtn = document.getElementById('addTrackerBtn');
const modalOverlay = document.getElementById('modalOverlay');
const modalClose = document.getElementById('modalClose');
const modalCancel = document.getElementById('modalCancel');
const modalCreate = document.getElementById('modalCreate');
const trackerGrid = document.getElementById('trackerGrid');

const trackerName = document.getElementById('trackerName');
const trackerWhat = document.getElementById('trackerWhat');
const trackerFrequency = document.getElementById('trackerFrequency');

function openModal() {
  modalOverlay.hidden = false;
  trackerName.focus();
}

function closeModal() {
  modalOverlay.hidden = true;
  trackerName.value = '';
  trackerWhat.value = '';
  trackerFrequency.selectedIndex = 1;
}

addTrackerBtn.addEventListener('click', openModal);
modalClose.addEventListener('click', closeModal);
modalCancel.addEventListener('click', closeModal);
modalOverlay.addEventListener('click', (e) => {
  if (e.target === modalOverlay) closeModal();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !modalOverlay.hidden) closeModal();
});

function createTrackerCard(name, desc) {
  const card = document.createElement('div');
  card.className = 'tracker-card';
  card.innerHTML = `
    <div class="tracker-card-top">
      <span class="tracker-title"></span>
      <span class="tracker-status" data-state="working">
        <span class="tracker-status-dot"></span>
        Watching
      </span>
    </div>
    <p class="tracker-desc"></p>
    <span class="tracker-meta">Just now</span>
  `;
  card.querySelector('.tracker-title').textContent = name;
  card.querySelector('.tracker-desc').textContent = desc;
  return card;
}

modalCreate.addEventListener('click', () => {
  const name = trackerName.value.trim();
  const what = trackerWhat.value.trim();

  if (!name || !what) {
    trackerName.style.borderColor = name ? 'var(--border)' : 'var(--state-error)';
    trackerWhat.style.borderColor = what ? 'var(--border)' : 'var(--state-error)';
    return;
  }

  const card = createTrackerCard(name, what);
  trackerGrid.appendChild(card);
  setAgentState('working');
  setTimeout(() => setAgentState('idle'), 1600);
  closeModal();
});
