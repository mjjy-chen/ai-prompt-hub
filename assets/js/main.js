// AI Prompt Hub - 主交互脚本 v2.0

document.addEventListener('DOMContentLoaded', function() {
    initCopyButtons();
    initSearch();
    initCategoryFilter();
});

// 复制功能
function initCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const targetId = this.dataset.target;
            const targetElement = document.getElementById(targetId);
            if (!targetElement) return;
            
            const text = targetElement.textContent || targetElement.innerText;
            
            try {
                await navigator.clipboard.writeText(text);
                showToast('✅ 已复制到剪贴板');
                const originalText = this.innerHTML;
                this.innerHTML = '✓ 已复制';
                this.classList.add('copied');
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('copied');
                }, 2000);
            } catch (err) {
                // Fallback for non-HTTPS
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand('copy');
                    showToast('✅ 已复制到剪贴板');
                } catch(e) {
                    showToast('❌ 复制失败，请手动复制');
                }
                document.body.removeChild(textarea);
            }
        });
    });
}

// 搜索功能 - 修复路径问题
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    if (!searchInput) return;
    
    let searchData = [];
    
    // 自动检测base路径（支持GitHub Pages子目录）
    const basePath = detectBasePath();
    const searchUrl = basePath + 'search.json';
    
    fetch(searchUrl)
        .then(res => {
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return res.json();
        })
        .then(data => {
            searchData = data;
            console.log('搜索数据加载成功:', searchData.length, '条');
        })
        .catch(err => {
            console.log('搜索数据加载失败:', err, 'URL:', searchUrl);
        });
    
    // 实时搜索
    let debounceTimer;
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const query = this.value.trim().toLowerCase();
            
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.classList.remove('active');
                return;
            }
            
            const results = searchData.filter(item => {
                return (item.title && item.title.toLowerCase().includes(query)) ||
                       (item.title_en && item.title_en.toLowerCase().includes(query)) ||
                       (item.description && item.description.toLowerCase().includes(query)) ||
                       (item.description_en && item.description_en.toLowerCase().includes(query)) ||
                       (item.tags && item.tags.some(tag => tag.toLowerCase().includes(query))) ||
                       (item.tags_en && item.tags_en.some(tag => tag.toLowerCase().includes(query)));
            }).slice(0, 8);
            
            renderSearchResults(results, query, basePath);
        }, 200);
    });
    
    // 点击外部关闭
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            searchResults.classList.remove('active');
        }
    });
}

// 检测base路径
function detectBasePath() {
    // 从当前URL推断：如果路径包含 /ai-prompt-hub/，说明在GitHub Pages子目录
    const path = window.location.pathname;
    if (path.includes('/ai-prompt-hub')) {
        return '/ai-prompt-hub/';
    }
    // 本地开发
    if (path.includes('/prompts/') || path.includes('/agents/')) {
        const parts = path.split('/');
        // /prompts/xxx/ → ../, /agents/xxx/ → ../
        if (parts.length > 2) {
            return '../';
        }
        return './';
    }
    return '/';
}

function renderSearchResults(results, query, basePath) {
    const searchResults = document.getElementById('search-results');
    if (!searchResults) return;
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-no-results">未找到相关内容 / No results found</div>';
        searchResults.classList.add('active');
        return;
    }
    
    const html = results.map(item => {
        // 修正URL：确保链接正确
        let url = item.url;
        if (url.startsWith('/')) {
            // 绝对路径需要加base
            if (basePath && basePath !== '/') {
                url = basePath + url.replace(/^\//, '');
            }
        }
        
        const langIcon = item.language === 'en' ? '🇺🇸' : item.language === 'zh' ? '🇨🇳' : '🌐';
        const typeIcon = item.type === 'agent' ? '👤' : '💡';
        
        return `<a href="${url}" class="search-result-item">
            <div class="search-result-title">${typeIcon} ${langIcon} ${highlightText(item.title, query)}</div>
            <div class="search-result-desc">${highlightText(item.description || '', query)}</div>
            <div class="search-result-tags">
                ${(item.tags || []).slice(0, 3).map(tag => `<span class="search-tag">${tag}</span>`).join('')}
            </div>
        </a>`;
    }).join('');
    
    searchResults.innerHTML = html;
    searchResults.classList.add('active');
}

function highlightText(text, query) {
    if (!query || !text) return text || '';
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// 分类过滤
function initCategoryFilter() {
    document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn[data-filter]').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.dataset.filter;
            document.querySelectorAll('.card').forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
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
