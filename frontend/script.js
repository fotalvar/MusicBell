const getAPIUrl = () => {
  const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  const port = window.location.port;
  return `${protocol}//${hostname}${port ? ":" + port : ""}/api`;
};
const API_URL = getAPIUrl();
const cache = { archivos: null, archivosTiempo: 0, CACHE_DURACION: 30000 };
let canciones = [];
let archivosDisponibles = [];
let estadoPanel = "abierto";
let updateInterval = null;
async function fetchAPI(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
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
function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}
function formatarTamaño(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}
function formatarFecha(fechaIso) {
  if (!fechaIso) return "N/A";
  const fecha = new Date(fechaIso);
  const dia = String(fecha.getDate()).padStart(2, "0");
  const mes = String(fecha.getMonth() + 1).padStart(2, "0");
  const año = fecha.getFullYear();
  return `${dia}/${mes}/${año}`;
}
function obtenerNombreDia(fecha) {
  const dias = [
    "domingo",
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
  ];
  return dias[fecha.getDay()];
}
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM cargado");
  inicializar();
});
async function inicializar() {
  console.log("Inicializando aplicación...");
  conectarEventos();
  inicializarPanelEstado();
  await cargarArchivos();
  await cargarCanciones();
  await cargarEstado();
  await obtenerDatosRemoto();
  actualizarSubbarra("canciones");
  updateInterval = setInterval(async () => {
    await cargarEstado();
  }, 2000);
}
function conectarEventos() {
  document.querySelectorAll(".nav-option").forEach((btn) => {
    btn.addEventListener("click", function () {
      const tab = this.dataset.tab;
      cambiarTab(tab);
    });
  });
  const formularioCancion = document.getElementById("formularioCancion");
  if (formularioCancion) {
    formularioCancion.addEventListener("submit", agregarCancion);
  }
  const formularioProgramacion = document.getElementById(
    "formularioProgramacionRapida",
  );
  if (formularioProgramacion) {
    formularioProgramacion.addEventListener(
      "submit",
      generarProgramacionRapida,
    );
  }
  const uploadArea = document.getElementById("uploadArea");
  if (uploadArea) {
    uploadArea.addEventListener("click", () => {
      document.getElementById("fileInput").click();
    });
  }
  const btnAbrirModal = document.getElementById("btnAbrirModalAgregarCancion");
  if (btnAbrirModal) {
    btnAbrirModal.addEventListener("click", abrirModalAgregarCancion);
  }
  const btnProgramacion = document.getElementById("btnAbrirModalProgramacion");
  if (btnProgramacion) {
    btnProgramacion.addEventListener("click", abrirModalProgramacion);
  }
  const fechaInicio = document.getElementById("fechaInicio");
  const fechaFin = document.getElementById("fechaFin");
  if (fechaInicio && fechaFin) {
    fechaInicio.addEventListener("change", actualizarResumenProgramacion);
    fechaFin.addEventListener("change", actualizarResumenProgramacion);
    document
      .getElementById("incluirFinSemana")
      .addEventListener("change", actualizarResumenProgramacion);
  }
}
function inicializarPanelEstado() {
  // Cerrar el panel si se hace clic fuera de él
  document.addEventListener("click", (e) => {
    const panel = document.getElementById("panelEstado");
    const btnEstado = document.getElementById("btnEstado");

    if (!panel.contains(e.target) && !btnEstado.contains(e.target)) {
      panel.classList.remove("mostrado");
    }
  });
}
function cambiarTab(tabName) {
  console.log("Cambiando a pestaña:", tabName);
  document.querySelectorAll(".tab-pane").forEach((tab) => {
    tab.classList.remove("activo");
  });
  const tabElement = document.getElementById(`tab-${tabName}`);
  if (tabElement) {
    tabElement.classList.add("activo");
  }
  document.querySelectorAll(".nav-option").forEach((btn) => {
    btn.classList.remove("activo");
  });
  const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
  if (activeBtn) {
    activeBtn.classList.add("activo");
  }
  actualizarSubbarra(tabName);
}
function actualizarSubbarra(tab) {
  const subbarraContent = document.getElementById("subbarraAcciones");
  let html = "";
  if (tab === "canciones") {
    html = `
            <button id="btnAbrirModalAgregarCancion" class="btn-agregar">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                Añadir Canción
            </button>
            <button id="btnAbrirModalProgramacion" class="btn-programacion-rapida">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 3h-2v10h2V3zm4.83 2.17l-1.41 1.41C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z"/></svg>
                Programación Rápida
            </button>
            <button id="btnAbrirModalCarga" class="btn-agregar">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                Cargar Música
            </button>
        `;
  } else if (tab === "reproduccion") {
    html = `<p style="margin: 0; color: #666; font-size: 0.9em;">Selecciona una canción para reproducir</p>`;
  } else if (tab === "conflictos") {
    html = `<p style="margin: 0; color: #666; font-size: 0.9em;">Verifica los conflictos de horario</p>`;
  }
  subbarraContent.innerHTML = html;
  if (tab === "canciones") {
    document
      .getElementById("btnAbrirModalAgregarCancion")
      .addEventListener("click", abrirModalAgregarCancion);
    document
      .getElementById("btnAbrirModalProgramacion")
      .addEventListener("click", abrirModalProgramacion);
    document
      .getElementById("btnAbrirModalCarga")
      .addEventListener("click", abrirModalCargaRemota);
  }
}
async function cargarArchivos() {
  try {
    const response = await fetchAPI(`${API_URL}/archivos`);
    archivosDisponibles = response;
    const selectArchivo = document.getElementById("archivo");
    if (selectArchivo) {
      selectArchivo.innerHTML =
        '<option value="">-- Selecciona un archivo --</option>';
      response.forEach((archivo) => {
        const option = document.createElement("option");
        option.value = archivo.nombre;
        option.textContent = `${archivo.nombre} (${formatarTamaño(archivo.tamaño)})`;
        selectArchivo.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Error cargando archivos:", error);
  }
}
async function cargarCanciones() {
  try {
    const response = await fetchAPI(`${API_URL}/canciones`);
    canciones = response;
    renderizarPlaylist();
    actualizarPlayerWidget();
  } catch (error) {
    console.error("Error cargando canciones:", error);
  }
}
async function cargarEstado() {
  try {
    const response = await fetchAPI(`${API_URL}/estado`);
    console.log("Respuesta de estado:", response);
    const cancionActual = (response.cancion_actual || "").trim();
    console.log("Canción actual obtenida:", cancionActual);
    actualizarPlayerWidget(cancionActual);
  } catch (error) {
    console.error("Error cargando estado:", error);
  }
}
function actualizarPlayerWidget(cancionActual) {
  const playerContent = document.getElementById("playerContent");
  if (!playerContent) return;

  // Si no se proporciona cancionActual, dejarlo vacío/parado
  if (cancionActual === undefined) {
    cancionActual = "";
  } else {
    cancionActual = (cancionActual || "").trim();
  }

  console.log("Actualizando widget con cancionActual:", cancionActual);

  if (cancionActual && cancionActual.length > 0) {
    // Canción reproduciéndose
    playerContent.innerHTML = `
      <div class="player-playing">
        <div class="player-song-name">▶ ${cancionActual}</div>
        <button class="btn-player-stop" onclick="detenerCancion()">STOP</button>
      </div>
    `;
  } else {
    // No hay canción reproduciéndose - mostrar próxima programada con botón STOP
    const proximaCancion = obtenerProximaCancionProgramada();
    if (proximaCancion) {
      const fechaFormato = formatarFecha(proximaCancion.fecha);
      playerContent.innerHTML = `
        <div class="player-content-wrapper">
          <div class="player-info">
            <p style="font-size: 0.65em; color: #fff; margin: 0 0 6px 0;">Próxima canción programada: <strong>${fechaFormato}</strong></p>
            <p style="font-size: 1em; font-weight: bold; margin: 0;">${proximaCancion.nombre}</p>
          </div>
        </div>
        <button class="btn-player-stop" onclick="detenerCancion()">STOP</button>
      `;
    } else {
      playerContent.innerHTML = `
        <div class="player-content-wrapper">
          <div class="player-info">
            <p style="font-size: 0.85em; margin: 0;">Próxima canción programada: Ninguna</p>
          </div>
        </div>
        <button class="btn-player-stop" onclick="detenerCancion()">STOP</button>
      `;
    }
  }
}

function obtenerProximaCancionProgramada() {
  if (!canciones || canciones.length === 0) return null;

  // Filtrar canciones que aún no han sonado
  const proximasCanciones = canciones.filter((c) => {
    if (!c.fecha) return false;
    const fechaCancion = new Date(c.fecha);
    const ahora = new Date();
    return fechaCancion >= ahora;
  });

  // Ordenar por fecha
  proximasCanciones.sort((a, b) => {
    const fechaA = new Date(a.fecha);
    const fechaB = new Date(b.fecha);
    return fechaA - fechaB;
  });

  if (proximasCanciones.length > 0) {
    const proximaCancion = proximasCanciones[0];
    return {
      nombre: proximaCancion.archivo.replace(/\.mp3$/i, ""),
      fecha: proximaCancion.fecha,
    };
  }
  return null;
}
async function obtenerDatosRemoto() {
  try {
    const response = await fetchAPI(`${API_URL}/datos-remoto`);
    document.getElementById("estadoIP").textContent =
      response.ip || "Desconocida";
    document.getElementById("estadoPuerto").textContent =
      response.puerto || "5000";
    document.getElementById("estadoRemoto").textContent =
      `${response.ip}:${response.puerto}` || "-";
  } catch (error) {
    console.error("Error obteniendo datos remoto:", error);
    document.getElementById("estadoIP").textContent = "localhost";
    document.getElementById("estadoPuerto").textContent = "5000";
  }
}
function renderizarPlaylist() {
  const container = document.getElementById("playlistContainer");
  if (!container) return;
  const cancionesActivas = canciones;
  if (cancionesActivas.length === 0) {
    container.innerHTML = "<p>No hay canciones en la playlist</p>";
    return;
  }
  // Ordenar cronológicamente (por hora si existe, sino por nombre)
  // Ordenar por fecha creciente
  cancionesActivas.sort((a, b) => {
    const fechaA = a.fecha ? new Date(a.fecha) : new Date("2099-12-31");
    const fechaB = b.fecha ? new Date(b.fecha) : new Date("2099-12-31");
    return fechaA - fechaB;
  });
  const html = `
    <table class="tabla-playlist">
      <thead>
        <tr>
          <th>Tarea</th>
          <th>Fecha</th>
          <th>Hora</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        ${cancionesActivas
          .map((cancion) => {
            const nombreArchivo = cancion.archivo.replace(/\.mp3$/i, "");
            const fechaObj = cancion.fecha ? new Date(cancion.fecha) : null;
            const ahora = new Date();

            // Comparar fecha + hora
            let yaReproducida = false;
            if (fechaObj && cancion.hora) {
              try {
                const [horas, minutos] = cancion.hora.split(":");
                if (horas !== undefined && minutos !== undefined) {
                  const horasNum = parseInt(horas);
                  const minutosNum = parseInt(minutos);
                  if (!isNaN(horasNum) && !isNaN(minutosNum)) {
                    fechaObj.setHours(horasNum, minutosNum, 0, 0);
                    yaReproducida = fechaObj < ahora;
                  }
                }
              } catch (e) {
                console.error("Error procesando hora:", cancion.hora, e);
              }
            } else if (fechaObj) {
              yaReproducida = fechaObj < ahora;
            }

            return `
          <tr class="fila-cancion ${yaReproducida ? "fila-reproducida" : ""}" data-id="${cancion.id}">
            <td class="celda-nombre"><span>${nombreArchivo}</span></td>
            <td class="celda-fecha" ondblclick="editarCelda(this, 'fecha', ${cancion.id})"><span>${cancion.fecha ? formatarFecha(cancion.fecha) : "-"}</span></td>
            <td class="celda-hora" ondblclick="editarCelda(this, 'hora', ${cancion.id})"><span>${cancion.hora || "-"}</span></td>
            <td class="celda-acciones">
              <button onclick="eliminarCancion(${cancion.id})" class="btn-tabla btn-eliminar" title="Eliminar">🗑️</button>
            </td>
          </tr>
        `;
          })
          .join("")}
      </tbody>
    </table>
  `;
  container.innerHTML = html;
  agregarEstilosTabla();
}
function renderizarReproduccion() {
  const container = document.getElementById("reproduccionContainer");
  if (!container || !archivosDisponibles) return;
  if (archivosDisponibles.length === 0) {
    container.innerHTML = "<p>No hay canciones disponibles";
    return;
  }
  container.innerHTML = archivosDisponibles
    .map(
      (archivo) => `
        <div class="cancion-card">
            <h4>${archivo.nombre}</h4>
            <p><strong>Tamaño:</strong> ${formatarTamaño(archivo.tamaño)}</p>
            <button onclick="reproducirCancion('${archivo.nombre}')" class="btn-reproducir">
                ▶ Reproducir
            </button>
        </div>
    `,
    )
    .join("");
  agregarEstilosCancionCard();
}
function renderizarArchivadas() {
  // Función eliminada - no se usa archivado
}
function agregarEstilosTabla() {
  if (!document.getElementById("tabla-styles")) {
    const style = document.createElement("style");
    style.id = "tabla-styles";
    style.textContent = `
      .tabla-playlist {
        width: 100%;
        border-collapse: collapse;
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-radius: 8px;
        overflow: hidden;
        font-size: 0.9em;
        table-layout: fixed;
      }
      .tabla-playlist thead {
        background: linear-gradient(135deg, #5b6dff 0%, #7c3aed 100%);
        color: var(--white);
        font-weight: 600;
      }
      .tabla-playlist th {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 2px solid var(--gray-200);
      }
      .tabla-playlist tbody tr {
        border-bottom: 1px solid var(--gray-200);
        transition: all 0.2s ease;
      }
      .tabla-playlist tbody tr:hover {
        background-color: #f8f9fa;
      }
      .tabla-playlist td {
        padding: 12px 15px;
      }
      .celda-nombre, .celda-hora, .celda-fecha {
        cursor: pointer;
        position: relative;
      }
      .celda-hora, .celda-fecha {
        padding: 8px 12px;
      }
      .celda-hora:hover, .celda-fecha:hover {
        border: 2px solid var(--primary);
        border-radius: 4px;
        padding: 6px 10px;
      }
      .celda-nombre input, .celda-hora input, .celda-fecha input {
        width: 95%;
        padding: 6px 8px;
        border: 2px solid var(--primary);
        border-radius: 4px;
        font-size: 0.9em;
        font-family: inherit;
      }
      .fila-reproducida {
        background-color: #d4f5e3;
      }
      .fila-reproducida:hover {
        background-color: #c1eed6;
      }
      .celda-archivo {
        color: var(--gray-600);
        font-size: 0.85em;
      }
      .celda-acciones {
        display: flex;
        gap: 6px;
      }
      .btn-tabla {
        padding: 6px 10px;
        border: 1px solid var(--gray-300);
        background: var(--white);
        border-radius: 4px;
        cursor: pointer;
        font-size: 1em;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 36px;
        height: 36px;
      }
      .btn-tabla:hover {
        transform: scale(1.1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      }
      .btn-archivar:hover, .btn-restaurar:hover {
        background: var(--warning);
        color: var(--white);
      }
      .btn-eliminar:hover {
        background: var(--danger);
        color: var(--white);
      }
    `;
    document.head.appendChild(style);
  }
}

function editarCelda(cell, campo, id) {
  if (cell.querySelector("input")) return;
  const span = cell.querySelector("span");
  const valor = span.textContent;
  const input = document.createElement("input");
  input.type = campo === "fecha" ? "date" : campo === "hora" ? "time" : "text";
  input.value = valor === "-" ? "" : valor;
  cell.innerHTML = "";
  cell.appendChild(input);
  input.focus();
  input.select();

  async function guardarCambio() {
    const nuevoValor = input.value;
    try {
      await fetchAPI(`${API_URL}/canciones/${id}`, {
        method: "PUT",
        body: JSON.stringify({ [campo]: nuevoValor || null }),
      });
      await cargarCanciones();
      await actualizarPlayerWidget();
    } catch (error) {
      console.error("Error al guardar:", error);
      cell.innerHTML = `<span>${valor}</span>`;
    }
  }

  input.addEventListener("blur", guardarCambio);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") guardarCambio();
  });
}
function abrirModalAgregarCancion() {
  document.getElementById("modalAgregarCancion").classList.add("abierto");
  cargarArchivos();
}
function cerrarModalAgregarCancion() {
  document.getElementById("modalAgregarCancion").classList.remove("abierto");
  document.getElementById("formularioCancion").reset();
}
function abrirModalProgramacion() {
  document.getElementById("modalProgramacionRapida").classList.add("abierto");
  const hoy = new Date().toISOString().split("T")[0];
  document.getElementById("fechaInicio").value = hoy;
  cargarArchivos();
  // Cargar archivos en el selector de programación
  const selectArchivo = document.getElementById("archivoProgramacion");
  if (selectArchivo && archivosDisponibles && archivosDisponibles.length > 0) {
    selectArchivo.innerHTML =
      '<option value="">-- Selecciona uno o más archivos --</option>';
    archivosDisponibles.forEach((archivo) => {
      const option = document.createElement("option");
      option.value = archivo.nombre;
      option.textContent = `${archivo.nombre} (${formatarTamaño(archivo.tamaño)})`;
      selectArchivo.appendChild(option);
    });
  }
}
function cerrarModalProgramacion() {
  document
    .getElementById("modalProgramacionRapida")
    .classList.remove("abierto");
  document.getElementById("formularioProgramacionRapida").reset();
}
function abrirModalCargaRemota() {
  document.getElementById("modalCargaRemota").classList.add("abierto");
}
function cerrarModalCargaRemota() {
  document.getElementById("modalCargaRemota").classList.remove("abierto");
  document.getElementById("fileInput").value = "";
}
function cambiarTipo() {
  const tipo = document.getElementById("tipo").value;
  document.getElementById("grupoFecha").style.display =
    tipo === "fecha" ? "block" : "none";
  document.getElementById("grupoDias").style.display =
    tipo === "dia_semana" ? "block" : "none";
}
async function agregarCancion(e) {
  e.preventDefault();
  const nombre = document.getElementById("nombre").value;
  const archivo = document.getElementById("archivo").value;
  const tipo = document.getElementById("tipo").value;
  const hora = document.getElementById("hora").value;
  const fecha = document.getElementById("fecha").value;
  const dias = [];
  document.querySelectorAll('input[name="dia"]:checked').forEach((checkbox) => {
    dias.push(checkbox.value);
  });
  const data = {
    nombre,
    archivo,
    tipo_planificacion: tipo,
    hora,
    fecha: fecha || undefined,
    dias: dias.length > 0 ? dias : undefined,
    habilitada: true,
  };
  try {
    const response = await fetchAPI(`${API_URL}/canciones`, {
      method: "POST",
      body: JSON.stringify(data),
    });
    alert("¡Canción añadida exitosamente!");
    cerrarModalAgregarCancion();
    await cargarCanciones();
  } catch (error) {
    alert("Error al añadir canción: " + error.message);
  }
}
async function reproducirCancion(nombreArchivo) {
  try {
    // Reproducir el audio directamente en el navegador
    const audioPlayer =
      document.getElementById("audioPlayer") || crearAudioPlayer();
    audioPlayer.src = `/canciones/${nombreArchivo}`;
    audioPlayer.play();

    // Notificar al backend
    await fetchAPI(`${API_URL}/reproducir/${nombreArchivo}`, {
      method: "POST",
    });
    alert("Reproduciendo: " + nombreArchivo);
    await cargarEstado();
  } catch (error) {
    alert("Error reproduciendo: " + error.message);
  }
}

function crearAudioPlayer() {
  let audio = document.getElementById("audioPlayer");
  if (!audio) {
    audio = document.createElement("audio");
    audio.id = "audioPlayer";
    audio.hidden = true;
    document.body.appendChild(audio);
  }
  return audio;
}
async function detenerCancion() {
  try {
    await fetchAPI(`${API_URL}/detener`, { method: "POST" });
    alert("Reproducción detenida");
    await cargarEstado();
  } catch (error) {
    alert("Error deteniendo: " + error.message);
  }
}
async function eliminarCancion(id) {
  if (!confirm("¿Estás seguro de que quieres eliminar esta canción?")) return;
  try {
    await fetchAPI(`${API_URL}/canciones/${id}`, { method: "DELETE" });
    await cargarCanciones();
  } catch (error) {
    alert("Error eliminando canción: " + error.message);
  }
}
async function archivarCancion(id) {
  // Función eliminada - no se usa archivado
}
async function desarchivarCancion(id) {
  try {
    await fetchAPI(`${API_URL}/canciones/${id}`, {
      method: "PUT",
      body: JSON.stringify({ archivado: false }),
    });
    await cargarCanciones();
  } catch (error) {
    alert("Error desarchivando canción: " + error.message);
  }
}
function actualizarResumenProgramacion() {
  const fechaInicio = new Date(document.getElementById("fechaInicio").value);
  const fechaFin = new Date(document.getElementById("fechaFin").value);
  const incluirFinSemana = document.getElementById("incluirFinSemana").checked;
  const selectArchivo = document.getElementById("archivoProgramacion");
  const archivosSeleccionados = Array.from(selectArchivo.selectedOptions).map(
    (opt) => opt.value,
  );

  if (archivosSeleccionados.length === 0) {
    document.getElementById("resumenProgramacion").innerHTML =
      '<p style="color: #999; margin: 0;">Selecciona al menos un archivo</p>';
    return;
  }
  if (!fechaInicio || !fechaFin || fechaInicio > fechaFin) {
    document.getElementById("resumenProgramacion").innerHTML =
      '<p style="color: #d32f2f; margin: 0;">Fechas inválidas</p>';
    return;
  }
  let count = 0;
  const currentDate = new Date(fechaInicio);
  while (currentDate <= fechaFin) {
    const dayOfWeek = currentDate.getDay();
    if (incluirFinSemana || (dayOfWeek !== 0 && dayOfWeek !== 6)) {
      count++;
    }
    currentDate.setDate(currentDate.getDate() + 1);
  }
  const totalCanciones = count;
  const mensaje =
    count === 0
      ? "No hay días seleccionados"
      : `<span style="color: #4caf50; font-weight: bold;">✓ Se programarán ${totalCanciones} canción(es)</span><br><span style="font-size: 0.85em; color: #666;">${archivosSeleccionados.length} archivo(s) en rotativa × ${count} día(s)</span><br><span style="font-size: 0.85em; color: #666;">Del ${fechaInicio.toLocaleDateString("es-ES")} al ${fechaFin.toLocaleDateString("es-ES")}</span>`;
  document.getElementById("resumenProgramacion").innerHTML = mensaje;
}
async function generarProgramacionRapida(e) {
  e.preventDefault();
  const selectArchivo = document.getElementById("archivoProgramacion");
  const archivosSeleccionados = Array.from(selectArchivo.selectedOptions).map(
    (opt) => opt.value,
  );

  if (archivosSeleccionados.length === 0) {
    alert("Por favor selecciona al menos un archivo");
    return;
  }

  const nombreBase =
    document.getElementById("nombre").value || "Canción programada";
  const fechaInicio = new Date(document.getElementById("fechaInicio").value);
  const fechaFin = new Date(document.getElementById("fechaFin").value);
  const horaRapida = document.getElementById("horaRapida").value;
  const incluirFinSemana = document.getElementById("incluirFinSemana").checked;

  const currentDate = new Date(fechaInicio);
  let cancionesCreadas = 0;
  let indiceCancion = 0;

  while (currentDate <= fechaFin) {
    const dayOfWeek = currentDate.getDay();
    if (incluirFinSemana || (dayOfWeek !== 0 && dayOfWeek !== 6)) {
      // Seleccionar el siguiente archivo de forma rotativa
      const archivo =
        archivosSeleccionados[indiceCancion % archivosSeleccionados.length];

      const data = {
        nombre: `${nombreBase} - ${currentDate.toLocaleDateString("es-ES")}`,
        archivo,
        tipo_planificacion: "fecha",
        hora: horaRapida,
        fecha: currentDate.toISOString().split("T")[0],
        habilitada: true,
      };

      try {
        await fetchAPI(`${API_URL}/canciones`, {
          method: "POST",
          body: JSON.stringify(data),
        });
        cancionesCreadas++;
        indiceCancion++;
      } catch (error) {
        console.error("Error creando canción:", error);
      }
    }
    currentDate.setDate(currentDate.getDate() + 1);
  }

  alert(
    `¡${cancionesCreadas} canciones programadas exitosamente! (${archivosSeleccionados.length} archivo(s))`,
  );
  cerrarModalProgramacion();
  await cargarCanciones();
}
function toggleEstadoPanel() {
  const panel = document.getElementById("panelEstado");
  panel.classList.toggle("mostrado");
}
function cerrarEstadoPanel() {
  const panel = document.getElementById("panelEstado");
  panel.classList.remove("mostrado");
}
function minimizarPanel() {
  // Función deprecada - ahora se usa cerrarEstadoPanel
  cerrarEstadoPanel();
}
function copiarDatosRemoto() {
  const ip = document.getElementById("estadoIP").textContent;
  const puerto = document.getElementById("estadoPuerto").textContent;
  const datos = `${ip}:${puerto}`;
  navigator.clipboard
    .writeText(datos)
    .then(() => {
      alert("Datos copiados: " + datos);
    })
    .catch((err) => {
      alert("Error al copiar: " + err);
    });
}
function handleDragOver(e) {
  e.preventDefault();
  document.getElementById("uploadArea").classList.add("dragover");
}
function handleDragLeave(e) {
  e.preventDefault();
  document.getElementById("uploadArea").classList.remove("dragover");
}
function handleDrop(e) {
  e.preventDefault();
  document.getElementById("uploadArea").classList.remove("dragover");
  const files = e.dataTransfer.files;
  handleFileSelect({ target: { files } });
}
function handleFileSelect(e) {
  const files = e.target.files;
  uploadarArchivos(files);
}
async function uploadarArchivos(files) {
  if (files.length === 0) return;
  for (let file of files) {
    if (!file.name.toLowerCase().endsWith(".mp3")) {
      alert("Solo se permiten archivos MP3");
      return;
    }
  }
  document.getElementById("uploadProgress").style.display = "block";
  let uploadedCount = 0;
  for (let file of files) {
    try {
      const formData = new FormData();
      formData.append("file", file);
      const response = await fetch(`${API_URL}/cargar-archivo`, {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        uploadedCount++;
        const progress = (uploadedCount / files.length) * 100;
        document.getElementById("progressFill").style.width = progress + "%";
        document.getElementById("uploadStatus").textContent =
          `Subidos ${uploadedCount} de ${files.length} archivos...`;
      }
    } catch (error) {
      console.error("Error subiendo archivo:", error);
    }
  }
  document.getElementById("uploadProgress").style.display = "none";
  alert(`¡${uploadedCount} archivo(s) subido(s) exitosamente!`);
  await cargarArchivos();
  cerrarModalCargaRemota();
}
async function apagarAplicacion() {
  if (!confirm("¿Estás seguro de que quieres apagar la aplicación?")) return;
  try {
    await fetchAPI(`${API_URL}/apagar`, { method: "POST" });
  } catch (error) {
    console.error("Error apagando:", error);
  }
}
document.addEventListener("visibilitychange", async () => {
  if (!document.hidden) {
    await cargarCanciones();
    await cargarEstado();
  }
});
const observer = new MutationObserver(async (mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.attributeName === "class") {
      const tabPanes = document.querySelectorAll(".tab-pane");
      tabPanes.forEach((pane) => {
        if (pane.classList.contains("activo")) {
          const tabId = pane.id;
          if (tabId === "tab-canciones") {
            renderizarPlaylist();
          } else if (tabId === "tab-reproduccion") {
            renderizarReproduccion();
          }
        }
      });
    }
  });
});
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tab-pane").forEach((pane) => {
    observer.observe(pane, { attributes: true });
  });
});
