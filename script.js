/*---- Dark Mode Toggle ----*/
const themeToggle = document.querySelector('#theme-toggle');
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const isDark = document.body.classList.contains('dark');
    themeToggle.textContent = isDark ? '\u2600\uFE0F' : '\uD83C\uDF19';
});

/*---- To Top ----*/
const toTop = document.querySelector('#to-top');
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        toTop.classList.add('show');
    } else {
        toTop.classList.remove('show');
    }
});
toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

/*---- Load Repositories ----*/
async function loadRepositories() {
    const grid = document.querySelector('#repositories-grid');
    
    try {
        const response = await fetch('repositories.json');
        if (!response.ok) {
            throw new Error('Failed to load repositories');
        }
        
        const data = await response.json();
        const repos = data.repositories;
        
        if (!repos || repos.length === 0) {
            grid.innerHTML = '<div class="error">No repositories found.</div>';
            return;
        }
        
        // Sort by stars, then by last updated
        repos.sort((a, b) => {
            if (b.stars !== a.stars) return b.stars - a.stars;
            return new Date(b.updated_at) - new Date(a.updated_at);
        });
        
        // Create cards for each repository
        grid.innerHTML = repos.map(repo => createRepoCard(repo)).join('');
        
        // Add reveal animation to newly created cards
        const cards = grid.querySelectorAll('.repo-card');
        cards.forEach(card => {
            card.classList.add('reveal', 'is-visible');
        });
        
    } catch (error) {
        console.error('Error loading repositories:', error);
        grid.innerHTML = `<div class="error">Unable to load repositories. Please try again later.</div>`;
    }
}

function createRepoCard(repo) {
    const languageColor = getLanguageColor(repo.language);
    const topics = repo.topics && repo.topics.length > 0 
        ? repo.topics.slice(0, 3).map(topic => `<span class="repo-topic">${topic}</span>`).join('')
        : '';
    
    const homepage = repo.homepage ? `<a href="${repo.homepage}" target="_blank" rel="noopener" class="repo-link" title="Homepage">🔗</a>` : '';
    
    return `
        <article class="repo-card">
            <div class="repo-header">
                <a href="${repo.url}" target="_blank" rel="noopener" class="repo-name">${repo.name}</a>
                ${homepage}
            </div>
            <p class="repo-desc">${repo.description}</p>
            <div class="repo-meta">
                ${repo.language ? `<span class="repo-language"><span class="repo-stat-icon" style="color: ${languageColor}">●</span>${repo.language}</span>` : ''}
                ${repo.stars > 0 ? `<span class="repo-stat"><span class="repo-stat-icon">⭐</span>${repo.stars}</span>` : ''}
                ${repo.forks > 0 ? `<span class="repo-stat"><span class="repo-stat-icon">🔀</span>${repo.forks}</span>` : ''}
            </div>
            ${topics ? `<div class="repo-topics">${topics}</div>` : ''}
        </article>
    `;
}

function getLanguageColor(language) {
    const colors = {
        'JavaScript': '#f1e05a',
        'Python': '#3572A5',
        'TypeScript': '#2b7489',
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'Java': '#b07219',
        'C++': '#f34b7d',
        'Go': '#00ADD8',
        'Rust': '#ce422b',
        'PHP': '#777bb4',
        'C#': '#239120',
        'Swift': '#FA7343',
        'Kotlin': '#7F52FF',
    };
    return colors[language] || '#858585';
}

// Load repositories when DOM is ready
document.addEventListener('DOMContentLoaded', loadRepositories);

/*---- Scroll Reveal ----*/
const revealItems = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.15 });
revealItems.forEach(item => {
    observer.observe(item);
});