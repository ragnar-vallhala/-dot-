document.addEventListener('DOMContentLoaded', () => {
    let bookData = null;
    let currentChapterIndex = 0;

    const coverPage = document.getElementById('cover-page');
    const readerView = document.getElementById('reader-view');
    const contentContainer = document.getElementById('content-container');
    const tocList = document.getElementById('toc-list');
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menu-toggle');
    const hamburgerIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>`;
    const closeIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`;

    // Buttons
    const startBtn = document.getElementById('start-reading');
    const nextBtn = document.getElementById('next-ch');
    const prevBtn = document.getElementById('prev-ch');

    // Fetch Book Data
    fetch('book_data.json')
        .then(response => response.json())
        .then(data => {
            bookData = data;
            init();
        })
        .catch(err => console.error('Error loading book data:', err));

    function init() {
        renderTOC();
    }

    function renderTOC() {
        tocList.innerHTML = '';
        bookData.chapters.forEach((chapter, index) => {
            const li = document.createElement('li');
            li.className = 'toc-item';
            li.textContent = `${index + 1}. ${chapter.title}`;
            li.onclick = () => {
                currentChapterIndex = index;
                showChapter(index);
                sidebar.classList.remove('open');
                menuToggle.innerHTML = hamburgerIcon;
            };
            tocList.appendChild(li);
        });
    }

    function showChapter(index) {
        const chapter = bookData.chapters[index];
        if (!chapter) return;

        // Update UI
        coverPage.style.display = 'none';
        readerView.style.display = 'flex';

        // Render content
        let html = `<h2 class="chapter-title">${chapter.title}</h2>`;
        chapter.paragraphs.forEach(para => {
            html += `<p class="paragraph">${para}</p>`;
        });

        contentContainer.innerHTML = html;
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Update buttons
        prevBtn.disabled = index === 0;
        nextBtn.disabled = index === bookData.chapters.length - 1;

        // Update active TOC item
        const items = document.querySelectorAll('.toc-item');
        items.forEach((item, i) => {
            if (i === index) item.classList.add('active');
            else item.classList.remove('active');
        });

        // Save progress (optional)
        localStorage.setItem('currentChapter', index);
    }

    // Event Listeners
    startBtn.addEventListener('click', () => {
        showChapter(0);
    });

    nextBtn.addEventListener('click', () => {
        if (currentChapterIndex < bookData.chapters.length - 1) {
            currentChapterIndex++;
            showChapter(currentChapterIndex);
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentChapterIndex > 0) {
            currentChapterIndex--;
            showChapter(currentChapterIndex);
        }
    });

    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        menuToggle.innerHTML = sidebar.classList.contains('open') ? closeIcon : hamburgerIcon;
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
            sidebar.classList.remove('open');
            menuToggle.innerHTML = hamburgerIcon;
        }
    });
});
