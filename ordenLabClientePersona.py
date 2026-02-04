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

    # 1. Preparación de universos
    ids_pacientes = list(range(1, 27378))
    ids_examenes = list(range(1, 53))
    ids_doctores = list(range(1, 11))
    ids_recepcionistas = list(range(1, 8))

    #TODOS tengan 1 visita
    lista_ids_final = ids_pacientes.copy()

    #recurrencia
    #subgrupo de 8,000 pacientes que suelen enfermarse más seguido
    pacientes_frecuentes = random.sample(ids_pacientes, 8000)
    for _ in range(12623):
        lista_ids_final.append(random.choice(pacientes_frecuentes))

    random.shuffle(lista_ids_final)

    ordenes_batch = []
    detalles_batch = []
    id_detalle_cont = 1

    print(f"Generando {len(lista_ids_final)} órdenes con recurrencia real...")

    for i, id_p in enumerate(lista_ids_final, start=1):
        id_orden = i
        # Fechas entre 2024 y 2025
        fecha_orden = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 730))
        
        ordenes_batch.append((
            id_orden, fecha_orden.strftime('%Y-%m-%d'), "Pendiente", 
            10000 + i, id_p, id_p, random.choice(ids_doctores), random.choice(ids_recepcionistas)
        ))

        # Detalle: de 1 a 5 exámenes sin repetir
        n_ex = random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.2, 0.08, 0.02], k=1)[0]
        examenes_seleccionados = random.sample(ids_examenes, n_ex)

        for id_ex in examenes_seleccionados:
            detalles_batch.append((id_detalle_cont, id_orden, id_ex))
            id_detalle_cont += 1

        # Insertar en bloques de 5000 para no saturar la memoria
        if i % 5000 == 0:
            cursor.executemany("INSERT INTO orden_laboratorio VALUES (?,?,?,?,?,?,?,?)", ordenes_batch)
            cursor.executemany("INSERT INTO detalle_orden_examen VALUES (?,?,?)", detalles_batch)
            con.commit()
            ordenes_batch, detalles_batch = [], []
            print(f"Progreso: {i} órdenes insertadas...")

    # Insertar remanentes
    if ordenes_batch:
        cursor.executemany("INSERT INTO orden_laboratorio VALUES (?,?,?,?,?,?,?,?)", ordenes_batch)
        cursor.executemany("INSERT INTO detalle_orden_examen VALUES (?,?,?)", detalles_batch)
        con.commit()

    con.close()
    print("--- Proceso de recurrencia finalizado con éxito ---")

if __name__ == "__main__":
    poblar_movimiento_total()