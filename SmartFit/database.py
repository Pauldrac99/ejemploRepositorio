import sqlite3

def init_db():
    conn = sqlite3.connect('gymfit.db')
    cursor = conn.cursor()

    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            edad INTEGER,
            objetivo TEXT DEFAULT '',
            nivel TEXT DEFAULT '',
            rol TEXT DEFAULT 'cliente'
        )
    ''')

    # Usuario Entrenador por defecto
    cursor.execute("SELECT * FROM usuarios WHERE correo = 'trainer@gymfit.com'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO usuarios (nombre, apellido, correo, password, edad, rol)
            VALUES ('Entrenador', 'GymFit', 'trainer@gymfit.com', '1234', 30, 'entrenador')
        ''')

    conn.commit()
    conn.close()
    print("Base de datos creada exitosamente.")

if __name__ == '__main__':
    init_db()