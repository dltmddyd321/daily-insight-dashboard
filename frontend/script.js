document.addEventListener('DOMContentLoaded', () => {
    updateDate();
    loadInsights();
});

function updateDate() {
    const now = new Date();
    const optionsDate = { year: 'numeric', month: 'long', day: 'numeric' };
    const optionsDay = { weekday: 'long' };

    document.getElementById('current-date').textContent = now.toLocaleDateString('ko-KR', optionsDate);
    document.getElementById('current-day').textContent = now.toLocaleDateString('ko-KR', optionsDay);
}

async function loadInsights() {
    const container = document.getElementById('feed-container');

    try {
        // Check if data loaded from data.js
        if (typeof DAILY_INSIGHTS === 'undefined') {
            throw new Error('Data file (data.js) not loaded. Run the main script first.');
        }

        const data = DAILY_INSIGHTS;

        // Clear loading state
        container.innerHTML = '';

        if (data.length === 0) {
            container.innerHTML = '<div class="loading">No insights found for today.</div>';
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
            <p>Waiting for data...</p>
            <p style="font-size: 0.9rem; margin-top: 10px;">(Error: ${error.message})</p>
        </div>`;
    }
}

function createCard(data, index) {
    const article = document.createElement('article');
    article.className = 'insight-card';
    article.style.animationDelay = `${index * 0.1}s`;

    // Default values if missing
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
            <a href="#" class="read-btn" onclick="openOriginalEmail('${data.id}')">Read Original Email →</a>
        </div>
    `;

    return article;
}

function openOriginalEmail(id) {
    // Find the item to get the subject
    const item = DAILY_INSIGHTS.find(i => i.id === id);
    if (!item) {
        window.open('https://mail.naver.com', '_blank');
        return;
    }

    // Creating a search URL for Naver Mail
    // Note: The specific URL structure may vary, but searching by subject is generally reliable.
    // Try the PC web version search parameter.
    const searchUrl = `https://mail.naver.com/v2/folders/0/all/search/subject/${encodeURIComponent(item.subject)}`;

    // Alternative fallback if the V2 URL structure changes:
    // const searchUrl = `https://mail.naver.com/#/search/all?query=${encodeURIComponent(item.subject)}`;

    window.open(searchUrl, '_blank');
}
