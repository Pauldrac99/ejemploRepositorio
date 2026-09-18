let currentUser = null;

const rutinasBase = {
    "Bajar de peso": {
        "Fácil": "Duración: 30-45 min\n1. Caminata ligera - 10 min\n2. Bicicleta estática - 10 min\n3. Sentadillas sin peso - 3x10\n4. Movilidad - 5 min",
        "Básico": "Duración: 45-60 min\n1. Caminata rápida - 10 min\n2. Bicicleta estática - 15 min\n3. Sentadillas - 3x12\n4. Zancadas - 3x10\n5. Cardio - 10 min",
        "Avanzado": "Duración: 60 min\n1. Carrera/HIIT - 15 min\n2. Burpees - 4x15\n3. Mountain Climbers - 4x30s\n4. Sentadillas con salto - 4x15\n5. Cardio suave - 10 min"
    },
    "Aumentar masa muscular": {
        "Fácil": "Duración: 40 min\n1. Calentamiento - 5 min\n2. Sentadillas asistidas - 3x10\n3. Flexiones rodillas - 3x8\n4. Remo mancuernas ligeras - 3x10",
        "Básico": "Duración: 50 min\n1. Sentadilla con mancuerna - 4x10\n2. Press de banca o pechadas - 4x10\n3. Peso muerto rumano - 3x10\n4. Press militar - 3x10",
        "Avanzado": "Duración: 60-75 min\n1. Sentadilla pesada - 4x8\n2. Press de banca pesado - 4x8\n3. Dominadas/Remo barra - 4x8\n4. Press militar - 4x8\n5. Curl bíceps / Tríceps - 3x12"
    }
};

function toggleView(view) {
    if (view === 'register') {
        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('register-section').classList.remove('hidden');
    } else {
        document.getElementById('register-section').classList.add('hidden');
        document.getElementById('login-section').classList.remove('hidden');
    }
}

async function registrar() {
    const nombre = document.getElementById('reg-nombre').value;
    const apellido = document.getElementById('reg-apellido').value;
    const correo = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const edad = document.getElementById('reg-edad').value;

    if (!nombre || !correo || !password) {
        alert("Por favor completa los campos requeridos.");
        return;
    }

    const response = await fetch('/api/registro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, apellido, correo, password, edad })
    });

    const data = await response.json();
    alert(data.message);
    if (data.success) toggleView('login');
}

async function login() {
    const correo = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, password })
    });

    const data = await response.json();

    if (data.success) {
        currentUser = data.user;
        document.getElementById('login-section').classList.add('hidden');

        if (currentUser.rol === 'entrenador') {
            document.getElementById('trainer-section').classList.remove('hidden');
            cargarClientesEntrenador();
        } else {
            document.getElementById('user-section').classList.remove('hidden');
            document.getElementById('welcome-msg').innerText = `¡Bienvenido, ${currentUser.nombre}!`;
            document.getElementById('select-objetivo').value = currentUser.objetivo || '';
            document.getElementById('select-nivel').value = currentUser.nivel || '';
        }
    } else {
        alert(data.message);
    }
}

async function guardarPreferencias() {
    const objetivo = document.getElementById('select-objetivo').value;
    const nivel = document.getElementById('select-nivel').value;

    if (!objetivo || !nivel) {
        alert("Selecciona un objetivo y un nivel.");
        return;
    }

    const response = await fetch('/api/actualizar-perfil', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: currentUser.id, objetivo, nivel })
    });

    const data = await response.json();
    alert(data.message);

    currentUser.objetivo = objetivo;
    currentUser.nivel = nivel;
}

function mostrarRutina() {
    const objetivo = document.getElementById('select-objetivo').value;
    const nivel = document.getElementById('select-nivel').value;
    const box = document.getElementById('routine-container');

    if (!objetivo || !nivel) {
        alert("Primero debes seleccionar un objetivo y nivel.");
        return;
    }

    const rutina = rutinasBase[objetivo]?.[nivel];
    if (rutina) {
        box.innerHTML = `<h4>Rutina: ${objetivo} (${nivel})</h4><pre style="white-space: pre-wrap;">${rutina}</pre>`;
        box.classList.remove('hidden');
    }
}

async function cargarClientesEntrenador() {
    const response = await fetch('/api/entrenador/clientes');
    const data = await response.json();
    const listDiv = document.getElementById('trainer-clients-list');
    listDiv.innerHTML = '';

    if (data.clientes.length === 0) {
        listDiv.innerHTML = '<p>No hay clientes registrados.</p>';
        return;
    }

    data.clientes.forEach(c => {
        listDiv.innerHTML += `
            <div class="client-card">
                <p><strong>Cliente:</strong> ${c.nombre} ${c.apellido}</p>
                <p><strong>Correo:</strong> ${c.correo} | <strong>Edad:</strong> ${c.edad}</p>
                <p><strong>Objetivo:</strong> ${c.objetivo || 'No definido'}</p>
                <p><strong>Nivel:</strong> ${c.nivel || 'No definido'}</p>
            </div>
        `;
    });
}

function logout() {
    currentUser = null;
    document.getElementById('user-section').classList.add('hidden');
    document.getElementById('trainer-section').classList.add('hidden');
    document.getElementById('routine-container').classList.add('hidden');
    document.getElementById('login-section').classList.remove('hidden');
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js').catch(err => console.log(err));
}