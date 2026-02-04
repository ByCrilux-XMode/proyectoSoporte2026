import pyodbc
import random
from datetime import datetime

def poblar_resultados_analiticos():
    conn_str = ('DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\SQLEXPRESS;'
                'DATABASE=LabX2;'
                'Trusted_Connection=yes;')
    con = pyodbc.connect(conn_str)
    cursor = con.cursor()

    print("Iniciando generación de resultados médicos...")

    #coje id de bioquimicos y enfermedades
    cursor.execute("SELECT id_bioquimico FROM bioquimico")
    ids_bioquimicos = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id_enfermedad FROM enfermedad")
    ids_enfermedades = [row[0] for row in cursor.fetchall()]

    # Traemos los parámetros con sus valores de referencia para generar números realistas
    cursor.execute("""
        SELECT p.id_parametro, p.id_examen, vr.id_valor_ref, vr.rango_minimo, vr.rango_maximo, vr.unidad_medida
        FROM parametro p
        JOIN valor_referencia vr ON p.id_parametro = vr.id_parametro
    """)

    referencias = cursor.fetchall()
   
    mapa_referencias = {}
    for p_id, ex_id, ref_id, v_min, v_max, uni in referencias:
        if ex_id not in mapa_referencias:
            mapa_referencias[ex_id] = []
        mapa_referencias[ex_id].append((p_id, ref_id, float(v_min), float(v_max), uni))

    # 2. Obtener detalles de órdenes que están pagadas 
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

    for det_id, ex_id, muestra_id, fecha_o in examenes_a_procesar:
        id_bio = random.choice(ids_bioquimicos)
        
        # A. Insertar Cabecera de Resultado (Relación 1:1 con detalle_orden_examen)
        cursor.execute("""
            INSERT INTO resultado (id_resultado, fecha, id_bioquimico, id_detalle_orden_examen, id_muestra)
            VALUES (?, ?, ?, ?, ?)""",
            (id_res_cont, fecha_o, id_bio, det_id, muestra_id)
        )

        # B. Generar Detalles de Resultado (Valores para cada parámetro)
        # Si el examen tiene parámetros configurados en el sistema:
        if ex_id in mapa_referencias:
            fuera_de_rango = False
            for p_id, ref_id, v_min, v_max, unidad in mapa_referencias[ex_id]:
                # Simulamos un valor: 80% de probabilidad de estar sano, 20% de estar enfermo
                es_sano = random.random() > 0.2
                if es_sano:
                    valor_final = random.uniform(v_min, v_max)
                else:
                    # Generar valor alterado (por arriba o por abajo)
                    fuera_de_rango = True
                    if random.choice([True, False]):
                        valor_final = v_max + random.uniform(1, 20)
                    else:
                        valor_final = max(0, v_min - random.uniform(1, 10))

                cursor.execute("""
                    INSERT INTO detalle_resultado (id_detalle_resultado, valor_obtenido, unidad_medida, id_parametro, id_valor_ref, id_resultado)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (id_det_res_cont, round(valor_final, 2), unidad, p_id, ref_id, id_res_cont)
                )
                id_det_res_cont += 1

            logica_diagnostica = {
                # AREA 1: HEMATOLOGÍA
                1: [2, 12, 14], # HEMOGRAMA -> Anemia (2), Síndrome Anémico (12), Policitemia (14)
                3: [2, 12],     # RETICULOCITOS -> Anemia (2, 12)
                5: [18],        # VSG -> Artritis Reumatoide (18)
                6: [2, 14],     # FROTIS -> Anemia (2), Policitemia (14)
                
                # AREA 2: QUÍMICA SANGUÍNEA
                8: [1, 11],     # HBA1C -> Diabetes (1), Crisis Hiperglucémica (11)
                9: [1, 11],     # GLICEMIA -> Diabetes (1), Crisis Hiperglucémica (11)
                10: [16],       # CREATININA -> Síndrome Nefrótico (16)
                11: [16],       # UREA -> Síndrome Nefrótico (16)
                12: [15],       # ACIDO URICO -> Hiperuricemia (15)
                13: [4],        # COLESTEROL -> Hipercolesterolemia (4)
                15: [5, 13],    # TGO -> Hepatitis (5), Insuficiencia Hepática (13)
                16: [5, 13],    # BILIRRUBINAS -> Hepatitis (5), Insuficiencia Hepática (13)
                40: [1, 19],    # INSULINA -> Diabetes (1), Ovario Poliquístico (19)

                # AREA 3: SEROLOGÍA / INMUNOLOGÍA
                17: [7],        # WIDAL -> Fiebre Tifoidea (7)
                18: [9],        # H. PYLORI -> Gastritis por H. Pylori (9)
                20: [17],       # CHAGAS ELISA -> Chagas Crónico (17)
                22: [18],       # RA TEST -> Artritis Reumatoide (18)
                23: [8],        # DENGUE -> Dengue con signos de alarma (8)
                
                # AREA 4: COPROLOGÍA
                26: [10],       # COPRO SIMPLE -> Amibiasis (10)
                27: [10],       # MOCO FECAL -> Amibiasis (10)
                
                # AREA 5: ORINA
                29: [6],        # EGO -> Infección Urinaria (6)
                31: [16],       # PROTEINURIA -> Síndrome Nefrótico (16)
                
                # AREA 6: MICROBIOLOGÍA
                32: [6],        # UROCULTIVO -> Infección Urinaria (6)
                
                # AREA 7: HORMONAS
                35: [3],        # TSH -> Hipotiroidismo (3)
                36: [3],        # T4 LIBRE -> Hipotiroidismo (3)
                37: [3],        # T3 TOTAL -> Hipotiroidismo (3)
                39: [19],       # PROLACTINA -> Ovario Poliquístico (19)
                
                # AREA 9: TOXICOLOGÍA
                48: [20],       # PLOMO EN SANGRE -> Intoxicación por Metales Pesados (20)
            }

        if fuera_de_rango:
            # 1. Buscamos qué enfermedades corresponden a ESTE examen específico
            enfermedades_asociadas = logica_diagnostica.get(ex_id, [])
            if enfermedades_asociadas:
                # 2. De las asociadas, elegimos 1 o 2 para este paciente
                num_hallazgos = random.randint(1, min(2, len(enfermedades_asociadas)))
                enfermedades_paciente = random.sample(enfermedades_asociadas, num_hallazgos)

                for enf_id in enfermedades_paciente:
                    cursor.execute("""
                        INSERT INTO hallazgo_diagnostico (descripcion, id_enfermedad, id_resultado)
                        VALUES (?, ?, ?)""",
                        ("Valores alterados sugieren sospecha clínica.", enf_id, id_res_cont)
                    )

        id_res_cont += 1
        
        if id_res_cont % 500 == 0:
            con.commit()
            print(f"Progreso: {id_res_cont} resultados médicos validados...")

    con.commit()
    con.close()
    print("--- Proceso Analítico finalizado: Base de datos LabX2 con datos médicos reales ---")

if __name__ == "__main__":
    poblar_resultados_analiticos()