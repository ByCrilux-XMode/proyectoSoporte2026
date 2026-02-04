import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime, date

def poblar_precios_historicos():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\SQLEXPRESS;'
        'DATABASE=LabX2;'
        'Trusted_Connection=yes;'
    )
    con = pyodbc.connect(conn_str)
    cursor = con.cursor()

    #1(2024 - 2025)
    periodos = [
        ('2024-01-01', '2024-03-31'),
        ('2024-04-01', '2024-06-30'),
        ('2024-07-01', '2024-09-30'),
        ('2024-10-01', '2024-12-31'),
        ('2025-01-01', '2025-03-31'),
        ('2025-04-01', '2025-06-30'),
        ('2025-07-01', '2025-09-30'),
        ('2025-10-01', '2025-12-31')
    ]

    #2 ids de examenes existentes
    cursor.execute("SELECT id_examen FROM examen")
    ids_examenes = [row[0] for row in cursor.fetchall()]

    precios_batch = []
    id_precio_cont = 1

    print("Generando historial de precios trimestrales...")

    for id_ex in ids_examenes:
        #Precio base inicial para el examen (entre 50 y 500 bolivianos)
        precio_base = np.random.randint(50, 500)
        
        for idx, (f_inicio, f_fin) in enumerate(periodos):
            # Variación aleatoria del precio cada trimestre (+/- 5%)
            variacion = np.random.uniform(0.95, 1.05)
            precio_actual = round(precio_base * variacion, 2)
            
            # El último periodo (oct-dic 2025) queda como Activo 'A', el resto Inactivo 'I'
            estado = 1 if idx == len(periodos) - 1 else 0
            
            precios_batch.append((
                id_precio_cont,
                precio_actual,
                f_inicio,
                f_fin,
                estado,
                id_ex
            ))
            id_precio_cont += 1
            
            # El precio actual se vuelve la base para el siguiente cambio
            precio_base = precio_actual

    try:
        cursor.executemany("""
            INSERT INTO examen_precio (id_examen_precio, precio, fecha_inicio, fecha_fin, estado, id_examen)
            VALUES (?, ?, ?, ?, ?, ?)""", precios_batch)
        con.commit()
        print(f"¡Éxito! Se generaron {len(precios_batch)} registros de precios históricos.")
    except Exception as e:
        print(f"Error: {e}")
        con.rollback()
    finally:
        con.close()

if __name__ == "__main__":
    poblar_precios_historicos()