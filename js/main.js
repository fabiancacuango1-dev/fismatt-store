/* ============================================
   FISMATT SYSTEMS — Main JavaScript v3.0
   Premium Redesign
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMobileMenu();
    initScrollReveal();
    initFAQ();
    initSmoothScroll();
    initActiveNavLinks();
    initCloudTabs();
    initProofCarousel();
});

/* ---- Real product carousel ---- */
function initProofCarousel() {
    const carousel = document.querySelector('[data-proof-carousel]');
    if (!carousel) return;

    const track = carousel.querySelector('.proof-gallery');
    const slides = Array.from(carousel.querySelectorAll('.proof-shot'));
    const dotsContainer = carousel.querySelector('[data-proof-dots]');
    const currentLabel = carousel.querySelector('[data-proof-current]');
    const previous = carousel.querySelector('[data-proof-prev]');
    const next = carousel.querySelector('[data-proof-next]');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let current = 0;
    let timer;

    const dots = slides.map((_, index) => {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.setAttribute('aria-label', `Ver imagen ${index + 1}`);
        dot.addEventListener('click', () => goTo(index, true));
        dotsContainer.appendChild(dot);
        return dot;
    });

    function goTo(index, restart = false) {
        current = (index + slides.length) % slides.length;
        track.style.transform = `translate3d(-${current * 100}%, 0, 0)`;
        currentLabel.textContent = String(current + 1).padStart(2, '0');
        slides.forEach((slide, slideIndex) => {
            slide.setAttribute('aria-hidden', slideIndex === current ? 'false' : 'true');
        });
        dots.forEach((dot, dotIndex) => {
            const active = dotIndex === current;
            dot.classList.toggle('active', active);
            dot.setAttribute('aria-current', active ? 'true' : 'false');
        });
        if (restart) start();
    }

    function stop() {
        window.clearInterval(timer);
    }

    function start() {
        stop();
        if (!reducedMotion) timer = window.setInterval(() => goTo(current + 1), 6000);
    }

    previous.addEventListener('click', () => goTo(current - 1, true));
    next.addEventListener('click', () => goTo(current + 1, true));
    carousel.addEventListener('pointerenter', stop);
    carousel.addEventListener('pointerleave', start);
    carousel.addEventListener('focusin', stop);
    carousel.addEventListener('focusout', start);
    goTo(0);
    start();
}

/* ---- Navbar Scroll Effect ---- */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    let ticking = false;
    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(() => {
                navbar.classList.toggle('scrolled', window.scrollY > 30);
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

/* ---- Mobile Menu Toggle ---- */
function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    if (!btn || !menu) return;

    btn.addEventListener('click', () => {
        const isOpen = menu.classList.contains('open');
        if (isOpen) {
            menu.classList.remove('open');
            setTimeout(() => menu.classList.add('hidden'), 400);
        } else {
            menu.classList.remove('hidden');
            menu.offsetHeight;
            menu.classList.add('open');
        }
    });

    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('open');
            setTimeout(() => menu.classList.add('hidden'), 400);
        });
    });
}

/* ---- Scroll Reveal (Intersection Observer) ---- */
function initScrollReveal() {
    const elements = document.querySelectorAll('.scroll-reveal');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.08,
        rootMargin: '0px 0px -40px 0px'
    });

    elements.forEach(el => observer.observe(el));
}

/* ---- FAQ Accordion ---- */
function initFAQ() {
    const toggles = document.querySelectorAll('.faq-toggle');

    toggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const item = toggle.closest('.faq-item');
            const content = item.querySelector('.faq-content');
            const isActive = item.classList.contains('active');

            // Close all others
            document.querySelectorAll('.faq-item.active').forEach(activeItem => {
                if (activeItem !== item) {
                    activeItem.classList.remove('active');
                    const ac = activeItem.querySelector('.faq-content');
                    ac.classList.remove('show');
                    setTimeout(() => ac.classList.add('hidden'), 500);
                    activeItem.querySelector('.faq-toggle').setAttribute('aria-expanded', 'false');
                }
            });

            // Toggle current
            if (isActive) {
                item.classList.remove('active');
                content.classList.remove('show');
                setTimeout(() => content.classList.add('hidden'), 500);
                toggle.setAttribute('aria-expanded', 'false');
            } else {
                item.classList.add('active');
                content.classList.remove('hidden');
                content.offsetHeight;
                content.classList.add('show');
                toggle.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

/* ---- FISMATT Cloud / Portal de Familias tabs ---- */
function initCloudTabs() {
    const tabs = document.querySelectorAll('.cloud-tab');
    if (!tabs.length) return;

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = 'cloud-slide-' + tab.dataset.cloudTarget;

            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            document.querySelectorAll('.cloud-slide').forEach(slide => {
                slide.classList.toggle('hidden', slide.id !== targetId);
            });
        });
    });
}

/* ---- Smooth Scroll for Anchor Links ---- */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (!target) return;

            e.preventDefault();

            const navbarHeight = document.getElementById('navbar')?.offsetHeight || 64;
            const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight - 10;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        });
    });
}

/* ---- Active Navigation Link Highlight ---- */
function initActiveNavLinks() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!sections.length || !navLinks.length) return;

    let ticking = false;
    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(() => {
                const scrollPos = window.scrollY + 100;
                sections.forEach(section => {
                    const top = section.offsetTop;
                    const height = section.offsetHeight;
                    const id = section.getAttribute('id');
                    if (scrollPos >= top && scrollPos < top + height) {
                        navLinks.forEach(link => {
                            link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
                        });
                    }
                });
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}
