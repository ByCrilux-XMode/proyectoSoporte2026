import pyodbc
import random
from datetime import datetime, timedelta

def poblar_movimiento_total():
    conn_str = ('DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=LabX2;'
                'Trusted_Connection=yes;')
    con = pyodbc.connect(conn_str)
    cursor = con.cursor()

    print("Sincronizando universos de IDs y Requisitos...")
    
    # 1. Obtenemos los IDs de pacientes (que por tu script anterior coinciden con los IDs de clientes)
    cursor.execute("SELECT id_paciente FROM paciente")
    ids_pacientes = [row[0] for row in cursor.fetchall()]
    
    # 2. Cargar Requisitos de Muestra (id_examen -> id_tipo_muestra)
    cursor.execute("SELECT id_examen, id_tipo_muestra FROM examen_requisito_muestra")
    mapa_requisitos = {row[0]: row[1] for row in cursor.fetchall()}

    # 3. Cargar IDs de catálogos para evitar errores de FK
    ids_examenes = [row[0] for row in cursor.execute("SELECT id_examen FROM examen").fetchall()]
    ids_doctores = [row[0] for row in cursor.execute("SELECT id_doctor FROM doctor").fetchall()]
    ids_recepcionistas = [row[0] for row in cursor.execute("SELECT id_recepcionista FROM recepcionista").fetchall()]

    # 4. Generar lista de órdenes (Base + Recurrencia)
    lista_ids_pacientes = ids_pacientes.copy()
    # Simulamos que un 15% de los pacientes regresa para otro examen en el tiempo
    pacientes_recurrentes = random.sample(ids_pacientes, int(len(ids_pacientes) * 0.20))
    for _ in range(int(len(ids_pacientes) * 0.15)):
        lista_ids_pacientes.append(random.choice(pacientes_recurrentes))

    random.shuffle(lista_ids_pacientes)

    # Contadores para las llaves primarias
    id_detalle_cont = 1
    id_muestra_cont = 1
    
    # Batches para inserción masiva
    batch_ordenes = []
    batch_muestras = []
    batch_detalles = []

    print(f"Generando {len(lista_ids_pacientes)} órdenes y sus movimientos...")

    for i, id_p in enumerate(lista_ids_pacientes, start=1):
        id_orden = i
        # El cliente es el mismo ID que el paciente (según tu script de poblado anterior)
        id_c = id_p 
        
        fecha_dt = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 400))
        fecha_str = fecha_dt.strftime('%Y-%m-%d')
        
        # A. INSERT ORDEN_LABORATORIO
        # Columnas: id_orden_lab, fecha_orden, estado, numero_orden, id_paciente, id_cliente, id_doctor, id_recepcionista
        batch_ordenes.append((
            id_orden, fecha_str, "Registrado", 10000 + i, id_p, id_c, 
            random.choice(ids_doctores), random.choice(ids_recepcionistas)
        ))

        # B. LÓGICA DE EXÁMENES Y MUESTRAS
        n_ex = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05], k=1)[0]
        examenes_sel = random.sample(ids_examenes, n_ex)
        muestras_en_esta_orden = {} 

        for id_ex in examenes_sel:
            tipo_m_necesario = mapa_requisitos.get(id_ex, 1) 

            if tipo_m_necesario not in muestras_en_esta_orden:
                cod_m = f"M-{id_p}-{id_muestra_cont}"
                # Tabla muestra: id_muestra, fecha_toma, estado, observacion, codigo_muestra, id_tipo_muestra
                batch_muestras.append((id_muestra_cont, fecha_str, "Recolectada", None, cod_m, tipo_m_necesario))
                muestras_en_esta_orden[tipo_m_necesario] = id_muestra_cont
                id_m_actual = id_muestra_cont
                id_muestra_cont += 1
            else:
                id_m_actual = muestras_en_esta_orden[tipo_m_necesario]

            # C. INSERT DETALLE_ORDEN_EXAMEN
            # Columnas: id_detalle_orden_examen, id_orden_lab, id_examen, id_muestra
            batch_detalles.append((id_detalle_cont, id_orden, id_ex, id_m_actual))
            id_detalle_cont += 1

        # Ejecución por lotes para velocidad (cada 1000 órdenes)
        if i % 1000 == 0:
            cursor.executemany("INSERT INTO orden_laboratorio VALUES (?,?,?,?,?,?,?,?)", batch_ordenes)
            cursor.executemany("INSERT INTO muestra VALUES (?,?,?,?,?,?)", batch_muestras)
            cursor.executemany("INSERT INTO detalle_orden_examen VALUES (?,?,?,?)", batch_detalles)
            con.commit()
            batch_ordenes, batch_muestras, batch_detalles = [], [], []
            print(f"Progreso: {i} órdenes insertadas exitosamente...")

    # Inserción de los últimos registros
    if batch_ordenes:
        cursor.executemany("INSERT INTO orden_laboratorio VALUES (?,?,?,?,?,?,?,?)", batch_ordenes)
        cursor.executemany("INSERT INTO muestra VALUES (?,?,?,?,?,?)", batch_muestras)
        cursor.executemany("INSERT INTO detalle_orden_examen VALUES (?,?,?,?)", batch_detalles)
        con.commit()

    con.close()
    print(f"--- Proceso Terminado: {len(lista_ids_pacientes)} órdenes creadas ---")

if __name__ == "__main__":
    poblar_movimiento_total()