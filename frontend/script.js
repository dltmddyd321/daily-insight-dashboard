document.addEventListener('DOMContentLoaded', () => {
    initDateControls();
    loadInsights();
});

function initDateControls() {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('target-date');
    if (dateInput) {
        dateInput.value = today;
    }

    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            loadInsights(dateInput.value);
        });
    }

    updateDateDisplay(new Date());
}

function updateDateDisplay(dateObj) {
    const optionsDate = { year: 'numeric', month: 'long', day: 'numeric' };
    const optionsDay = { weekday: 'long' };

    const dateEl = document.getElementById('current-date');
    const dayEl = document.getElementById('current-day');

    if (dateEl) dateEl.textContent = dateObj.toLocaleDateString('ko-KR', optionsDate);
    if (dayEl) dayEl.textContent = dateObj.toLocaleDateString('ko-KR', optionsDay);
}

async function loadInsights(targetDate = null) {
    const container = document.getElementById('feed-container');
    if (!container) return;

    container.innerHTML = '<div class="loading">Fetching insights from server...</div>';

    if (targetDate) {
        updateDateDisplay(new Date(targetDate));
    }

    try {
        const url = targetDate
            ? `http://127.0.0.1:8000/api/insights?date=${targetDate}`
            : `http://127.0.0.1:8000/api/insights`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const result = await response.json();
        const data = result.insights;

        // Clear loading state
        container.innerHTML = '';

        if (!data || data.length === 0) {
            container.innerHTML = '<div class="loading">No insights found for this date.</div>';
            return;
        }

        // Render cards
        data.forEach((item, index) => {
            const card = createCard(item, index);
            container.appendChild(card);
        });

    } catch (error) {
        console.error('Error loading insights:', error);
        container.innerHTML = `<div class="loading">
            <p>Error connecting to API server.</p>
            <p style="font-size: 0.9rem; margin-top: 10px;">Make sure the backend server (run.py) is running.</p>
            <p style="font-size: 0.8rem; color: #888;">(${error.message})</p>
        </div>`;
    }
}

function createCard(data, index) {
    const article = document.createElement('article');
    article.className = 'insight-card';
    article.style.animationDelay = `${index * 0.1}s`;

    const category = data.category || 'General';
    const summary = data.summary || 'No summary available.';
    const keyPoints = data.key_points || [];
    const actionable = data.actionable_item;

    const keyPointsHtml = keyPoints.map(point => `<li>${point}</li>`).join('');

    const actionableHtml = actionable
        ? `<div class="actionable-item">
            <span class="actionable-title">💡 Action Item</span>
            ${actionable}
           </div>`
        : '';

    article.innerHTML = `
        <div class="card-header">
            <div class="sender-info">${data.sender}</div>
            <span class="card-category">${category}</span>
        </div>
        
        <h2 class="card-title">${data.subject}</h2>
        <p style="color: #555; margin-bottom: 1.5rem;">${summary}</p>
        
        <ul class="insight-list">
            ${keyPointsHtml}
        </ul>
        
        ${actionableHtml}
        
        <div class="card-actions">
            <button class="read-btn">Read Original Email →</button>
        </div>
    `;

    // Add event listener to the button
    const readBtn = article.querySelector('.read-btn');
    if (readBtn) {
        readBtn.addEventListener('click', () => {
            openOriginalEmail(data.id);
        });
    }

    return article;
}

function openOriginalEmail(mailId) {
    // Direct link to Naver Mail using Folder 0 (Inbox) and the Mail ID (UID)
    const directLink = `https://mail.naver.com/v2/read/0/${mailId}`;
    window.open(directLink, '_blank');
}
