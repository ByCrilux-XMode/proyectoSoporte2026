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

    # 1. Cargar Requisitos de Muestra (Diccionario: id_examen -> id_tipo_muestra)
    cursor.execute("SELECT id_examen, id_tipo_muestra FROM examen_requisito_muestra")
    # Creamos un mapa para saber qué tipo de muestra necesita cada examen
    mapa_requisitos = {row[0]: row[1] for row in cursor.fetchall()}

    # 2. Preparación de universos
    ids_pacientes = list(range(1, 27378))
    ids_examenes = list(range(1, 53))
    ids_doctores = list(range(1, 11))
    ids_recepcionistas = list(range(1, 10))

    # TODOS tengan 1 visita + recurrencia
    lista_ids_final = ids_pacientes.copy()
    pacientes_frecuentes = random.sample(ids_pacientes, 8000)
    for _ in range(12623):
        lista_ids_final.append(random.choice(pacientes_frecuentes))

    random.shuffle(lista_ids_final)

    # Contadores globales
    id_detalle_cont = 1
    id_muestra_cont = 1

    print(f"Generando {len(lista_ids_final)} órdenes con lógica de muestras...")

    for i, id_p in enumerate(lista_ids_final, start=1):
        id_orden = i
        fecha_dt = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 730))
        fecha_str = fecha_dt.strftime('%Y-%m-%d')
        
        # A. Crear Orden
        cursor.execute("""
            INSERT INTO orden_laboratorio (id_orden_lab, fecha_orden, estado, numero_orden, id_paciente, id_cliente, id_doctor, id_recepcionista)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
            (id_orden, fecha_str, "Registrado", 10000 + i, id_p, id_p, random.choice(ids_doctores), random.choice(ids_recepcionistas))
        )

        # B. Lógica de Muestras: ¿Qué exámenes pidió y qué muestras generan?
        n_ex = random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.2, 0.08, 0.02], k=1)[0]
        examenes_seleccionados = random.sample(ids_examenes, n_ex)

        # Agrupamos exámenes por el tipo de muestra que requieren para no crear tubos de más
        # Ejemplo: Si 2 exámenes piden 'Sangre', se crea 1 sola muestra de sangre.
        muestras_de_esta_orden = {} # Tipo_Muestra -> ID_Muestra_Generado

        for id_ex in examenes_seleccionados:
            tipo_necesario = mapa_requisitos.get(id_ex, 1) # Default 1 si no hay requisito

            if tipo_necesario not in muestras_de_esta_orden:
                # Insertar nueva muestra física
                cod_m = f"M-{id_p}-{id_muestra_cont}"
                cursor.execute("""
                    INSERT INTO muestra (id_muestra, fecha_toma, estado, codigo_muestra, id_tipo_muestra)
                    VALUES (?, ?, ?, ?, ?)""",
                    (id_muestra_cont, fecha_str, "Recolectada", cod_m, tipo_necesario)
                )
                muestras_de_esta_orden[tipo_necesario] = id_muestra_cont
                id_muestra_actual = id_muestra_cont
                id_muestra_cont += 1
            else:
                # Ya existe un tubo para este tipo de muestra en esta orden
                id_muestra_actual = muestras_de_esta_orden[tipo_necesario]

            # C. Crear Detalle de Orden vinculado a la Muestra
            cursor.execute("""
                INSERT INTO detalle_orden_examen (id_detalle_orden_examen, id_orden_lab, id_examen, id_muestra)
                VALUES (?, ?, ?, ?)""",
                (id_detalle_cont, id_orden, id_ex, id_muestra_actual)
            )
            id_detalle_cont += 1

        # Control de transacciones cada 500 órdenes para no saturar
        if i % 500 == 0:
            con.commit()
            print(f"Progreso: {i} órdenes y sus muestras procesadas...")

    con.commit()
    con.close()
    print("--- Proceso finalizado: Órdenes y Muestras sincronizadas ---")

if __name__ == "__main__":
    poblar_movimiento_total()