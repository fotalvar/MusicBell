// ============= CONFIGURACIÓN GLOBAL =============

const API_URL = 'http://localhost:5000/api';

// Cache para reducir llamadas innecesarias
const cache = {
    archivos: null,
    archivosTiempo: 0,
    CACHE_DURACION: 30000 // 30 segundos
};

// Elementos del DOM - Cacheados para mejor rendimiento
const DOMElements = {
    formularioCancion: document.getElementById('formularioCancion'),
    selectArchivo: document.getElementById('archivo'),
    selectTipo: document.getElementById('tipo'),
    grupoFecha: document.getElementById('grupoFecha'),
    grupoDias: document.getElementById('grupoDias'),
    btnConflictos: document.getElementById('btnConflictos'),
    contenedorConflictos: document.getElementById('conflictosContent'),
    estadoContent: document.getElementById('estadoContent'),
    btnAbrirModalAgregarCancion: document.getElementById('btnAbrirModalAgregarCancion'),
    modalAgregarCancion: document.getElementById('modalAgregarCancion'),
    btnAbrirModalProgramacion: document.getElementById('btnAbrirModalProgramacion'),
    modalProgramacionRapida: document.getElementById('modalProgramacionRapida'),
    formularioProgramacionRapida: document.getElementById('formularioProgramacionRapida'),
    fechaInicio: document.getElementById('fechaInicio'),
    fechaFin: document.getElementById('fechaFin'),
    horaRapida: document.getElementById('horaRapida'),
    incluirFinSemana: document.getElementById('incluirFinSemana'),
    resumenProgramacion: document.getElementById('resumenProgramacion'),
    playlistContainer: document.getElementById('playlistContainer'),
    archivadoContainer: document.getElementById('archivadoContainer'),
    reproduccionContainer: document.getElementById('reproduccionContainer'),
    estadoRapido: document.getElementById('estadoRapido'),
    btnStop: document.getElementById('btnStop'),
    btnApagar: document.getElementById('btnApagar')
};

// Estado global
let canciones = [];
let archivosDisponibles = [];

// Intervalo de actualización
let updateInterval = null;

// ============= FUNCIONES AUXILIARES GENERALES =============

