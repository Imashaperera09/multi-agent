const API_URL = 'http://localhost:8000';

const analyzeBtn = document.getElementById('analyze-btn');
const statusText = document.getElementById('status-text');
const thinkingProcess = document.getElementById('thinking-process');
const thoughtStream = document.getElementById('thought-stream');
const riskCount = document.getElementById('risk-count');
const stockHealth = document.getElementById('stock-health');
const disruptionList = document.getElementById('disruption-list');
const mitigationList = document.getElementById('mitigation-list');

const agentBadges = {
    'Risk Sentinel': document.getElementById('risk-badge'),
    'Inventory Analyst': document.getElementById('inventory-badge'),
    'Logistics Optimizer': document.getElementById('logistics-badge'),
    'system': null
};

analyzeBtn.addEventListener('click', async () => {
    try {
        resetUI();
        setSystemStatus('ANALYZING...', 'var(--accent-color)');
        analyzeBtn.disabled = true;
        thinkingProcess.classList.remove('hidden');

        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: 'global supply chain risks' })
        });

        if (!response.ok) throw new Error('Analysis failed');

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
    disruptionList.innerHTML = '<p class="placeholder">Analyzing...</p>';
    mitigationList.innerHTML = '<p class="placeholder">Analyzing...</p>';
    riskCount.innerText = '0';
    stockHealth.innerText = '--';
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

    // Render Disruptions
    setTimeout(() => {
        disruptionList.innerHTML = '';
        data.disruptions.forEach(d => {
            const item = document.createElement('div');
            item.className = 'disruption-item';
            item.innerHTML = `
                <h4>${d.type}: ${d.location} <span class="badge severity-${d.severity.toLowerCase()}">${d.severity}</span></h4>
                <p>${d.description}</p>
                <small style="color: #4a5568">Source: ${d.source}</small>
            `;
            disruptionList.appendChild(item);
        });
        riskCount.innerText = data.disruptions.length;
    }, data.thoughts.length * 1000);

    // Render Mitigation
    setTimeout(() => {
        mitigationList.innerHTML = '';
        data.mitigation_plan.forEach(m => {
            const item = document.createElement('div');
            item.className = 'strategy-item';
            item.innerHTML = `
                <h4>${m.action} <span class="badge" style="background: rgba(0, 242, 255, 0.1); border: 1px solid var(--accent-color)">${m.priority}</span></h4>
                <p>${m.impact}</p>
            `;
            mitigationList.appendChild(item);
        });

        // Calculate Stock Health
        const atRisk = data.inventory.filter(i => i.status !== 'OK').length;
        stockHealth.innerText = atRisk > 0 ? 'AT RISK' : 'HEALTHY';
        stockHealth.style.color = atRisk > 0 ? 'var(--danger-color)' : 'var(--success-color)';
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

    // Render user message
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
