document.addEventListener('DOMContentLoaded', () => {
    initDateControls();
    loadInsights();
});

function initDateControls() {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('target-date');
    dateInput.value = today;

    document.getElementById('refresh-btn').addEventListener('click', () => {
        loadInsights(dateInput.value);
    });

    updateDateDisplay(new Date());
}

function updateDateDisplay(dateObj) {
    const optionsDate = { year: 'numeric', month: 'long', day: 'numeric' };
    const optionsDay = { weekday: 'long' };

    document.getElementById('current-date').textContent = dateObj.toLocaleDateString('ko-KR', optionsDate);
    document.getElementById('current-day').textContent = dateObj.toLocaleDateString('ko-KR', optionsDay);
}

async function loadInsights(targetDate = null) {
    const container = document.getElementById('feed-container');
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
            <a href="#" class="read-btn" onclick="openOriginalEmail('${data.subject}')">Read Original Email →</a>
        </div>
    `;

    return article;
}

function openOriginalEmail(subject) {
    const searchUrl = `https://mail.naver.com/v2/folders/0/all/search/subject/${encodeURIComponent(subject)}`;
    window.open(searchUrl, '_blank');
}
