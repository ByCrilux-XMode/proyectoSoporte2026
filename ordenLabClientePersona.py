import pyodbc
import pandas as pd
import random
from datetime import datetime, timedelta

def generar_movimiento_real():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=LabX2;'
        'Trusted_Connection=yes;'
    )
    
    try:
        con = pyodbc.connect(conn_str)
        cursor = con.cursor()
    except Exception as e:
        print(f"Error de conexión: {e}")
        return

    # Parámetros base
    ids_pacientes_clientes = list(range(1, 27378))
    ids_doctores = list(range(1, 6))
    ids_recepcionistas = list(range(1, 4))
    ids_examenes = list(range(1, 53))

    ordenes_batch = []
    detalles_batch = []
    
    id_detalle_cont = 1 # PK para detalle_orden_examen

    print("Procesando 27,377 órdenes coherentes...")

    for i in ids_pacientes_clientes:

        id_orden = i 
        fecha_orden = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 730))
        estado_orden = "Pendiente"
        num_orden_correlativo = 1000 + i #orden ficticio
        id_doc = random.choice(ids_doctores)
        id_rec = random.choice(ids_recepcionistas)

        ordenes_batch.append((
            id_orden, fecha_orden.strftime('%Y-%m-%d'), estado_orden, 
            num_orden_correlativo, i, i, id_doc, id_rec
        ))

        n_ex = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.4, 0.3, 0.02, 0.06], k=1)[0]
        examenes_random = random.sample(ids_examenes, n_ex)

        for id_ex in examenes_random:
            detalles_batch.append((id_detalle_cont, id_orden, id_ex))
            id_detalle_cont += 1

    #Inserción
    try:
        print("Insertando en orden_laboratorio...")
        cursor.executemany("""
            INSERT INTO orden_laboratorio 
            (id_orden_lab, fecha_orden, estado, numero_orden, id_paciente, id_cliente, id_doctor, id_recepcionista)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", ordenes_batch)
        
        print("Insertando en detalle_orden_examen...")
        cursor.executemany("""
            INSERT INTO detalle_orden_examen 
            (id_detalle_orden_examen, id_orden_lab, id_examen)
            VALUES (?, ?, ?)""", detalles_batch)
        
        con.commit()
        print(f"¡Se crearon {len(ordenes_batch)} órdenes y {len(detalles_batch)} detalles.")
    except Exception as e:
        print(f"Error en SQL: {e}")
        con.rollback()
    finally:
        con.close()

if __name__ == "__main__":
    generar_movimiento_real()