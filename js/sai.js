/* FISMATT · SAI — lo mínimo que comparten todas las páginas.
   La página se lee entera sin este archivo: aquí solo hay dos mejoras. */
(function () {
    'use strict';

    // 1. Cuántas cosas hay en la cotización, junto al botón de la cabecera.
    try {
        var c = JSON.parse(localStorage.getItem('sai_cotizacion_v1') || 'null');
        if (c) {
            var n = c.docentes | 0;
            for (var k in (c.items || {})) n += c.items[k] | 0;
            var el = document.querySelector('.btn-carrito .n');
            if (el && n > 0) el.textContent = n;
        }
    } catch (e) { /* sin almacenamiento: el botón sale sin número */ }

    // 2. El video de YouTube solo se pide cuando alguien lo quiere ver.
    document.querySelectorAll('.video[data-yt]').forEach(function (caja) {
        var boton = caja.querySelector('button');
        if (!boton) return;
        boton.addEventListener('click', function () {
            var f = document.createElement('iframe');
            f.src = 'https://www.youtube-nocookie.com/embed/' + caja.dataset.yt + '?autoplay=1&rel=0';
            f.title = caja.dataset.titulo || 'Video';
            f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
            f.allowFullscreen = true;
            caja.innerHTML = '';
            caja.appendChild(f);
        });
    });
})();
