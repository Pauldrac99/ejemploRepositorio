import os
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

def get_db_connection():
    conn = sqlite3.connect('gymfit.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/registro', methods=['POST'])
def registro():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, apellido, correo, password, edad)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['nombre'], data['apellido'], data['correo'], data['password'], data['edad']))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Usuario registrado exitosamente"})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"success": False, "message": "El correo ya está registrado"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM usuarios WHERE correo = ? AND password = ?',
        (data['correo'], data['password'])
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "user": dict(user)})
    return jsonify({"success": False, "message": "Correo o contraseña incorrectos"}), 401

# Actualizar Objetivo y Nivel del Cliente
@app.route('/api/actualizar-perfil', methods=['POST'])
def actualizar_perfil():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios 
        SET objetivo = ?, nivel = ? 
        WHERE id = ?
    ''', (data['objetivo'], data['nivel'], data['user_id']))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Preferencias guardadas con éxito"})

# Obtener todos los clientes (Para el Entrenador)
@app.route('/api/entrenador/clientes', methods=['GET'])
def obtener_clientes():
    conn = get_db_connection()
    clientes = conn.execute("SELECT nombre, apellido, correo, edad, objetivo, nivel FROM usuarios WHERE rol = 'cliente'").fetchall()
    conn.close()
    return jsonify({"success": True, "clientes": [dict(c) for c in clientes]})

if __name__ == '__main__':
    # Lee el puerto que le asigna Render automáticamente. Si estás en tu PC, usará el 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)