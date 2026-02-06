-- ejecutar despues de hacer poblado todo lo demas
SELECT MIN(id_cliente) as id_maestro, nombre
INTO #MaestrosEmpresas
FROM cliente
WHERE id_tipo_cliente <> 1 
GROUP BY nombre;
UPDATE ol
SET ol.id_cliente = m.id_maestro
FROM orden_laboratorio ol
JOIN cliente c ON ol.id_cliente = c.id_cliente
JOIN #MaestrosEmpresas m ON c.nombre = m.nombre
WHERE c.id_tipo_cliente <> 1;
DELETE FROM cliente
WHERE id_tipo_cliente <> 1
AND id_cliente NOT IN (SELECT id_maestro FROM #MaestrosEmpresas);
DROP TABLE #MaestrosEmpresas;