/**
 * Wrapper para fetch con manejo de errores mejorado
 */
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error en fetch a ${url}:`, error);
        throw error;
    }
}

/**
 * Debounce para funciones que se llaman frecuentemente
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

/**
 * Formatea bytes a formato legible
 */
function formatarTamaño(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Formatea fecha ISO a formato legible español
 */
function formatarFecha(fechaIso) {
    if (!fechaIso) return 'N/A';
    const fecha = new Date(fechaIso);
    return fecha.toLocaleString('es-ES');
}

/**
 * Obtiene el nombre del día de la semana
 */
function obtenerDiaSemana(fecha) {
    const diasSemana = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    const diaNumero = new Date(fecha + 'T00:00:00').getDay();
    return diasSemana[diaNumero];
}

/**
 * Obtiene fecha y hora actual formateadas
 */
function obtenerFechaHoraActual() {
    const ahora = new Date();
    return {
        fecha: ahora.toISOString().split('T')[0],
        hora: ahora.getHours().toString().padStart(2, '0') + ':' + 
              ahora.getMinutes().toString().padStart(2, '0')
    };
}

// ============= FUNCIONES INICIALES =============

document.addEventListener('DOMContentLoaded', () => {
    inicializarAplicacion();
    inicializarEventListeners();
});

function inicializarAplicacion() {
    cargarArchivos();
    cargarCanciones();
    cargarEstado();
    actualizarEstadoRapido();
    
    // Reducido de 5 segundos a 10 segundos para mejor rendimiento
    updateInterval = setInterval(() => {
        cargarEstado();
        cargarCanciones();
        actualizarEstadoRapido();
    }, 10000);
}

function inicializarEventListeners() {
    // Formulario de canción
    DOMElements.formularioCancion?.addEventListener('submit', manejarFormularioCancion);
    DOMElements.selectTipo?.addEventListener('change', cambiarTipo);
    
    // Modales
    DOMElements.btnAbrirModalAgregarCancion?.addEventListener('click', abrirModalAgregarCancion);
    DOMElements.btnAbrirModalProgramacion?.addEventListener('click', abrirModalProgramacionRapida);
    
    // Eventos de programación rápida
    [DOMElements.fechaInicio, DOMElements.fechaFin, DOMElements.incluirFinSemana].forEach(el => {
        el?.addEventListener('change', debounce(actualizarResumenProgramacion, 300));
    });
    
    // Cerrar modal al hacer clic fuera
    DOMElements.modalProgramacionRapida?.addEventListener('click', (e) => {
        if (e.target === DOMElements.modalProgramacionRapida) {
            cerrarModalProgramacion();
        }
    });
    
    // Botones de control
    DOMElements.btnStop?.addEventListener('click', detenerCancion);
    DOMElements.btnApagar?.addEventListener('click', apagarAplicacion);
    DOMElements.btnConflictos?.addEventListener('click', detectarConflictos);
}

// ============= NAVEGACIÓN DE TABS =============

function cambiarTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('activo'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('activo'));
    
    const tabActivo = document.getElementById(`tab-${tabName}`);
    if (tabActivo) tabActivo.classList.add('activo');
    
    const btnActivo = document.querySelector(`[onclick="cambiarTab('${tabName}')"]`);
    if (btnActivo) btnActivo.classList.add('activo');
}

// ============= CARGA DE DATOS =============

async function cargarArchivos() {
    try {
        // Usar cache si está disponible y no ha expirado
        const ahora = Date.now();
        if (cache.archivos && (ahora - cache.archivosTiempo) < cache.CACHE_DURACION) {
            return cache.archivos;
        }
        
        const archivos = await fetchAPI(`${API_URL}/archivos`);
        cache.archivos = archivos;
        cache.archivosTiempo = ahora;
        return archivos;
    } catch (error) {
        console.error('Error cargando archivos:', error);
        return [];
    }
}

async function cargarCanciones() {
    try {
        const data = await fetchAPI(`${API_URL}/canciones`);
        canciones = Array.isArray(data) ? data : [];
        mostrarCanciones();
    } catch (error) {
        console.error('Error cargando canciones:', error);
    }
}

async function cargarEstado() {
    try {
        const estado = await fetchAPI(`${API_URL}/estado`);
        mostrarEstado(estado);
    } catch (error) {
        console.error('Error cargando estado:', error);
    }
}

// ============= MOSTRAR DATOS =============

function mostrarCanciones() {
    const playlistCanciones = canciones.filter(c => !c.archivado);
    const archivadoCanciones = canciones.filter(c => c.archivado);
    const { fecha: fechaActual, hora: horaActual } = obtenerFechaHoraActual();
    
    // Archivar automáticamente canciones pasadas
    archivarCancionesPasadas(playlistCanciones, archivadoCanciones, fechaActual, horaActual);
    
    mostrarPlaylist(playlistCanciones);
    mostrarArchivado(archivadoCanciones);
    cargarCancionesDisponibles();
}

function archivarCancionesPasadas(playlistCanciones, archivadoCanciones, fechaActual, horaActual) {
    for (let cancion of playlistCanciones) {
        let debeMover = false;
        
        if (cancion.fecha && cancion.hora) {
            debeMover = cancion.fecha < fechaActual || 
                       (cancion.fecha === fechaActual && cancion.hora < horaActual);
        } else if (cancion.fecha && !cancion.hora) {
            debeMover = cancion.fecha < fechaActual;
        }
        
        if (debeMover && !cancion.archivado) {
            actualizarCancion(cancion.id, { archivado: true });
            cancion.archivado = true;
            archivadoCanciones.push(cancion);
        }
    }
}

function mostrarPlaylist(playlistFinal) {
    const container = DOMElements.playlistContainer;
    if (!container) return;
    
    if (playlistFinal.length === 0) {
        container.innerHTML = '<p class="vacio">No hay canciones en la playlist. Añade una nueva.</p>';
        return;
    }
    
    const ordenadas = playlistFinal.sort((a, b) => {
        const dateA = new Date(`${a.fecha || '2099-12-31'}T${a.hora || '23:59'}`);
        const dateB = new Date(`${b.fecha || '2099-12-31'}T${b.hora || '23:59'}`);
        return dateA - dateB;
    });
    
    let html = '<table class="playlist-table"><thead><tr><th>Canción</th><th>Duración</th><th>Fecha</th><th>Hora</th><th>Día</th><th>Acciones</th></tr></thead><tbody>';
    
    ordenadas.forEach(cancion => {
        const diaNombre = cancion.fecha ? obtenerDiaSemana(cancion.fecha) : obtenerDiaSemana(new Date().toISOString().split('T')[0]);
        html += `<tr id="cancion-${cancion.id}">
                    <td>${cancion.nombre || cancion.archivo}</td>
                    <td class="duracion-cell">${cancion.duracion || 'N/A'}</td>
                    <td><input type="date" value="${cancion.fecha || ''}" class="tabla-input" onchange="editarCancionRapida(${cancion.id}, 'fecha', this.value)"></td>
                    <td><input type="time" value="${cancion.hora || ''}" class="tabla-input" onchange="editarCancionRapida(${cancion.id}, 'hora', this.value)"></td>
                    <td class="dia-semana-cell">${diaNombre}</td>
                    <td class="tabla-acciones"><button class="btn-eliminar" onclick="eliminarCancion(${cancion.id})">🗑️ Eliminar</button></td>
                 </tr>`;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

function mostrarArchivado(archivadoCanciones) {
    const container = DOMElements.archivadoContainer;
    if (!container) return;
    
    if (archivadoCanciones.length === 0) {
        container.innerHTML = '<p class="vacio">No hay canciones archivadas</p>';
        return;
    }
    
    let html = '<table class="archivado-table"><thead><tr><th>Canción</th><th>Duración</th><th>Fecha</th><th>Hora</th><th>Acciones</th></tr></thead><tbody>';
    
    archivadoCanciones.forEach(cancion => {
        html += `<tr id="cancion-${cancion.id}">
                    <td>${cancion.nombre || cancion.archivo}</td>
                    <td class="duracion-cell">${cancion.duracion || 'N/A'}</td>
                    <td>${cancion.fecha || 'N/A'}</td>
                    <td>${cancion.hora || 'N/A'}</td>
                    <td class="tabla-acciones"><button class="btn-eliminar" onclick="eliminarCancion(${cancion.id})">🗑️ Eliminar</button></td>
                 </tr>`;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

function mostrarEstado(estado) {
    const container = DOMElements.estadoContent;
    if (!container) return;
    
    if (!estado || Object.keys(estado).length === 0) {
        container.innerHTML = '<p class="vacio">Sin información de estado</p>';
        container.classList.add('vacio');
        return;
    }
    
    container.classList.remove('vacio');
    container.innerHTML = `
        <div class="estado-item"><span class="estado-label">Reproduciendo:</span> ${estado.reproduciendo ? 'Sí' : 'No'}</div>
        <div class="estado-item"><span class="estado-label">Canción actual:</span> ${estado.cancion_actual || 'Ninguna'}</div>
        <div class="estado-item"><span class="estado-label">Última actualización:</span> ${formatarFecha(estado.fecha_ultima_actualizacion)}</div>
    `;
}

// ============= FORMULARIO =============

function cambiarTipo() {
    const tipo = DOMElements.selectTipo.value;
    const mostrarFecha = tipo === 'fecha';
    const mostrarDias = tipo === 'dia_semana';
    
    DOMElements.grupoFecha.style.display = mostrarFecha ? 'block' : 'none';
    DOMElements.grupoDias.style.display = mostrarDias ? 'block' : 'none';
}

async function manejarFormularioCancion(e) {
    e.preventDefault();
    
    const tipo = DOMElements.selectTipo.value;
    const dias = Array.from(document.querySelectorAll('input[name="dia"]:checked')).map(cb => cb.value);
    
    const datosCancion = {
        nombre: document.getElementById('nombre').value,
        archivo: DOMElements.selectArchivo.value,
        tipo_planificacion: tipo,
        hora: document.getElementById('hora').value,
        ...(tipo === 'fecha' && { fecha: document.getElementById('fecha').value }),
        ...(tipo === 'dia_semana' && { dias: dias })
    };
    
    try {
        await fetchAPI(`${API_URL}/canciones`, {
            method: 'POST',
            body: JSON.stringify(datosCancion)
        });
        
        DOMElements.formularioCancion.reset();
        DOMElements.grupoFecha.style.display = 'none';
        DOMElements.grupoDias.style.display = 'none';
        cerrarModalAgregarCancion();
        cargarCanciones();
    } catch (error) {
        alert('Error al añadir canción');
    }
}

// ============= OPERACIONES CRUD =============

async function editarCancionRapida(id, campo, valor) {
    try {
        await actualizarCancion(id, { [campo]: valor });
        
        const row = document.getElementById(`cancion-${id}`);
        if (row) {
            row.style.backgroundColor = '#c8e6c9';
            setTimeout(() => { row.style.backgroundColor = 'white'; }, 500);
        }
        cargarCanciones();
    } catch (error) {
        console.error('Error editando:', error);
    }
}

async function actualizarCancion(id, datos) {
    return fetchAPI(`${API_URL}/canciones/${id}`, {
        method: 'PUT',
        body: JSON.stringify(datos)
    });
}

async function eliminarCancion(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta canción?')) return;
    
    try {
        await fetchAPI(`${API_URL}/canciones/${id}`, { method: 'DELETE' });
        cargarCanciones();
    } catch (error) {
        alert('Error al eliminar la canción');
    }
}

// ============= CONFLICTOS =============

async function detectarConflictos() {
    try {
        const data = await fetchAPI(`${API_URL}/detectar-conflictos`);
        
        if (data.conflictos && Object.keys(data.conflictos).length > 0) {
            let html = '';
            for (const [hora, conflictoCanciones] of Object.entries(data.conflictos)) {
                html += `<div class="conflicto-item">
                    <div class="conflicto-hora">🕐 ${hora}</div>
                    <ul class="conflicto-lista">${conflictoCanciones.map(c => `<li>${c}</li>`).join('')}</ul>
                </div>`;
            }
            DOMElements.contenedorConflictos.innerHTML = html;
        } else {
            DOMElements.contenedorConflictos.innerHTML = '<div class="sin-conflictos">No hay conflictos de horario</div>';
        }
    } catch (error) {
        console.error('Error detectando conflictos:', error);
        DOMElements.contenedorConflictos.innerHTML = '<p>Error al verificar conflictos</p>';
    }
}

// ============= MODAL AGREGAR CANCIÓN =============

async function abrirModalAgregarCancion() {
    try {
        const archivos = await cargarArchivos();
        DOMElements.selectArchivo.innerHTML = '<option value="">-- Selecciona un archivo --</option>';
        archivos.forEach(archivo => {
            const option = document.createElement('option');
            option.value = archivo.nombre;
            option.textContent = `${archivo.nombre} (${formatarTamaño(archivo.tamaño)})`;
            DOMElements.selectArchivo.appendChild(option);
        });
    } catch (error) {
        console.error('Error cargando archivos:', error);
    }
    
    DOMElements.formularioCancion.reset();
    DOMElements.grupoFecha.style.display = 'none';
    DOMElements.grupoDias.style.display = 'none';
    DOMElements.modalAgregarCancion.classList.add('activo');
}

function cerrarModalAgregarCancion() {
    DOMElements.modalAgregarCancion.classList.remove('activo');
    DOMElements.formularioCancion.reset();
    DOMElements.grupoFecha.style.display = 'none';
    DOMElements.grupoDias.style.display = 'none';
}

// ============= PROGRAMACIÓN RÁPIDA =============

async function abrirModalProgramacionRapida() {
    try {
        const archivos = await cargarArchivos();
        archivosDisponibles = archivos;
    } catch (error) {
        console.error('Error cargando archivos:', error);
        archivosDisponibles = [];
    }
    
    const hoy = new Date();
    const manana = new Date(hoy);
    manana.setDate(manana.getDate() + 7);
    
    const formatoFecha = (fecha) => fecha.toISOString().split('T')[0];
    
    DOMElements.fechaInicio.value = formatoFecha(hoy);
    DOMElements.fechaFin.value = formatoFecha(manana);
    DOMElements.horaRapida.value = '08:00';
    
    DOMElements.modalProgramacionRapida.classList.add('activo');
    actualizarResumenProgramacion();
}

function cerrarModalProgramacion() {
    DOMElements.modalProgramacionRapida.classList.remove('activo');
}

function actualizarResumenProgramacion() {
    if (!DOMElements.fechaInicio.value || !DOMElements.fechaFin.value) return;
    
    const inicio = new Date(DOMElements.fechaInicio.value);
    const fin = new Date(DOMElements.fechaFin.value);
    
    if (inicio > fin) {
        DOMElements.resumenProgramacion.textContent = 'La fecha de inicio es posterior a la fecha de fin';
        return;
    }
    
    const diasLaborales = calcularDiasLaborales(inicio, fin, DOMElements.incluirFinSemana.checked);
    const totalArchivos = archivosDisponibles.length;
    
    let resumen = `${diasLaborales} día(s)`;
    if (totalArchivos > 0) {
        resumen += ` × ${totalArchivos} archivo(s)`;
        if (diasLaborales > totalArchivos) {
            resumen += ` (se reciclará desde el inicio)`;
        }
        const listaArchivos = archivosDisponibles.map(a => `• ${a.nombre}`).join('\n');
        resumen += `\n\nArchivos disponibles:\n${listaArchivos}`;
    } else {
        resumen += ` (Sin archivos MP3 disponibles)`;
    }
    
    DOMElements.resumenProgramacion.textContent = resumen;
}

function calcularDiasLaborales(inicio, fin, incluirFinSemana) {
    let contador = 0;
    const fecha = new Date(inicio);
    
    while (fecha <= fin) {
        const diaSemana = fecha.getDay();
        const esFinSemana = diaSemana === 0 || diaSemana === 6;
        
        if (incluirFinSemana || !esFinSemana) {
            contador++;
        }
        
        fecha.setDate(fecha.getDate() + 1);
    }
    
    return contador;
}

DOMElements.formularioProgramacionRapida?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!DOMElements.fechaInicio.value || !DOMElements.fechaFin.value || !DOMElements.horaRapida.value) {
        alert('Por favor, rellena todos los campos');
        return;
    }
    
    if (archivosDisponibles.length === 0) {
        alert('No hay archivos MP3 disponibles para programar');
        return;
    }
    
    const inicio = new Date(DOMElements.fechaInicio.value);
    const fin = new Date(DOMElements.fechaFin.value);
    
    if (inicio > fin) {
        alert('La fecha de inicio no puede ser posterior a la fecha de fin');
        return;
    }
    
    const nuevasCanciones = [];
    let indiceArchivo = 0;
    const fecha = new Date(inicio);
    
    while (fecha <= fin) {
        const diaSemana = fecha.getDay();
        const esFinSemana = diaSemana === 0 || diaSemana === 6;
        
        if (DOMElements.incluirFinSemana.checked || !esFinSemana) {
            const archivo = archivosDisponibles[indiceArchivo % archivosDisponibles.length];
            const fechaFormato = fecha.toISOString().split('T')[0];
            const nombreArchivo = archivo.nombre.replace(/\.(mp3|MP3)$/, '');
            
            nuevasCanciones.push({
                nombre: `${nombreArchivo} (${fechaFormato})`,
                archivo: archivo.nombre,
                tipo_planificacion: 'fecha',
                fecha: fechaFormato,
                hora: DOMElements.horaRapida.value,
                habilitada: true
            });
            
            indiceArchivo++;
        }
        
        fecha.setDate(fecha.getDate() + 1);
    }
    
    let agregadas = 0;
    for (const cancion of nuevasCanciones) {
        try {
            await fetchAPI(`${API_URL}/canciones`, {
                method: 'POST',
                body: JSON.stringify(cancion)
            });
            agregadas++;
        } catch (error) {
            console.error('Error agregando canción:', error);
        }
    }
    
    if (agregadas > 0) {
        alert(`${agregadas} canción(es) programada(s) exitosamente`);
        DOMElements.formularioProgramacionRapida.reset();
        cerrarModalProgramacion();
        cargarCanciones();
    } else {
        alert('Error al programar las canciones');
    }
});

// ============= FUNCIONES DE CONTROL =============

async function detenerCancion() {
    try {
        await fetchAPI(`${API_URL}/detener`, { method: 'POST' });
        actualizarEstadoRapido();
        alert('Canción detenida');
    } catch (error) {
        alert('Error al detener la canción');
    }
}

async function apagarAplicacion() {
    if (!confirm('¿Estás seguro de que quieres apagar la aplicación completamente?')) return;
    
    try {
        await fetchAPI(`${API_URL}/apagar`, { method: 'POST' });
        alert('Aplicación apagada');
        document.body.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100vh; font-size: 24px; text-align: center;"><div><h1>MusicBell</h1><p>La aplicación ha sido apagada correctamente.</p></div></div>';
    } catch (error) {
        alert('Error al apagar la aplicación');
    }
}

async function actualizarEstadoRapido() {
    try {
        const estado = await fetchAPI(`${API_URL}/estado`);
        const elemento = DOMElements.estadoRapido;
        if (elemento) {
            elemento.textContent = estado.reproduciendo && estado.cancion_actual 
                ? `Reproduciendo: ${estado.cancion_actual}` 
                : 'Estado: Sin reproducción';
        }
    } catch (error) {
        console.error('Error actualizando estado rápido:', error);
    }
}

// ============= REPRODUCCIÓN RÁPIDA =============

async function cargarCancionesDisponibles() {
    try {
        const archivos = await cargarArchivos();
        const container = DOMElements.reproduccionContainer;
        
        if (!container) return;
        
        if (archivos.length === 0) {
            container.innerHTML = '<p class="vacio">No hay canciones disponibles en la carpeta Canciones</p>';
            return;
        }
        
        archivos.sort((a, b) => a.nombre.localeCompare(b.nombre));
        
        let html = '<table class="reproduccion-table"><thead><tr><th>Canción</th><th>Tamaño</th><th>Acción</th></tr></thead><tbody>';
        archivos.forEach(archivo => {
            html += `<tr><td>${archivo.nombre}</td><td class="tamaño-cell">${formatarTamaño(archivo.tamaño)}</td>
                    <td class="tabla-acciones"><button class="btn-play" onclick="reproducirCancionRapida('${archivo.nombre.replace(/'/g, "\\'")}')">Reproducir</button></td></tr>`;
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (error) {
        console.error('Error cargando canciones disponibles:', error);
        if (DOMElements.reproduccionContainer) {
            DOMElements.reproduccionContainer.innerHTML = '<p class="error">Error al cargar las canciones</p>';
        }
    }
}

async function reproducirCancionRapida(nombreArchivo) {
    try {
        const data = await fetchAPI(`${API_URL}/reproducir/${encodeURIComponent(nombreArchivo)}`, {
            method: 'POST'
        });
        
        actualizarEstadoRapido();
        alert(`${data.mensaje}\n${data.cancion}`);
    } catch (error) {
        alert('Error al reproducir la canción');
    }
}


