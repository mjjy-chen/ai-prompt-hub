// AI Prompt Hub - 主交互脚本

document.addEventListener('DOMContentLoaded', function() {
    // 初始化复制按钮
    initCopyButtons();
    
    // 初始化搜索功能
    initSearch();
});

// 复制功能
function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(btn => {
        btn.addEventListener('click', async function() {
            const targetId = this.dataset.target;
            const targetElement = document.getElementById(targetId);
            
            if (!targetElement) return;
            
            const text = targetElement.textContent || targetElement.innerText;
            
            try {
                await navigator.clipboard.writeText(text);
                showToast('✅ 已复制到剪贴板');
                
                // 按钮反馈
                const originalText = this.innerHTML;
                this.innerHTML = '✓ 已复制';
                this.classList.add('copied');
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('copied');
                }, 2000);
            } catch (err) {
                showToast('❌ 复制失败，请手动复制');
            }
        });
    });
}

// 搜索功能
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput) return;
    
    let searchData = [];
    
    // 加载搜索数据
    fetch('/search.json')
        .then(res => res.json())
        .then(data => {
            searchData = data;
        })
        .catch(err => console.log('搜索数据加载失败:', err));
    
    // 实时搜索
    searchInput.addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.classList.remove('active');
            return;
        }
        
        const results = searchData.filter(item => {
            return item.title.toLowerCase().includes(query) ||
                   item.description.toLowerCase().includes(query) ||
                   item.tags.some(tag => tag.toLowerCase().includes(query));
        }).slice(0, 8);
        
        renderSearchResults(results, query);
    });
    
    // 点击外部关闭搜索结果
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            searchResults.classList.remove('active');
        }
    });
}

function renderSearchResults(results, query) {
    const searchResults = document.getElementById('search-results');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-no-results">未找到相关内容</div>';
        searchResults.classList.add('active');
        return;
    }
    
    const html = results.map(item => `
        <a href="${item.url}" class="search-result-item">
            <div class="search-result-title">${highlightText(item.title, query)}</div>
            <div class="search-result-desc">${highlightText(item.description, query)}</div>
            <div class="search-result-tags">
                ${item.tags.slice(0, 3).map(tag => `<span class="search-tag">${tag}</span>`).join('')}
            </div>
        </a>
    `).join('');
    
    searchResults.innerHTML = html;
    searchResults.classList.add('active');
}

function highlightText(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Toast提示
function showToast(message) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
