--create database LabX2;
--use LabX2;

create table departamento( --listo
    id_departamento int primary key not null,
    nombre_departamento varchar(50) not null,
    sigla varchar(10) not null
);

create table provincia( --listo
    id_provincia int primary key not null,
    nombre_provincia varchar(50) not null,
    id_departamento int not null,
    foreign key (id_departamento) references departamento(id_departamento)
);
create table genero( --listo
    id_genero int primary key not null,
    nombre_genero varchar(20) not null
);

create table tipo_convenio( --listo
	id_tipo_convenio int primary key not null,
	nombre_tipo varchar(50),
	descripcion varchar(100)
);
create table convenio(--listo
    id_convenio int primary key not null,
    nombre_convenio varchar(50) not null,
    fecha_inicio date not null,
    fecha_fin date not null,
    porcentaje_descuento decimal(5,2) not null,
	id_tipo_convenio int not null,
	foreign key (id_tipo_convenio) references tipo_convenio (id_tipo_convenio)
);

create table tipo_cliente( --listo
    id_tipo_cliente int primary key not null,
    nombre_tipo_cliente varchar(30) not null
);

create table metodo_pago( --listo
    id_metodo_pago int primary key not null,
    nombre_metodo_pago varchar(30) not null
);

create table bioquimico( --listo
    id_bioquimico int primary key not null,
    nombre varchar(50) not null,
    apellidoP varchar(50) not null,
    apellidoM varchar(50) not null,
);



create table enfermedad( --listo
    id_enfermedad int primary key not null,
    nombre_enfermedad varchar(50) not null
);


create table recepcionista( --listo
    id_recepcionista int primary key not null,
    nombre varchar(50) not null,
    apellidoP varchar(50) not null,
    apellidoM varchar(50) not null,
    telefono varchar(15) not null
);

create table doctor( --listo
    id_doctor int primary key not null,
    nombre varchar(50) not null,
    apellidoP varchar(50) not null,
    apellidoM varchar(50) not null,
    telefono varchar(15) not null,
    email varchar(50) not null
);

create table tipo_muestra( --listo
    id_tipo_muestra int primary key not null,
    nombre_tipo_muestra varchar(30) not null
);

create table area( --listo
    id_area int primary key not null,
    nombre_area varchar(50) not null
);

create table cliente( -- metodo
    id_cliente int primary key not null,
    nombre varchar(50) not null,
    apellidoP varchar(50) not null,
    apellidoM varchar(50) not null,
    nit varchar(15) not null,
    email varchar(50) not null,
    telefono varchar(15) not null,
    id_tipo_cliente int not null,
    id_convenio int not null,
    foreign key (id_tipo_cliente) references tipo_cliente(id_tipo_cliente),
    foreign key (id_convenio) references convenio(id_convenio)
);

create table paciente( --metodo
    id_paciente int primary key not null,
    nombre varchar(50) not null,
    apellidoP varchar(50) not null,
    apellidoM varchar(50) not null,
    telefono varchar(15) not null,
    email varchar(50) not null,
    direccion varchar(100) not null,
    ci varchar(15) not null,
    id_genero int not null,
    id_provincia int not null,
    foreign key (id_genero) references genero(id_genero),
    foreign key (id_provincia) references provincia(id_provincia)
);

create table orden_laboratorio( --metodo
    id_orden_lab int primary key not null,
    fecha_orden date not null,
    estado varchar(20) not null,
    numero_orden int not null,
    id_paciente int not null,
    id_cliente int not null,
    id_doctor int not null,
    id_recepcionista int not null,
    foreign key (id_paciente) references paciente(id_paciente),
    foreign key (id_cliente) references cliente(id_cliente),
    foreign key (id_doctor) references doctor(id_doctor),
    foreign key (id_recepcionista) references recepcionista(id_recepcionista)
);

create table muestra( --metodo
    id_muestra int primary key not null,
    fecha_toma date not null,
    estado varchar(20) not null,
    observacion varchar(200),
    codigo_muestra varchar(30) not null,
    id_tipo_muestra int not null,
    foreign key (id_tipo_muestra) references tipo_muestra(id_tipo_muestra)
);

