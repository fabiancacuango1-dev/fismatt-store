/* ============================================
   SoftPlugin Pro — Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMobileMenu();
    initScrollAnimations();
    initFAQ();
    initContactForm();
    initSmoothScroll();
    initActiveNavLinks();
});

/* ---- Navbar Scroll Effect ---- */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    function onScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
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
            menu.classList.add('hidden');
        } else {
            menu.classList.remove('hidden');
            // Force reflow for animation
            menu.offsetHeight;
            menu.classList.add('open');
        }
    });

    // Close menu on link click
    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('open');
            setTimeout(() => menu.classList.add('hidden'), 300);
        });
    });
}

/* ---- Scroll Animations (Intersection Observer) ---- */
function initScrollAnimations() {
    const elements = document.querySelectorAll('.scroll-animate');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger delay for siblings
                const delay = index * 100;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, Math.min(delay, 400));
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
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
                    const activeContent = activeItem.querySelector('.faq-content');
                    activeContent.classList.remove('show');
                    activeContent.classList.add('hidden');
                    activeItem.querySelector('.faq-toggle').setAttribute('aria-expanded', 'false');
                }
            });

            // Toggle current
            if (isActive) {
                item.classList.remove('active');
                content.classList.remove('show');
                setTimeout(() => content.classList.add('hidden'), 400);
                toggle.setAttribute('aria-expanded', 'false');
            } else {
                item.classList.add('active');
                content.classList.remove('hidden');
                // Force reflow
                content.offsetHeight;
                content.classList.add('show');
                toggle.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

/* ---- Contact Form (mailto fallback) ---- */
function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = sanitizeInput(form.querySelector('#name').value.trim());
        const email = sanitizeInput(form.querySelector('#email').value.trim());
        const message = sanitizeInput(form.querySelector('#message').value.trim());

        // Validation
        if (!name || !email || !message) {
            showFormStatus('Por favor, completa todos los campos.', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            showFormStatus('Por favor ingresa un correo electrónico válido.', 'error');
            return;
        }

        if (name.length > 100) {
            showFormStatus('El nombre es demasiado largo.', 'error');
            return;
        }

        if (message.length > 5000) {
            showFormStatus('El mensaje es demasiado largo.', 'error');
            return;
        }

        // Show loading
        const submitBtn = document.getElementById('submit-btn');
        const originalContent = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner"></span> Enviando...';
        submitBtn.disabled = true;

        // Build mailto link
        const subject = encodeURIComponent(`Consulta de ${name} — SoftPlugin Pro`);
        const body = encodeURIComponent(
            `Nombre: ${name}\nCorreo: ${email}\n\nMensaje:\n${message}`
        );
        const mailtoLink = `mailto:rectores_federal09@icloud.com?subject=${subject}&body=${body}`;

        // Simulate brief delay for UX
        setTimeout(() => {
            window.location.href = mailtoLink;

            // Reset form
            submitBtn.innerHTML = originalContent;
            submitBtn.disabled = false;
            form.reset();

            showFormStatus('¡Se abrió tu cliente de correo! Envía el mensaje para completar tu consulta.', 'success');
        }, 800);
    });
}

/* ---- Form Helpers ---- */
function sanitizeInput(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showFormStatus(message, type) {
    const statusEl = document.getElementById('form-status');
    if (!statusEl) return;

    statusEl.classList.remove('hidden');
    statusEl.className = `mt-4 p-4 rounded-xl text-sm font-medium ${
        type === 'success'
            ? 'bg-green-500/10 border border-green-500/20 text-green-400'
            : 'bg-red-500/10 border border-red-500/20 text-red-400'
    }`;
    statusEl.textContent = message;

    // Auto-hide after 6 seconds
    setTimeout(() => {
        statusEl.classList.add('hidden');
    }, 6000);
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

            const navbarHeight = document.getElementById('navbar')?.offsetHeight || 80;
            const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight;

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

    function onScroll() {
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}