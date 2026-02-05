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

    print("Iniciando generación masiva de resultados y hallazgos...")

    # 1. Cargar Bioquímicos
    cursor.execute("SELECT id_bioquimico FROM bioquimico")
    ids_bioquimicos = [row[0] for row in cursor.fetchall()]

    # 2. Mapa de Referencias (Optimizado en memoria)
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

    # 3. Lógica Diagnóstica (Relación examen -> enfermedad)
    logica_diagnostica = {
        1: [2, 12, 14], 3: [2, 12], 5: [18], 6: [2, 14], 8: [1, 11],
        9: [1, 11], 10: [16], 11: [16], 12: [15], 13: [4], 15: [5, 13],
        16: [5, 13], 17: [7], 18: [9], 20: [17], 22: [18], 23: [8],
        26: [10], 27: [10], 29: [6], 31: [16], 32: [6], 35: [3],
        36: [3], 37: [3], 39: [19], 40: [1, 19], 48: [20]
    }

    # 4. Obtener solo exámenes PAGADOS (Filtro de integridad de negocio)
    print("Consultando exámenes pagados pendientes de resultado...")
    cursor.execute("""
        SELECT doe.id_detalle_orden_examen, doe.id_examen, ol.fecha_orden
        FROM detalle_orden_examen doe
        JOIN orden_laboratorio ol ON doe.id_orden_lab = ol.id_orden_lab
        JOIN factura f ON ol.id_orden_lab = f.id_orden_lab
        WHERE f.id_estado = 1 
    """)
    examenes_a_procesar = cursor.fetchall()

    # Contadores y Batches
    id_res_cont = 1
    id_det_res_cont = 1
    batch_resultados = []
    batch_detalles = []
    batch_hallazgos = []

    for det_id, ex_id, fecha_o in examenes_a_procesar:
        id_bio = random.choice(ids_bioquimicos)
        
        # Lógica de entrega (75% puntual, 20% retraso leve, 5% demora)
        cat = random.choices(['P', 'R', 'E'], weights=[0.75, 0.20, 0.05], k=1)[0]
        retraso = random.randint(1,2) if cat == 'P' else random.randint(3,5) if cat == 'R' else random.randint(6,12)
        fecha_res = fecha_o + timedelta(days=retraso)

        # A. Preparar Cabecera de Resultado
        batch_resultados.append((id_res_cont, fecha_res.strftime('%Y-%m-%d'), id_bio, det_id))

        # B. Generar Valores de Parámetros
        fue_patologico = False
        if ex_id in mapa_referencias:
            for p_id, ref_id, v_min, v_max, unidad in mapa_referencias[ex_id]:
                # 85% sanos, 15% fuera de rango (fluctuación real)
                es_sano = random.random() > 0.15 
                if es_sano:
                    valor = random.uniform(v_min, v_max)
                else:
                    fue_patologico = True
                    # Generar valor alto o bajo fuera de los límites
                    if random.random() > 0.5:
                        valor = v_max + random.uniform(v_max * 0.1, v_max * 0.5)
                    else:
                        valor = max(0, v_min - random.uniform(v_min * 0.1, v_min * 0.5))

                batch_detalles.append((id_det_res_cont, round(valor, 2), unidad, p_id, ref_id, id_res_cont))
                id_det_res_cont += 1

        # C. Generar Hallazgos Diagnósticos (Solo si hubo valores alterados)
        if fue_patologico and ex_id in logica_diagnostica:
            enfermedades = logica_diagnostica[ex_id]
            # Elegir 1 o 2 posibles enfermedades relacionadas
            elegidas = random.sample(enfermedades, k=random.randint(1, min(2, len(enfermedades))))
            for enf_id in elegidas:
                obs = random.choice(["Hallazgos clínicos alterados.", "Sugerir correlación clínica.", "Paciente requiere seguimiento."])
                batch_hallazgos.append((obs, enf_id, id_res_cont))

        # D. Inserción por Lotes (Cada 1000 resultados)
        if len(batch_resultados) >= 1000:
            cursor.executemany("INSERT INTO resultado (id_resultado, fecha, id_bioquimico, id_detalle_orden_examen) VALUES (?,?,?,?)", batch_resultados)
            cursor.executemany("INSERT INTO detalle_resultado VALUES (?,?,?,?,?,?)", batch_detalles)
            if batch_hallazgos:
                cursor.executemany("INSERT INTO hallazgo_diagnostico VALUES (?,?,?)", batch_hallazgos)
            con.commit()
            print(f"Progreso: {id_res_cont} informes médicos procesados...")
            batch_resultados, batch_detalles, batch_hallazgos = [], [], []

        id_res_cont += 1

    # Insertar remanentes finales
    if batch_resultados:
        cursor.executemany("INSERT INTO resultado (id_resultado, fecha, id_bioquimico, id_detalle_orden_examen) VALUES (?,?,?,?)", batch_resultados)
        cursor.executemany("INSERT INTO detalle_resultado VALUES (?,?,?,?,?,?)", batch_detalles)
        if batch_hallazgos:
            cursor.executemany("INSERT INTO hallazgo_diagnostico VALUES (?,?,?)", batch_hallazgos)
        con.commit()

    con.close()
    print(f"--- Proceso Finalizado: {id_res_cont-1} resultados clínicos generados ---")

if __name__ == "__main__":
    poblar_resultados_analiticos()