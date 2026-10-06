/* FISMATT · SAI — la tienda: arma la cotización y el pedido.

   Todo ocurre en el navegador del visitante. No hay servidor: lo que escribe
   (nombre, institución) no se envía a ningún sitio hasta que él mismo pulsa
   «Enviar pedido por WhatsApp» o «Enviar por correo».

   Los precios NO están aquí: se leen de la propia página (data-precio), que
   sale de scripts/generar_sitio.py. Un solo lugar para cambiarlos. */
(function () {
    'use strict';

    var CLAVE = 'sai_cotizacion_v1';
    var WHATSAPP = '593983274499';
    var CORREO = 'rectores_federal09@icloud.com';

    var raiz = document.getElementById('tienda');
    if (!raiz) return;

    // ── Catálogo, leído del HTML ────────────────────────────────────────
    var planes = {};
    raiz.querySelectorAll('input[name="plan"]').forEach(function (r) {
        planes[r.value] = {
            nombre: r.dataset.nombre,
            precio: parseFloat(r.dataset.precio),
            periodo: r.dataset.periodo            // mes | año | único
        };
    });
    var articulos = {};
    raiz.querySelectorAll('[data-item]').forEach(function (el) {
        articulos[el.dataset.item] = {
            nombre: el.dataset.nombre,
            precio: parseFloat(el.dataset.precio),
            periodo: el.dataset.periodo,
            el: el
        };
    });

    // ── Estado ──────────────────────────────────────────────────────────
    var estado = { plan: 'anual', docentes: 1, items: {}, pago: 'Transferencia bancaria' };
    try {
        var g = JSON.parse(localStorage.getItem(CLAVE) || 'null');
        if (g && typeof g === 'object') {
            if (planes[g.plan]) estado.plan = g.plan;
            if (g.docentes >= 0) estado.docentes = Math.min(999, g.docentes | 0);
            for (var k in (g.items || {})) if (articulos[k]) estado.items[k] = Math.min(999, g.items[k] | 0);
            if (g.pago) estado.pago = String(g.pago);
        }
    } catch (e) { /* estado por defecto */ }

    // Quien llega desde un botón «Elegir anual» de la portada trae el plan en
    // la dirección (tienda.html?plan=anual).
    try {
        var pedido = new URLSearchParams(location.search).get('plan');
        if (pedido && planes[pedido]) { estado.plan = pedido; if (estado.docentes < 1) estado.docentes = 1; }
    } catch (e) { /* navegador sin URLSearchParams */ }

    function guardar() {
        try { localStorage.setItem(CLAVE, JSON.stringify(estado)); } catch (e) { /* modo privado */ }
    }

    // ── Dinero ──────────────────────────────────────────────────────────
    function usd(v) {
        var r = Math.round(v * 100) / 100;
        return '$' + (r % 1 === 0 ? String(r) : r.toFixed(2).replace('.', ','));
    }
    function sufijo(periodo) {
        return periodo === 'mes' ? ' al mes' : periodo === 'año' ? ' al año' : ' (pago único)';
    }

    // ── Cálculo ─────────────────────────────────────────────────────────
    function lineas() {
        var out = [];
        if (estado.docentes > 0) {
            var p = planes[estado.plan];
            out.push({
                cant: estado.docentes,
                nombre: 'Sistema Académico SAI — ' + p.nombre,
                unit: p.precio, periodo: p.periodo,
                total: p.precio * estado.docentes
            });
        }
        Object.keys(articulos).forEach(function (id) {
            var q = estado.items[id] | 0;
            if (q > 0) {
                var a = articulos[id];
                out.push({ cant: q, nombre: a.nombre, unit: a.precio, periodo: a.periodo, total: a.precio * q });
            }
        });
        return out;
    }
    function totales(ls) {
        var t = { hoy: 0, anual: 0, mensual: 0 };
        ls.forEach(function (l) {
            t.hoy += l.total;
            if (l.periodo === 'año') t.anual += l.total;
            if (l.periodo === 'mes') t.mensual += l.total;
        });
        return t;
    }

    // ── Texto del pedido ────────────────────────────────────────────────
    function cliente() {
        var v = function (id) { var e = document.getElementById(id); return e ? e.value.trim() : ''; };
        return { nombre: v('c-nombre'), institucion: v('c-institucion'), ciudad: v('c-ciudad') };
    }
    function textoPedido() {
        var ls = lineas(), t = totales(ls), c = cliente();
        var m = ['Hola, quiero hacer este pedido en FISMATT:', ''];
        ls.forEach(function (l) {
            m.push('• ' + l.cant + ' × ' + l.nombre + ': ' + usd(l.total) + sufijo(l.periodo));
        });
        m.push('', 'Total a pagar ahora: ' + usd(t.hoy) + ' USD', 'Forma de pago: ' + estado.pago);
        if (c.nombre || c.institucion || c.ciudad) {
            m.push('');
            if (c.nombre) m.push('Nombre: ' + c.nombre);
            if (c.institucion) m.push('Institución: ' + c.institucion);
            if (c.ciudad) m.push('Ciudad: ' + c.ciudad);
        }
        return m.join('\n');
    }

    // ── Pintar ──────────────────────────────────────────────────────────
    var elLineas = document.getElementById('r-lineas');
    var elVacio = document.getElementById('r-vacio');
    var elTotal = document.getElementById('r-total');
    var elRenueva = document.getElementById('r-renueva');
    var elInst = document.getElementById('r-institucion');
    var btnWa = document.getElementById('b-wa');
    var btnCorreo = document.getElementById('b-correo');
    var btnPdf = document.getElementById('b-pdf');
    var insignia = document.querySelector('.btn-carrito .n');

    function pintar() {
        // Controles
        var base = raiz.querySelector('[data-base]');
        base.querySelector('output').textContent = estado.docentes;
        base.classList.toggle('en', estado.docentes > 0);
        raiz.querySelectorAll('input[name="plan"]').forEach(function (r) { r.checked = (r.value === estado.plan); });
        Object.keys(articulos).forEach(function (id) {
            var q = estado.items[id] | 0;
            articulos[id].el.querySelector('output').textContent = q;
            articulos[id].el.classList.toggle('en', q > 0);
        });
        document.querySelectorAll('input[name="pago"]').forEach(function (r) { r.checked = (r.value === estado.pago); });

        // Resumen
        var ls = lineas(), t = totales(ls), vacio = ls.length === 0;
        elLineas.innerHTML = '';
        ls.forEach(function (l) {
            var li = document.createElement('li');
            var s = document.createElement('span');
            s.textContent = l.cant + ' × ' + l.nombre;
            var b = document.createElement('b');
            b.textContent = usd(l.total);
            li.appendChild(s); li.appendChild(b);
            elLineas.appendChild(li);
        });
        elVacio.hidden = !vacio;
        elTotal.textContent = usd(t.hoy);
        var t2 = document.getElementById('r-total-2');
        if (t2) t2.textContent = usd(t.hoy);

        var ren = [];
        if (t.anual > 0) ren.push(usd(t.anual) + ' al año');
        if (t.mensual > 0) ren.push(usd(t.mensual) + ' al mes');
        elRenueva.textContent = ren.length
            ? 'Después se renueva: ' + ren.join(' y ') + '.'
            : (vacio ? '' : 'Pago único: no se renueva.');
        elInst.hidden = estado.docentes < 5;

        var txt = encodeURIComponent(textoPedido());
        btnWa.href = 'https://wa.me/' + WHATSAPP + '?text=' + txt;
        btnCorreo.href = 'mailto:' + CORREO + '?subject=' + encodeURIComponent('Pedido FISMATT') + '&body=' + txt;
        [btnWa, btnCorreo, btnPdf].forEach(function (b) { b.setAttribute('aria-disabled', vacio ? 'true' : 'false'); });

        if (insignia) {
            var n = estado.docentes;
            for (var k in estado.items) n += estado.items[k] | 0;
            insignia.textContent = n > 0 ? n : '';
        }
        guardar();
    }

    // ── Eventos ─────────────────────────────────────────────────────────
    raiz.addEventListener('click', function (ev) {
        var b = ev.target.closest('button[data-paso]');
        if (!b) return;
        var paso = parseInt(b.dataset.paso, 10);
        var cont = b.closest('[data-base], [data-item]');
        if (cont.hasAttribute('data-base')) {
            estado.docentes = Math.max(0, Math.min(999, estado.docentes + paso));
        } else {
            var id = cont.dataset.item;
            estado.items[id] = Math.max(0, Math.min(999, (estado.items[id] | 0) + paso));
        }
        pintar();
    });
    raiz.addEventListener('change', function (ev) {
        if (ev.target.name === 'plan') { estado.plan = ev.target.value; if (estado.docentes === 0) estado.docentes = 1; pintar(); }
    });
    document.addEventListener('change', function (ev) {
        if (ev.target.name === 'pago') { estado.pago = ev.target.value; pintar(); }
    });
    ['c-nombre', 'c-institucion', 'c-ciudad'].forEach(function (id) {
        var e = document.getElementById(id);
        if (e) e.addEventListener('input', pintar);
    });

    // ── Cotización para imprimir o guardar como PDF ─────────────────────
    btnPdf.addEventListener('click', function (ev) {
        ev.preventDefault();
        var ls = lineas();
        if (!ls.length) return;
        var t = totales(ls), c = cliente(), d = new Date();
        var dos = function (x) { return (x < 10 ? '0' : '') + x; };
        var num = 'COT-' + d.getFullYear() + dos(d.getMonth() + 1) + dos(d.getDate()) + '-' + dos(d.getHours()) + dos(d.getMinutes());
        var fecha = d.toLocaleDateString('es-EC', { day: 'numeric', month: 'long', year: 'numeric' });
        var esc = function (s) { var x = document.createElement('i'); x.textContent = s; return x.innerHTML; };

        var filas = ls.map(function (l) {
            return '<tr><td>' + l.cant + '</td><td>' + esc(l.nombre) + '</td><td class="der">' + usd(l.unit) +
                   esc(sufijo(l.periodo)) + '</td><td class="der">' + usd(l.total) + '</td></tr>';
        }).join('');
        var ren = [];
        if (t.anual > 0) ren.push(usd(t.anual) + ' al año');
        if (t.mensual > 0) ren.push(usd(t.mensual) + ' al mes');

        document.getElementById('cotizacion').innerHTML =
            '<div class="mem"><div><h1>FISMATT</h1><div class="ch">Sistemas Educativos · fis-matt.com<br>WhatsApp +593 983 274 499</div></div>' +
            '<div class="ch" style="text-align:right"><b>Cotización ' + num + '</b><br>' + esc(fecha) + '<br>Válida por 15 días</div></div>' +
            (c.nombre || c.institucion || c.ciudad
                ? '<p class="ch"><b>Para:</b> ' + esc([c.nombre, c.institucion, c.ciudad].filter(Boolean).join(' · ')) + '</p>' : '') +
            '<table><thead><tr><th>Cant.</th><th>Descripción</th><th class="der">Precio</th><th class="der">Importe</th></tr></thead><tbody>' +
            filas + '<tr class="tot"><td colspan="3">Total a pagar ahora (USD)</td><td class="der">' + usd(t.hoy) + '</td></tr></tbody></table>' +
            (ren.length ? '<p class="ch">Renovación posterior: ' + ren.join(' y ') + '.</p>' : '') +
            '<p class="ch" style="margin-top:5mm"><b>Formas de pago:</b> transferencia bancaria, depósito o efectivo, tarjeta o PayPal. ' +
            'Al confirmar el pedido por WhatsApp le enviamos los datos para pagar; con el comprobante recibe su clave de licencia ' +
            'y la guía de instalación.</p>' +
            '<p class="ch">Precios individuales, por docente. Para instituciones preparamos una propuesta según el número de docentes.</p>';
        window.print();
    });

    pintar();
})();