create table examen( --listo
    id_examen int primary key not null,
    nombre_examen varchar(50) not null,
    metodo varchar(100) not null,
    id_area int not null,
    foreign key (id_area) references area(id_area)
);

create table examen_precio( --metodo
    id_examen_precio int primary key not null,
    precio decimal(10,2) not null,
    fecha_inicio date not null,
    fecha_fin date,
    estado int not null, --1 activo, 0 inactivo
    id_examen int not null,
    foreign key (id_examen) references examen(id_examen)
);

create table examen_requisito_muestra( -- listo
    cantidad_requerida int not null,
    instrucciones_recoleccion varchar(200),
    recipiente varchar(50) not null,
    id_examen int not null,
    id_tipo_muestra int not null,
    primary key (id_examen, id_tipo_muestra),
    foreign key (id_examen) references examen(id_examen),
    foreign key (id_tipo_muestra) references tipo_muestra(id_tipo_muestra)
);





create table parametro( --listo
    id_parametro int primary key not null,
    nombre_parametro varchar(50) not null,
    descripcion varchar(200),
    id_examen int not null,
    foreign key (id_examen) references examen(id_examen)
);

create table valor_referencia( --listo
    id_valor_ref int primary key not null,
    descripcion varchar(200) not null,
    rango_minimo decimal(10,2) not null,
    rango_maximo decimal(10,2) not null,
    unidad_medida varchar(20) not null,
    id_parametro int not null,
    foreign key (id_parametro) references parametro(id_parametro)
);



create table estado_factura( --listo
    id int primary key not null,
    nombre varchar(30) not null,
    descripcion varchar(100)
);

create table factura( --metodo
    id_factura int primary key not null,
    fecha_emision date not null,
    subtotal_total decimal(10,2) not null, --suma de los precios sin descuento
    total_descuento decimal(10,2) not null, --monto descontado-lo que se ahorra el cliente
    total_a_pagar decimal(10,2) not null, --lo que el cliente realmente paga
    id_estado int not null, 
    id_orden_lab int not null,
    id_metodo_pago int not null,
    foreign key (id_estado) references estado_factura(id),
    foreign key (id_orden_lab) references orden_laboratorio(id_orden_lab),
    foreign key (id_metodo_pago) references metodo_pago(id_metodo_pago)
);


create table detalle_orden_examen( --metodo
    id_detalle_orden_examen int primary key not null,
    id_orden_lab int not null,
    id_examen int not null,
    id_muestra int not null,
    foreign key (id_muestra) references muestra(id_muestra),
    foreign key (id_orden_lab) references orden_laboratorio(id_orden_lab),
    foreign key (id_examen) references examen(id_examen)
);

create table resultado( --metodo
    id_resultado int primary key not null,
    fecha date not null,
    id_bioquimico int not null,
    id_detalle_orden_examen int not null,
    foreign key (id_bioquimico) references bioquimico(id_bioquimico),
    foreign key (id_detalle_orden_examen) references detalle_orden_examen(id_detalle_orden_examen)
);

create table hallazgo_diagnostico( --metodo
    descripcion varchar(200) not null,
    id_enfermedad int not null,
    id_resultado int not null,
    primary key (id_enfermedad, id_resultado),
    foreign key (id_enfermedad) references enfermedad(id_enfermedad),
    foreign key (id_resultado) references resultado(id_resultado)
);

create table detalle_resultado( --metodo
    id_detalle_resultado int primary key not null,
    valor_obtenido varchar(100) not null,
    unidad_medida varchar(20) not null,
    id_parametro int not null,
    id_valor_ref int not null,
    id_resultado int not null,
    foreign key (id_parametro) references parametro(id_parametro),
    foreign key (id_valor_ref) references valor_referencia(id_valor_ref),
    foreign key (id_resultado) references resultado(id_resultado)
);

create table detalle_factura( --metodo
    id_detalle_factura int primary key not null,
    precio_unitario decimal(10,2) not null, -- el precio de la table examen hpy
    descuento_linea decimal(10,2) not null, -- el descuento calculado hoy
    subtotal_linea decimal(10,2) not null, -- (precio unitario * cantidad) - descuento
    id_factura int not null,
    id_examen int not null,
    foreign key (id_examen) references examen(id_examen),
    foreign key (id_factura) references factura(id_factura)
);
