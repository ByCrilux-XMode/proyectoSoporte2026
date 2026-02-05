import pyodbc
from datetime import datetime
import random

def poblar_facturacion_masiva():
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

    print("Iniciando proceso de facturación optimizado...")

    # 1. Obtener órdenes con información de convenio del cliente para calcular descuentos
    cursor.execute("""
        SELECT 
            ol.id_orden_lab, 
            ol.fecha_orden, 
            doe.id_examen,
            c.porcentaje_descuento
        FROM orden_laboratorio ol
        JOIN detalle_orden_examen doe ON ol.id_orden_lab = doe.id_orden_lab
        JOIN cliente cl ON ol.id_cliente = cl.id_cliente
        JOIN convenio c ON cl.id_convenio = c.id_convenio
    """)
    filas = cursor.fetchall()

    # Estructura para agrupar detalles por factura
    ordenes_procesadas = {}
    
    # 2. Agrupación y cálculo de precios
    for id_orden, fecha, id_ex, pct_descuento in filas:
        # Buscamos el precio del examen vigente a la fecha de la orden
        cursor.execute("""
            SELECT precio 
            FROM examen_precio 
            WHERE id_examen = ? AND ? BETWEEN fecha_inicio AND ISNULL(fecha_fin, '2099-12-31')
        """, (id_ex, fecha))
        
        res_precio = cursor.fetchone()
        precio_v = float(res_precio[0]) if res_precio else 50.0 # Precio base si no encuentra

        if id_orden not in ordenes_procesadas:
            ordenes_procesadas[id_orden] = {
                'fecha': fecha,
                'detalles': [],
                'subtotal_acumulado': 0.0,
                'descuento_acumulado': 0.0,
                'pct_conv': float(pct_descuento) / 100
            }
        
        # Cálculo por línea (examen)
        monto_descuento_linea = precio_v * ordenes_procesadas[id_orden]['pct_conv']
        subtotal_linea = precio_v - monto_descuento_linea
        
        # Guardamos id_ex para el nuevo detalle_factura
        ordenes_procesadas[id_orden]['detalles'].append((precio_v, monto_descuento_linea, subtotal_linea, id_ex))
        
        # Acumuladores de la cabecera
        ordenes_procesadas[id_orden]['subtotal_acumulado'] += precio_v
        ordenes_procesadas[id_orden]['descuento_acumulado'] += monto_descuento_linea

    # 3. Inserción masiva
    id_factura_cont = 1
    id_det_fac_cont = 1
    facturas_batch = []
    detalles_f_batch = []

    estados = [1, 2, 3] # 1: Pagado, 2: Pendiente, 3: Anulado
    pesos_est = [0.85, 0.10, 0.05]
    metodos_pago = [1, 2, 3, 4] # Efectivo, QR, Tarjeta, Transferencia

    for id_orden, data in ordenes_procesadas.items():
        sub_total = data['subtotal_acumulado']
        tot_desc = data['descuento_acumulado']
        total_final = sub_total - tot_desc
        
        id_est = random.choices(estados, weights=pesos_est, k=1)[0]
        id_met = random.choice(metodos_pago)
        
        # INSERT FACTURA
        facturas_batch.append((
            id_factura_cont, data['fecha'], sub_total, tot_desc, total_final, id_est, id_orden, id_met
        ))

        for p_u, d_l, s_l, id_ex_fact in data['detalles']:
            # INSERT DETALLE_FACTURA (Ahora apunta a id_examen directamente)
            detalles_f_batch.append((
                id_det_fac_cont, p_u, d_l, s_l, id_factura_cont, id_ex_fact
            ))
            id_det_fac_cont += 1
        
        id_factura_cont += 1

        # Lotes de 1000 para no saturar la memoria ni la transacción
        if len(facturas_batch) >= 1000:
            cursor.executemany("INSERT INTO factura VALUES (?,?,?,?,?,?,?,?)", facturas_batch)
            cursor.executemany("INSERT INTO detalle_factura VALUES (?,?,?,?,?,?)", detalles_f_batch)
            con.commit()
            facturas_batch, detalles_f_batch = [], []
            print(f"Sincronizadas {id_factura_cont} facturas con sus detalles...")

    # Insertar el resto
    if facturas_batch:
        cursor.executemany("INSERT INTO factura VALUES (?,?,?,?,?,?,?,?)", facturas_batch)
        cursor.executemany("INSERT INTO detalle_factura VALUES (?,?,?,?,?,?)", detalles_f_batch)
        con.commit()

    con.close()
    print(f"--- Proceso finalizado: {id_factura_cont-1} facturas generadas correctamente ---")

if __name__ == "__main__":
    poblar_facturacion_masiva()