const API_URL = 'https://multi-agent-azqa.onrender.com';

const analyzeBtn = document.getElementById('analyze-btn');
const researchInput = document.getElementById('research-query');
const statusText = document.getElementById('status-text');
const thinkingProcess = document.getElementById('thinking-process');
const thoughtStream = document.getElementById('thought-stream');
const findingsCount = document.getElementById('risk-count');
const knowledgeStatus = document.getElementById('stock-health');
const findingsList = document.getElementById('disruption-list');
const strategyList = document.getElementById('mitigation-list');

const agentBadges = {
    'Research Scout': document.getElementById('risk-badge'),
    'Critical Analyst': document.getElementById('inventory-badge'),
    'Strategy Advisor': document.getElementById('logistics-badge'),
    'system': null
};

analyzeBtn.addEventListener('click', async () => {
    const query = researchInput.value.trim();
    if (!query) {
        alert("Please enter a research topic.");
        return;
    }

    try {
        resetUI();
        setSystemStatus('RESEARCHING...', 'var(--accent-color)');
        analyzeBtn.disabled = true;
        thinkingProcess.classList.remove('hidden');

        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) throw new Error('Research failed');

        const data = await response.json();
        renderResults(data);
        setSystemStatus('ANALYSIS COMPLETE', 'var(--success-color)');
    } catch (error) {
        console.error(error);
        setSystemStatus('SYSTEM ERROR', 'var(--danger-color)');
        thoughtStream.innerHTML += `<div class="thought-entry"><span class="agent-name" style="color:red">ERROR</span> ${error.message}</div>`;
    } finally {
        analyzeBtn.disabled = false;
    }
});

function resetUI() {
    thoughtStream.innerHTML = '';
    findingsList.innerHTML = '<p class="placeholder">Searching...</p>';
    strategyList.innerHTML = '<p class="placeholder">Analyzing...</p>';
    findingsCount.innerText = '0';
    knowledgeStatus.innerText = '--';
    Object.values(agentBadges).forEach(badge => badge?.classList.remove('active'));
}

function setSystemStatus(text, color) {
    statusText.innerText = text;
    statusText.style.color = color;
    document.querySelector('.status-indicator').style.background = color;
    document.querySelector('.status-indicator').style.boxShadow = `0 0 8px ${color}`;
}

function renderResults(data) {
    // Render Thoughts sequentially for effect
    data.thoughts.forEach((t, index) => {
        setTimeout(() => {
            const entry = document.createElement('div');
            entry.className = 'thought-entry';
            entry.innerHTML = `<span class="agent-name">${t.agent}</span> ${t.thought}`;
            thoughtStream.appendChild(entry);
            thoughtStream.scrollTop = thoughtStream.scrollHeight;

            // Highlight active agent
            Object.values(agentBadges).forEach(b => b?.classList.remove('active'));
            if (agentBadges[t.agent]) agentBadges[t.agent].classList.add('active');
        }, index * 1000);
    });

    // Render Findings
    setTimeout(() => {
        findingsList.innerHTML = '';
        if (data.findings.length === 0) {
            findingsList.innerHTML = '<p class="placeholder">No specific findings found for this topic.</p>';
        }
        data.findings.forEach(f => {
            const item = document.createElement('div');
            item.className = 'disruption-item'; // Keep class for styling
            item.innerHTML = `
                <h4>${f.category}: ${f.title}</h4>
                <p>${f.description}</p>
                <small style="color: #4a5568">Source: ${f.source}</small>
            `;
            findingsList.appendChild(item);
        });
        findingsCount.innerText = data.findings.length;
    }, data.thoughts.length * 1000);

    // Render Strategies
    setTimeout(() => {
        strategyList.innerHTML = '';
        data.strategies.forEach(s => {
            const item = document.createElement('div');
            item.className = 'strategy-item';
            item.innerHTML = `
                <h4>${s.recommendation} <span class="badge" style="background: rgba(0, 242, 255, 0.1); border: 1px solid var(--accent-color)">Confidence: ${s.confidence}</span></h4>
                <p>${s.impact}</p>
            `;
            strategyList.appendChild(item);
        });

        // Knowledge Hub Status
        const topicsCount = data.knowledge_hub.length;
        knowledgeStatus.innerText = topicsCount > 0 ? topicsCount : '--';
        knowledgeStatus.style.color = 'var(--success-color)';
    }, (data.thoughts.length + 1) * 1000);
}

/* AI Co-pilot Chat Logic */
const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const closeChat = document.getElementById('close-chat');
const sendChat = document.getElementById('send-chat');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

chatToggle.addEventListener('click', () => {
    chatWindow.classList.toggle('hidden');
    if (!chatWindow.classList.contains('hidden')) {
        chatInput.focus();
    }
});

closeChat.addEventListener('click', () => {
    chatWindow.classList.add('hidden');
});

sendChat.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const msg = chatInput.value.trim();
    if (!msg) return;

    appendMessage(msg, 'user-msg');
    chatInput.value = '';

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });

        if (!response.ok) throw new Error('Chat failed');

        const data = await response.json();
        appendMessage(data.response, 'ai-msg');
    } catch (error) {
        console.error(error);
        appendMessage(`Error: ${error.message}`, 'ai-msg');
    }
}

function appendMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.className = className;
    msgDiv.innerText = text;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
