// Dark mode handling
const darkMode = document.getElementById('darkMode');
darkMode.checked = localStorage.getItem('darkMode') === 'true';
document.body.setAttribute('data-theme', darkMode.checked ? 'dark' : 'light');

darkMode.addEventListener('change', (e) => {
    const isDark = e.target.checked;
    document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
    localStorage.setItem('darkMode', isDark);
});

// Helper to format dates
function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString();
}

// Load and render conversations list
async function loadConversations() {
    const response = await fetch('/api/conversations');
    const conversations = await response.json();
    
    const container = document.getElementById('conversations');
    container.innerHTML = conversations.map(conv => `
        <div class="conversation-item" data-id="${conv.id}">
            <div class="conversation-title">${conv.title}</div>
            <div class="conversation-time">${formatDate(conv.timestamp)}</div>
        </div>
    `).join('');
    
    // Add click handlers
    container.querySelectorAll('.conversation-item').forEach(item => {
        item.addEventListener('click', () => loadConversation(item.dataset.id));
    });
}

// Load and render specific conversation
async function loadConversation(sessionId) {
    // Update active state
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.classList.toggle('active', item.dataset.id === sessionId);
    });
    
    const response = await fetch(`/api/conversation/${sessionId}`);
    const data = await response.json();
    
    const container = document.getElementById('messages');
    container.innerHTML = data.messages.map(msg => {
        // Special handling for selector decisions
        if (msg.role === 'Selector') {
            return `
                <div class="selector-decision">
                    <div class="selector-line"></div>
                    <div class="selector-content">
                        <span class="selector-icon">🔄</span>
                        Selector chose 
                        <span class="selector-choice">${msg.content.replace('Selected ', '')}</span>
                    </div>
                    <div class="selector-line"></div>
                </div>
            `;
        }

        const content = renderContent(msg.content);
        const needsCollapse = content.length > 500; // Collapse messages longer than 500 chars
        
        return `
            <div class="message ${msg.role.toLowerCase() === 'user' ? 'user' : msg.role}">
                <div class="message-header">
                    ${msg.role} • ${formatDate(msg.timestamp)}
                </div>
                <div class="message-content ${needsCollapse ? 'collapsed' : ''}" data-full-height="0">
                    ${content}
                    ${needsCollapse ? `
                        <div class="show-more-btn">
                            <span>Show more</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');

    // Add click handlers for show more buttons
    container.querySelectorAll('.show-more-btn').forEach(btn => {
        const content = btn.parentElement;
        const fullHeight = content.scrollHeight;
        content.dataset.fullHeight = fullHeight;
        
        btn.addEventListener('click', () => {
            const isCollapsed = content.classList.contains('collapsed');
            content.style.maxHeight = isCollapsed ? content.dataset.fullHeight + 'px' : '200px';
            content.classList.toggle('collapsed');
            content.classList.toggle('expanded');
            btn.querySelector('span').textContent = isCollapsed ? 'Show less' : 'Show more';
        });
    });
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

// Handle special content (images, code blocks)
function renderContent(content) {
    // Convert markdown image syntax
    content = content.replace(/!\[([^\]]*)\]\(([^)]*)\)/g, '<img src="$2" alt="$1">');
    
    // Convert markdown code blocks (basic)
    content = content.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => 
        `<pre><code class="language-${lang}">${escapeHtml(code.trim())}</code></pre>`
    );

    // Convert raw PDF paths to clickable links
    content = content.replace(/(?:output\\|output\/)[^\\\/\s)]+\.pdf/g, (match) => {
        // Replace backslashes with forward slashes
        const cleanPath = match.replace(/\\/g, '/');
        const href = cleanPath.startsWith('/') ? cleanPath : '/' + cleanPath;
        const filename = href.split('/').pop();
        return `<a href="${href}" target="_blank" rel="noopener">${filename}</a>`;
    });
    
    return content;
}

// HTML escaping helper
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initial load
loadConversations();

// Image modal handling
const imageModal = document.getElementById('imageModal');
const modalImg = imageModal.querySelector('img');

// Close modal when clicking outside the image
imageModal.addEventListener('click', (e) => {
    if (e.target === imageModal) {
        imageModal.classList.remove('visible');
    }
});

// Add click handlers to images
function setupImageHandlers() {
    document.querySelectorAll('.message img').forEach(img => {
        img.addEventListener('click', () => {
            modalImg.src = img.src;
            imageModal.classList.add('visible');
        });
    });
}

// Update the loadConversation function to setup image handlers
const originalLoadConversation = loadConversation;
loadConversation = async (sessionId) => {
    await originalLoadConversation(sessionId);
    setupImageHandlers();
};

// Optional: Poll for updates every 5 seconds
setInterval(loadConversations, 5000);
