--Ejercicio hecho en PostgreSQL
--Muestra los datos del cliente solo en los casos en el que el importe es mayor a 100.000 en los ultimos 12 meses
select ct.id, ct.nombre, ct.apellido from clientes ct
left join ventas vt on vt.id_cliente = ct.id
where importe > '100000' and fecha >= current_date - 365


--Muestra los datos del cliente y las fechas e importe de las ventas, solo cuando el importe es mayor a 100.000 en los ultimos 12 meses
select vt.id_cliente, ct.nombre, ct.apellido, vt.fecha, vt.importe from clientes ct
left join ventas vt on vt.id_cliente = ct.id
where importe > '100000' and fecha >= current_date - 365
