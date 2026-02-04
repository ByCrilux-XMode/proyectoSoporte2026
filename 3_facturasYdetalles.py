import pyodbc
from datetime import datetime
import random
def poblar_facturacion_masiva():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\SQLEXPRESS;'
        'DATABASE=LabX2;'
        'Trusted_Connection=yes;'
    )
    
    try:
        con = pyodbc.connect(conn_str)
        cursor = con.cursor()
    except Exception as e:
        print(f"Error de conexión: {e}")
        return

    print("Iniciando proceso de facturación...")

    #Obtener todas las ordenes con sus detalles y fechas
    cursor.execute("""
        select ol.id_orden_lab, ol.fecha_orden, doe.id_detalle_orden_examen, doe.id_examen
        from orden_laboratorio ol
        join detalle_orden_examen doe ON ol.id_orden_lab = doe.id_orden_lab
    """)
    filas = cursor.fetchall()

    # Estructura para agrupar detalles por factura
    ordenes_procesadas = {}
    
    # 2. Buscar el precio histórico para cada examen en la fecha de la orden
    print("Calculando precios y subtotales...")
    for id_orden, fecha, id_detalle_oe, id_ex in filas:
        #precio vigente en la fecha de la orden
        cursor.execute("""
            select precio 
            from examen_precio 
            where id_examen = ? AND ? BETWEEN fecha_inicio AND fecha_fin
        """, (id_ex, fecha))
        
        resultado_precio = cursor.fetchone()
        precio_v = float(resultado_precio[0]) if resultado_precio else 0.0

        if id_orden not in ordenes_procesadas:
            ordenes_procesadas[id_orden] = {
                'fecha': fecha,
                'detalles': [],
                'subtotal_total': 0.0
            }
        
        subtotal_linea = precio_v # Cantidad es 1 por defecto ahora
        ordenes_procesadas[id_orden]['detalles'].append((precio_v, 0, subtotal_linea, id_detalle_oe))
        ordenes_procesadas[id_orden]['subtotal_total'] += subtotal_linea

    # 3. Inserción en Factura y Detalle_Factura
    id_factura_cont = 1
    id_detalle_fac_cont = 1
    
    facturas_batch = []
    detalles_f_batch = []

    estados = [1, 2, 3]
    pesos_estado = [0.80, 0.15, 0.05]
    metodos_pago = [1, 2, 3, 4]

    for id_orden, data in ordenes_procesadas.items():
        total_a_pagar = data['subtotal_total'] # Sin descuentos para esta prueba
        id_estado_factura = random.choices(estados, weights=pesos_estado, k=1)[0]
        id_metodo_pago = random.choice(metodos_pago)
        
        #faatura
        facturas_batch.append((
            id_factura_cont, data['fecha'], data['subtotal_total'], 0, total_a_pagar, id_estado_factura, id_orden, id_metodo_pago
        ))

        for p_u, desc, sub_l, id_doe in data['detalles']:
            # Tabla detalle_factura
            detalles_f_batch.append((
                id_detalle_fac_cont, p_u, desc, sub_l, id_factura_cont, id_doe
            ))
            id_detalle_fac_cont += 1
        
        id_factura_cont += 1

        # Commit cada 1000 facturas para eficiencia
        if id_factura_cont % 1000 == 0:
            cursor.executemany("INSERT INTO factura VALUES (?,?,?,?,?,?,?,?)", facturas_batch)
            cursor.executemany("INSERT INTO detalle_factura VALUES (?,?,?,?,?,?)", detalles_f_batch)
            con.commit()
            facturas_batch, detalles_f_batch = [], []
            print(f"Facturadas {id_factura_cont} órdenes...")

    # Insertar restantes
    if facturas_batch:
        cursor.executemany("INSERT INTO factura VALUES (?,?,?,?,?,?,?,?)", facturas_batch)
        cursor.executemany("INSERT INTO detalle_factura VALUES (?,?,?,?,?,?)", detalles_f_batch)
        con.commit()

    con.close()
    print("--- Proceso de facturación finalizado con éxito ---")

if __name__ == "__main__":
    poblar_facturacion_masiva()