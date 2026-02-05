import pyodbc
import random
from datetime import datetime, timedelta

def poblar_resultados_analiticos():
    conn_str = ('DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=LabX2;'
                'Trusted_Connection=yes;')
    con = pyodbc.connect(conn_str)
    cursor = con.cursor()

    print("Iniciando generación de resultados médicos...")

    # 1. Preparación de Diccionarios y Listas (FUERA DEL BUCLE)
    cursor.execute("SELECT id_bioquimico FROM bioquimico")
    ids_bioquimicos = [row[0] for row in cursor.fetchall()]

    logica_diagnostica = {
        1: [2, 12, 14], 3: [2, 12], 5: [18], 6: [2, 14], 8: [1, 11],
        9: [1, 11], 10: [16], 11: [16], 12: [15], 13: [4], 15: [5, 13],
        16: [5, 13], 17: [7], 18: [9], 20: [17], 22: [18], 23: [8],
        26: [10], 27: [10], 29: [6], 31: [16], 32: [6], 35: [3],
        36: [3], 37: [3], 39: [19], 40: [1, 19], 48: [20]
    }

    cursor.execute("""
        SELECT p.id_parametro, p.id_examen, vr.id_valor_ref, vr.rango_minimo, vr.rango_maximo, vr.unidad_medida
        FROM parametro p
        JOIN valor_referencia vr ON p.id_parametro = vr.id_parametro
    """)
    mapa_referencias = {}
    for p_id, ex_id, ref_id, v_min, v_max, uni in cursor.fetchall():
        if ex_id not in mapa_referencias:
            mapa_referencias[ex_id] = []
        mapa_referencias[ex_id].append((p_id, ref_id, float(v_min or 0), float(v_max or 100), uni))

    # 2. Obtener órdenes pagadas
    cursor.execute("""
        SELECT doe.id_detalle_orden_examen, doe.id_examen, doe.id_muestra, ol.fecha_orden
        FROM detalle_orden_examen doe
        JOIN orden_laboratorio ol ON doe.id_orden_lab = ol.id_orden_lab
        JOIN factura f ON ol.id_orden_lab = f.id_orden_lab
        WHERE f.id_estado = 1 
    """)
    examenes_a_procesar = cursor.fetchall()

    id_res_cont = 1
    id_det_res_cont = 1
    batch_detalles = [] # Para inserción masiva

    for det_id, ex_id, muestra_id, fecha_o in examenes_a_procesar:
        id_bio = random.choice(ids_bioquimicos)
        
        # Lógica de retraso
        cat = random.choices(['P', 'R', 'E'], weights=[0.75, 0.20, 0.05], k=1)[0]
        retraso = random.randint(1,3) if cat == 'P' else random.randint(4,6) if cat == 'R' else random.randint(7,15)
        fecha_res = fecha_o + timedelta(days=retraso)

        # A. Insertar Cabecera de Resultado
        cursor.execute("""
            INSERT INTO resultado (id_resultado, fecha, id_bioquimico, id_detalle_orden_examen)
            VALUES (?, ?, ?, ?)""",
            (id_res_cont, fecha_res.strftime('%Y-%m-%d'), id_bio, det_id)
        )
        # Nota: He quitado id_muestra del INSERT porque quedamos en que ya no va ahí

        # B. Generar Detalles
        fuera_de_rango = False
        if ex_id in mapa_referencias:
            for p_id, ref_id, v_min, v_max, unidad in mapa_referencias[ex_id]:
                es_sano = random.random() > 0.2
                if es_sano:
                    valor = random.uniform(v_min, v_max)
                else:
                    fuera_de_rango = True
                    valor = v_max + random.uniform(1, 15) if random.random() > 0.5 else max(0, v_min - random.uniform(1, 5))

                batch_detalles.append((id_det_res_cont, round(valor, 2), unidad, p_id, ref_id, id_res_cont))
                id_det_res_cont += 1

        # C. Insertar Hallazgo si aplica
        if fuera_de_rango and ex_id in logica_diagnostica:
            asociadas = logica_diagnostica[ex_id]
            num = random.randint(1, min(2, len(asociadas)))
            elegidas = random.sample(asociadas, num)
            for enf_id in elegidas:
                cursor.execute("INSERT INTO hallazgo_diagnostico VALUES (?, ?, ?)", 
                               ("Hallazgos compatibles con cuadro clínico.", enf_id, id_res_cont))

        # Control de inserción masiva para detalles
        if len(batch_detalles) >= 1000:
            cursor.executemany("INSERT INTO detalle_resultado VALUES (?, ?, ?, ?, ?, ?)", batch_detalles)
            con.commit()
            batch_detalles = []

        id_res_cont += 1
        if id_res_cont % 500 == 0:
            print(f"Sincronizados {id_res_cont} informes médicos...")

    # Insertar remanentes
    if batch_detalles:
        cursor.executemany("INSERT INTO detalle_resultado VALUES (?, ?, ?, ?, ?, ?)", batch_detalles)
    
    con.commit()
    con.close()
    print("--- LabX2: Resultados y Diagnósticos finalizados con éxito ---")

if __name__ == "__main__":
    poblar_resultados_analiticos()