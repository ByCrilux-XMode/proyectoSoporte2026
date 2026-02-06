import pyodbc
import random
from datetime import datetime, timedelta

def poblar_movimiento_total_corporativo():
    conn_str = ('DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=LabX2;'
                'Trusted_Connection=yes;')
    con = pyodbc.connect(conn_str)
    cursor = con.cursor()

    print("Analizando estructura de Clientes y Pacientes...")
    
    # 1. Identificar Clientes Corporativos vs Particulares
    # Buscamos clientes que NO sean 'Persona Natural' (id_tipo_cliente != 1)
    cursor.execute("SELECT id_cliente FROM cliente WHERE id_tipo_cliente <> 1")
    ids_corporativos = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id_paciente FROM paciente")
    ids_pacientes = [row[0] for row in cursor.fetchall()]

    # 2. Cargar Requisitos y Catálogos
    cursor.execute("SELECT id_examen, id_tipo_muestra FROM examen_requisito_muestra")
    mapa_requisitos = {row[0]: row[1] for row in cursor.fetchall()}

    ids_examenes = [row[0] for row in cursor.execute("SELECT id_examen FROM examen").fetchall()]
    ids_doctores = [row[0] for row in cursor.execute("SELECT id_doctor FROM doctor").fetchall()]
    ids_recepcionistas = [row[0] for row in cursor.execute("SELECT id_recepcionista FROM recepcionista").fetchall()]

    # 3. Preparar Universo de Órdenes (Fluctuación de 200k aprox)
    lista_pacientes_ordenes = ids_pacientes.copy()
    # Añadimos recurrencia
    recurrentes = random.sample(ids_pacientes, int(len(ids_pacientes) * 0.15))
    lista_pacientes_ordenes.extend(recurrentes)
    random.shuffle(lista_pacientes_ordenes)

    # Contadores
    id_detalle_cont = 1
    id_muestra_cont = 1
    
    batch_ordenes, batch_muestras, batch_detalles = [], [], []

    print(f"Generando {len(lista_pacientes_ordenes)} órdenes con distribución corporativa...")

    for i, id_p in enumerate(lista_pacientes_ordenes, start=1):
        id_orden = i
        fecha_dt = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 400))
        fecha_str = fecha_dt.strftime('%Y-%m-%d')
        
        # --- LÓGICA DE ASIGNACIÓN DE CLIENTE ---
        # 30% de las órdenes pertenecen a un convenio corporativo (Seguros/Empresas)
        if random.random() < 0.30 and ids_corporativos:
            id_c = random.choice(ids_corporativos) # Muchos pacientes caen bajo el mismo ID corporativo
        else:
            id_c = id_p # El paciente se paga a sí mismo (Particular)
        
        # A. Orden_Laboratorio
        batch_ordenes.append((
            id_orden, fecha_str, "Registrado", 10000 + i, id_p, id_c, 
            random.choice(ids_doctores), random.choice(ids_recepcionistas)
        ))

        # B. Exámenes y Muestras
        n_ex = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.30, 0.15, 0.07, 0.03], k=1)[0]
        examenes_sel = random.sample(ids_examenes, n_ex)
        muestras_orden = {} 

        for id_ex in examenes_sel:
            tipo_m = mapa_requisitos.get(id_ex, 1) 

            if tipo_m not in muestras_orden:
                cod_m = f"M-{id_p}-{id_muestra_cont}"
                batch_muestras.append((id_muestra_cont, fecha_str, "Recolectada", None, cod_m, tipo_m))
                muestras_orden[tipo_m] = id_muestra_cont
                id_m_actual = id_muestra_cont
                id_muestra_cont += 1
            else:
                id_m_actual = muestras_orden[tipo_m]

            # C. Detalle_Orden_Examen
            batch_detalles.append((id_detalle_cont, id_orden, id_ex, id_m_actual))
            id_detalle_cont += 1

        # Commit por lotes de 1000
        if i % 1000 == 0:
            cursor.executemany("INSERT INTO orden_laboratorio VALUES (?,?,?,?,?,?,?,?)", batch_ordenes)
            cursor.executemany("INSERT INTO muestra VALUES (?,?,?,?,?,?)", batch_muestras)
            cursor.executemany("INSERT INTO detalle_orden_examen VALUES (?,?,?,?)", batch_detalles)
            con.commit()
            batch_ordenes, batch_muestras, batch_detalles = [], [], []
            print(f"Progreso: {i} órdenes corporativas y particulares procesadas...")

    # Insertar remanentes
    if batch_ordenes:
        cursor.executemany("INSERT INTO orden_laboratorio VALUES (?,?,?,?,?,?,?,?)", batch_ordenes)
        cursor.executemany("INSERT INTO muestra VALUES (?,?,?,?,?,?)", batch_muestras)
        cursor.executemany("INSERT INTO detalle_orden_examen VALUES (?,?,?,?)", batch_detalles)
        con.commit()

    con.close()
    print("--- Simulación Corporativa Finalizada ---")

if __name__ == "__main__":
    poblar_movimiento_total_corporativo()