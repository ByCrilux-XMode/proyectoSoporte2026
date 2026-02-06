import pyodbc
import random
from datetime import datetime, timedelta

def poblar_movimiento_final_corregido():
    conn_str = ('DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=LabX2;'
                'Trusted_Connection=yes;')
    con = pyodbc.connect(conn_str)
    cursor = con.cursor()

    # 1. IDENTIFICAR LOS "IDS MAESTROS" DE LAS EMPRESAS
    # En lugar de usar IDs aleatorios, buscamos el ID más bajo de cada empresa 
    # para usarlo como el ÚNICO pagador de ese convenio.
    print("Identificando IDs maestros de empresas...")
    cursor.execute("""
        SELECT MIN(id_cliente), nombre 
        FROM cliente 
        WHERE id_tipo_cliente <> 1 
        GROUP BY nombre
    """)
    # Esto crea un mapa: "YPFB Transporte" -> ID 23 (por ejemplo)
    mapa_maestros_empresa = {row[1]: row[0] for row in cursor.fetchall()}
    ids_maestros = list(mapa_maestros_empresa.values())

    cursor.execute("SELECT id_paciente FROM paciente")
    ids_pacientes = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id_examen, id_tipo_muestra FROM examen_requisito_muestra")
    mapa_requisitos = {row[0]: row[1] for row in cursor.fetchall()}

    ids_examenes = [row[0] for row in cursor.execute("SELECT id_examen FROM examen").fetchall()]
    ids_doctores = [row[0] for row in cursor.execute("SELECT id_doctor FROM doctor").fetchall()]
    ids_recepcionistas = [row[0] for row in cursor.execute("SELECT id_recepcionista FROM recepcionista").fetchall()]

    # Mezclamos pacientes para las órdenes
    lista_pacientes = ids_pacientes.copy()
    random.shuffle(lista_pacientes)

    id_detalle_cont = 1
    id_muestra_cont = 1
    batch_ordenes, batch_muestras, batch_detalles = [], [], []

    print(f"Generando órdenes con IDs de cliente consolidados...")

    for i, id_p in enumerate(lista_pacientes, start=1):
        id_orden = i
        fecha_str = (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 400))).strftime('%Y-%m-%d')
        
        # --- LÓGICA DE CONSOLIDACIÓN ---
        if random.random() < 0.30 and ids_maestros:
            # Seleccionamos UN SOLO ID de los maestros (ej. el ID 23 siempre será YPFB)
            id_c = random.choice(ids_maestros) 
        else:
            # El paciente es particular (se paga a sí mismo)
            id_c = id_p 
        
        batch_ordenes.append((id_orden, fecha_str, "Registrado", 10000 + i, id_p, id_c, 
                              random.choice(ids_doctores), random.choice(ids_recepcionistas)))

        # (La lógica de muestras y detalles se mantiene igual que antes...)
        n_ex = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1], k=1)[0]
        ex_sel = random.sample(ids_examenes, n_ex)
        muestras_orden = {}
        for id_ex in ex_sel:
            tipo_m = mapa_requisitos.get(id_ex, 1)
            if tipo_m not in muestras_orden:
                cod_m = f"M-{id_p}-{id_muestra_cont}"
                batch_muestras.append((id_muestra_cont, fecha_str, "Recolectada", None, cod_m, tipo_m))
                muestras_orden[tipo_m] = id_muestra_cont
                id_m_actual = id_muestra_cont
                id_muestra_cont += 1
            else:
                id_m_actual = muestras_orden[tipo_m]
            batch_detalles.append((id_detalle_cont, id_orden, id_ex, id_m_actual))
            id_detalle_cont += 1

        if i % 1000 == 0:
            cursor.executemany("INSERT INTO orden_laboratorio VALUES (?,?,?,?,?,?,?,?)", batch_ordenes)
            cursor.executemany("INSERT INTO muestra VALUES (?,?,?,?,?,?)", batch_muestras)
            cursor.executemany("INSERT INTO detalle_orden_examen VALUES (?,?,?,?)", batch_detalles)
            con.commit()
            batch_ordenes, batch_muestras, batch_detalles = [], [], []

    con.commit()
    con.close()
    print("--- Proceso Finalizado con IDs consolidados ---")

if __name__ == "__main__":
    poblar_movimiento_final_corregido()