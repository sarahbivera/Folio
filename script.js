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

/* ---- Projects Filter ---- */
const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.projects-grid .project-card');
const projectCount = document.getElementById('project-count');

function updateCount() {
    const visible = Array.from(projectCards).filter(c => !c.classList.contains('hidden')).length;
    projectCount.textContent = `${visible} Project${visible !== 1 ? 's' : ''}`;
}

function filterProjects(category){
    projectCards.forEach(card => {
        const cats = (card.dataset.category || '')
            .split(',')
            .map(s => s.trim().toLowerCase())
            .filter(Boolean);
        const match = category === 'all' || cats.includes(category);
        if(match){
            card.classList.remove('hidden');
            card.classList.remove('hiding');
        } else {
            card.classList.add('hidden');
            card.classList.remove('hiding');
        }
    });
    updateCount();
}

filterButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const category = btn.dataset.filter;
        filterProjects(category);
    });
});


updateCount();