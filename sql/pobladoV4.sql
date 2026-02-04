--use LabX2

insert into departamento (id_departamento, nombre_departamento, sigla) values 
(1, 'Santa Cruz', 'SC'),
(2, 'La Paz', 'LP'),
(3, 'Cochabamba', 'CB'),
(4, 'Oruro', 'OR'),
(5, 'Potosí', 'PT'),
(6, 'Tarija', 'TJ'),
(7, 'Chuquisaca', 'CH'),
(8, 'Beni', 'BN'),
(9, 'Pando', 'PA');

insert into provincia (id_provincia, nombre_provincia, id_departamento) values
--sc
(1, 'Andrés Ibáñez', 1),
(2, 'Ignacio Warnes', 1),
(3, 'José Miguel de Velasco', 1),
(4, 'Ichilo', 1),
(5, 'Chiquitos', 1),
(6, 'Sara', 1),
(7, 'Cordillera', 1),
(8, 'Vallegrande', 1),
(9, 'Florida', 1),
(10, 'Obispo Santistevan', 1),
(11, 'Ñuflo de Chávez', 1),
(12, 'Ángel Sandoval', 1),
(13, 'Manuel María Caballero', 1),
(14, 'Germán Busch', 1),
(15, 'Guarayos', 1),
--lp
(16, 'Aroma', 2),
(17, 'Bautista Saavedra', 2),
(18, 'Abel Iturralde', 2),
(19, 'Caranavi', 2),
(20, 'Eliodoro Camacho', 2),
(21, 'Franz Tamayo', 2),
(22, 'Gualberto Villarroel', 2),
(23, 'Ingavi', 2),
(24, 'Inquisivi', 2),
(25, 'José Manuel Pando', 2),
(26, 'Larecaja', 2),
(27, 'Loayza', 2),
(28, 'Los Andes', 2),
(29, 'Manco Kapac', 2),
(30, 'Muñecas', 2),
(31, 'Nor Yungas', 2),
(32, 'Omasuyos', 2),
(33, 'Pacajes', 2),
(34, 'Pedro Domingo Murillo', 2),
(35, 'Sud Yungas', 2),
--cbba
(36, 'Arani', 3),
(37, 'Arque', 3),
(38, 'Ayopaya', 3),
(39, 'Bolívar', 3),
(40, 'Capinota', 3),
(41, 'Carrasco', 3),
(42, 'Cercado', 3),
(43, 'Chapare', 3),
(44, 'Esteban Arce', 3),
(45, 'Germán Jordán', 3),
(46, 'Mizque', 3),
(47, 'Narciso Campero', 3),
(48, 'Punata', 3),
(49, 'Quillacollo', 3),
(50, 'Tapacarí', 3),
(51, 'Tiraque', 3),
--or
(52, 'Cercado', 4),
(53, 'Eduardo Avaroa', 4),
(54, 'Ladislao Cabrera', 4),
(55, 'Litoral de Atacama', 4),
(56, 'Nor Carangas', 4),
(57, 'Pantaléon Dalence', 4),
(58, 'Carangas', 4),
(59, 'Sajama', 4),
(60, 'San Pedro de Totora', 4),
(61, 'Saucarí', 4),
(62, 'Sebastián Pagador', 4),
(63, 'Sud Carangas', 4),
(64, 'Tomas Barrón', 4),
(65, 'Sabaya', 4),
(66, 'Santiago de Huari', 4),
--pt
(67, 'Alonso de Ibáñez', 5),
(68, 'Antonio Quijarro', 5),
(70, 'Bernardino Bilbao', 5),
(71, 'Charcas', 5),
(72, 'Chayanta', 5),
(73, 'Cornelio Saavedra', 5),
(74, 'Daniel Campos', 5),
(75, 'Enrique Baldivieso', 5),
(76, 'José María Linares', 5),
(77, 'Modesto Omiste', 5),
(78, 'Nor Chichas', 5),
(79, 'Nor Lípez', 5),
(80, 'Rafael Bustillo', 5),
(81, 'Sud Chichas', 5),
(82, 'Sud Lípez', 5),
(83, 'Tomás Frías', 5),
--tj
(84, 'Aniceto Arce', 6),
(85, 'Burdet O''Connor', 6),
(86, 'Cercado', 6),
(87, 'Eustaquio Méndez', 6),
(88, 'Gran Chaco', 6),
(89, 'José María Avilés', 6),
--ch
(90, 'Belisario Boeto', 7),
(91, 'Hernando Siles', 7),
(92, 'Jaime Zudáñez', 7),
(93, 'Luis Calvo', 7),
(94, 'Nor Cinti', 7),
(95, 'Oropeza', 7),
(96, 'Sud Cinti', 7),
(97, 'Tomina', 7),
(98, 'Yamparáez', 7),
(99, 'Juana Azurduy de Padilla', 7),
--bn
(100, 'Cercado', 8),
(101, 'Vaca Díez', 8),
(102, 'José Ballivián', 8),
(103, 'Yacuma', 8),
(104, 'Moxos', 8),
(105, 'Marbán', 8),
(106, 'Mamoré', 8),
(107, 'Iténez', 8),
--pa
(108, 'Abuná', 9),
(109, 'Federico Román', 9),
(110, 'Madre de Dios', 9),
(111, 'Manuripi', 9),
(112, 'Nicolás Suárez', 9);

insert into genero values
(1,'Masculino'), (2, 'Femenino');

insert into tipo_convenio values 
(1, 'PARTICULAR', 'Clientes sin afiliación que pagan precio de lista'),
(2, 'SEGURO MEDICO', 'Aseguradoras privadas y Cajas de Salud nacionales'),
(3, 'EMPRESARIAL', 'Convenios con empresas para beneficios de empleados'),
(4, 'SOCIAL / CAMPAÑA', 'Campañas de salud temporales o descuentos solidarios'),
(5, 'INTERNO', 'Descuentos para personal, socios o proveedores');

INSERT INTO convenio (id_convenio, nombre_convenio, porcentaje_descuento, fecha_inicio, fecha_fin, id_tipo_convenio)
VALUES 
(1, 'PARTICULAR', 0.00, '2020-01-01', '2099-12-31', 1),
(2, 'CAJA PETROLERA DE SALUD', 25.00, '2025-01-01', '2026-12-31', 2),
(3, 'BISA SEGUROS', 20.00, '2025-01-01', '2025-12-31', 2),
(4, 'YPFB TRANSPORTE', 15.00, '2025-05-01', '2026-05-01', 3),
(5, 'CAMPAÑA PREVENTIVA 2026', 30.00, '2026-02-01', '2026-03-31', 4);

insert into tipo_cliente values
(1, 'PERSONA NATURAL'),
(2, 'ASEGURADORA / CAJA DE SALUD'),
(3, 'EMPRESA PRIVADA'),
(4, 'INSTITUCION PUBLICA'),
(5, 'LABORATORIO EXTERNO');

insert into doctor values 
(1, 'MARCO', 'ANTONIO', 'SUAREZ', '70011223', 'm.suarez@medico.bo'),
(2, 'CARLA', 'PATRICIA', 'MENDOZA', '71022334', 'c.mendoza@clinica.com'),
(3, 'RICARDO', 'DANIEL', 'ORTIZ', '72033445', 'r.ortiz@hospital.bo'),
(4, 'MARIA', 'ELENA', 'VARGAS', '73044556', 'm.vargas@medica.bo'),
(5, 'LUIS', 'FERNANDO', 'ROJAS', '74055667', 'l.rojas@consulta.com'),
(6, 'ANA', 'LUCIA', 'GUZMAN', '75066778', 'a.guzman@med.bo'),
(7, 'JORGE', 'ALBERTO', 'ZABALA', '76077889', 'j.zabala@clinica.bo'),
(8, 'PAOLA', 'ANDREA', 'JUSTINIANO', '77088990', 'p.justiniano@medico.bo'),
(9, 'SERGIO', 'ANDRES', 'SALVATIERRA', '78099001', 's.salvatierra@hospital.com'),
(10, 'BEATRIZ', 'RAQUEL', 'VALDEZ', '79011223', 'b.valdez@medica.bo');

insert into recepcionista values
(1, 'ANDREA', 'SOLIZ', 'RIVERO', '70014521'),
(2, 'CARLOS', 'Heredia', 'Justiniano', '71025896'),
(3, 'MARIANA', 'VACA', 'Pinto', '72036987'),
(4, 'JORGE', 'ZURITA', 'CLAROS', '73047852'),
(5, 'CLAUDIA', 'MENDEZ', 'ARCE', '74058963'),
(6, 'ROBERTO', 'Vaca', 'Dorado', '75069874'),
(7, 'FABIOLA', 'TERRAZAS', 'Salvatierra', '76014725'),
(8, 'DIEGO', 'CHAVEZ', 'Morales', '77025814'),
(9, 'NATALIA', 'ROCA', 'Zabala', '78036925');

insert into estado_factura values
(1, 'EMITIDA / PAGADA', 'Factura cobrada exitosamente al contado.'),
(2, 'PENDIENTE', 'Factura registrada pero pendiente de cobro.'),
(3, 'ANULADA', 'Factura cancelada por error en datos o servicios.'),
(4, 'CREDITO', 'Monto enviado a cuentas por cobrar para empresas o aseguradoras.');

insert into metodo_pago values
(1, 'Efectivo'), (2, 'Tranferencia'), (3,'QR'), (4, 'Tarjeta');

insert into area values
(1, 'HEMATOLOGIA'),
(2, 'QUIMICA SANGUINEA'),
(3, 'SEROLOGIA / INMUNOLOGIA'),
(4, 'COPROLOGIA'),
(5, 'UROANALISIS'),
(6, 'BACTERIOLOGIA / MICROBIOLOGIA'),
(7, 'HORMONAS'),
(8, 'MARCADORES TUMORALES'),
(9, 'TOXICOLOGIA'),
(10, 'BIOLOGIA MOLECULAR');

insert into examen values 
--hematologia
(1, 'HEMOGRAMA COMPLETO', 'CITOMETRIA DE FLUJO / MICROSCOPIA', 1),
(2, 'GRUPO SANGUINEO Y FACTOR RH', 'AGLUTINACION EN PLACA/TUBO', 1),
(3, 'RECUENTO DE RETICULOCITOS', 'COLORACION SUPRAVITAL / MANUAL', 1),
(4, 'TIEMPO DE PROTROMBINA (TP)', 'COAGULOMETRIA AUTOMATIZADA', 1),
(5, 'VELOCIDAD DE ERITROSEDIMENTACION (VSG)', 'METODO WESTERGREN', 1),
(6, 'FROTIS DE SANGRE PERIFERICA', 'COLORACION WRIGHT / MICROSCOPIA', 1),
(7, 'RECUENTO DE PLAQUETAS', 'IMPEDANCIA ELECTRICA / MANUAL', 1),
(8, 'HEMOGLOBINA GLICOSILADA (HBA1C)', 'HPLC / INMUNOENSAYO', 1),
--quimica sanquinea
(9, 'GLICEMIA EN AYUNAS', 'ENZIMATICO COLORIMETRICO', 2),
(10, 'CREATININA', 'JAFE CINETICO', 2),
(11, 'UREA', 'UV ENZIMATICO', 2),
(12, 'ACIDO URICO', 'URICASA - POD', 2),
(13, 'COLESTEROL TOTAL', 'CHOD - PAP', 2),
(14, 'TRIGLICERIDOS', 'GPO - PAP', 2),
(15, 'TRANSAMINASA TGO (AST)', 'IFCC SIN PIRIDOXAL FOSFATO', 2),
(16, 'BILIRRUBINAS (TOTAL, DIRECTA, INDIRECTA)', 'JENDRASSIK - GROF', 2),
-- serologia / inmunologia
(17, 'WIDAL (SALMONELLAS)', 'AGLUTINACION DIRECTA', 3),
(18, 'PRUEBA RAPIDA H. PYLORI (ANTICUERPOS)', 'INMUNOCROMATOGRAFIA', 3),
(19, 'VDRL (SIFILIS)', 'FLOCULACION', 3),
(20, 'CHAGAS (ELISA)', 'ELISA', 3),
(21, 'TOXOPLASMOSIS IGG / IGM', 'QUIMIOLUMINISCENCIA', 3),
(22, 'FACTOR REUMATOIDEO (RA TEST)', 'AGLUTINACION DE LATEX', 3),
(23, 'DENGUE NS1 / IGG - IGM', 'INMUNOCROMATOGRAFIA', 3),
(24, 'VIH 1/2 (PRUEBA RAPIDA)', 'INMUNOCROMATOGRAFIA', 3),
(25, 'ASTO (ANTIESTREPTOLISINA O)', 'AGLUTINACION DE LATEX', 3),
--COPROLOGIA
(26, 'EXAMEN COPROPARASITOLOGICO SIMPLE', 'MICROSCOPIA DIRECTA', 4),
(27, 'MOCO FECAL (CITOLOGIA FECAL)', 'COLORACION WRIGHT / MICROSCOPIA', 4),
(28, 'SANGRE OCULTA EN HECES', 'INMUNOCROMATOGRAFIA', 4),
--UROANALISIS
(29, 'EXAMEN GENERAL DE ORINA (EGO)', 'FISICO - QUIMICO - SEDIMENTO', 5),
(30, 'PRUEBA DE EMBARAZO EN ORINA (HCG)', 'INMUNOCROMATOGRAFIA', 5),
(31, 'PROTEINURIA DE 24 HORAS', 'TURBIDIMETRICO / COLORIMETRICO', 5),
-- BACTERIOLOGIA / MICROBIOLOGIA
(32, 'UROCULTIVO Y ANTIBIOGRAMA', 'SIEMBRA EN MEDIOS SELECTIVOS', 6),
(33, 'CULTIVO DE SECRECION (FARINGEO/HERIDA)', 'SIEMBRA Y PRUEBAS BIOQUIMICAS', 6),
(34, 'TINCION GRAM', 'COLORACION DIFERENCIAL / MICROSCOPIA', 6),
--HORMONAS
(35, 'TSH (HORMONA ESTIMULANTE DE TIROIDES)', 'QUIMIOLUMINISCENCIA', 7),
(36, 'T4 LIBRE (TIROXINA LIBRE)', 'QUIMIOLUMINISCENCIA', 7),
(37, 'T3 TOTAL (TRIYODOTIRONINA)', 'QUIMIOLUMINISCENCIA', 7),
(38, 'B-HCG CUANTITATIVA (PRUEBA DE EMBARAZO EN SANGRE)', 'QUIMIOLUMINISCENCIA', 7),
(39, 'PROLACTINA', 'QUIMIOLUMINISCENCIA', 7),
(40, 'INSULINA EN AYUNAS', 'QUIMIOLUMINISCENCIA', 7),
--MARCADORES TUMORALES
(41, 'PSA TOTAL (ANTIGENO PROSTATICO ESPECIFICO)', 'QUIMIOLUMINISCENCIA', 8),
(42, 'CEA (ANTIGENO CARCINOEMBRIONARIO)', 'QUIMIOLUMINISCENCIA', 8),
(43, 'ALFAFETOPROTEINA (AFP)', 'QUIMIOLUMINISCENCIA', 8),
(44, 'CA-125 (MARCADOR DE OVARIO)', 'QUIMIOLUMINISCENCIA', 8),
--TOXICOLOGIA
(45, 'COCAINA EN ORINA', 'INMUNOCROMATOGRAFIA', 9),
(46, 'MARIHUANA (THC) EN ORINA', 'INMUNOCROMATOGRAFIA', 9),
(47, 'ALCOHOLEMIA EN SANGRE', 'METODO QUIMICO / ENZIMATICO', 9),
(48, 'DOSAJE DE PLOMO EN SANGRE', 'ABSORCION ATOMICA', 9),
--BIOLOGIA MOLECULAR
(49, 'RT-PCR PARA COVID-19', 'PCR EN TIEMPO REAL', 10),
(50, 'CARGA VIRAL VIH-1', 'PCR CUANTITATIVA', 10),
(51, 'DETECCION DE VPH (VIRUS PAPILOMA HUMANO)', 'CAPTURA HIBRIDA / PCR', 10),
(52, 'PRUEBA DE PATERNIDAD (DNA)', 'ANALISIS DE STR (MICROSATELITES)', 10);

insert into enfermedad values 
(1, 'DIABETES MELLITUS TIPO 2'),
(2, 'ANEMIA FERROPENICA'),
(3, 'HIPOTIROIDISMO PRIMARIO'),
(4, 'HIPERCOLESTEROLEMIA PURA'),
(5, 'HEPATITIS VIRAL AGUDA'),
(6, 'INFECCION DE VIAS URINARIAS (IVU)'),
(7, 'FIEBRE TIFOIDEA'),
(8, 'DENGUE CON SIGNOS DE ALARMA'),
(9, 'GASTRITIS POR HELICOBACTER PYLORI'),
(10, 'AMIBIASIS INTESTINAL'),
(11, 'CRISIS HIPERGLUCEMICA (CETOACIDOSIS)'),
(12, 'SINDROME ANEMICO SEVERO'),
(13, 'INSUFICIENCIA HEPATICA'),
(14, 'POLICITEMIA VERA (SANGRE ESPESA)'),
(15, 'HIPERURICEMIA (ACIDO URICO ALTO)'),
(16, 'SINDROME NEFROTICO'),
(17, 'CHAGAS CRONICO'),
(18, 'ARTRITIS REUMATOIDE'),
(19, 'SINDROME DE OVARIO POLIQUISTICO (SOP)'),
(20, 'INTOXICACION POR METALES PESADOS');

-- PARAMETROS PARA HEMATOLOGIA (id_examen 1-8)
INSERT INTO parametro (id_parametro, nombre_parametro, id_examen) VALUES
(1, 'Recuento de Glóbulos Rojos', 1),
(2, 'Hemoglobina', 1),
(3, 'Hematocrito', 1), 
(4, 'Volumen Corpuscular Medio (VCM)', 1),
(5, 'Leucocitos Totales', 1),
(6, 'Segmentados', 1),
(7, 'Linfocitos', 1),
(8, 'Monocitos', 1),
(9, 'Eosinofilos', 1),
(10, 'Basofilos', 1),
(11, 'Grupo Sanguíneo', 2),
(12, 'Factor Rh', 2),
(13, 'Porcentaje de Reticulocitos', 3),
(14, 'Tiempo del Paciente (Seg)', 4),
(15, 'Actividad (Porcentaje)', 4),
(16, 'INR', 4),
(17, 'VSG 1era Hora', 5),
(18, 'Serie Roja (Observaciones)', 6),
(19, 'Serie Blanca (Observaciones)', 6),
(20, 'Recuento de Plaquetas', 7),
(21, 'Porcentaje HbA1c', 8),
-- PARAMETROS PARA QUIMICA SANGUINEA (id_examen 9-16)
(22, 'Glucosa en ayunas', 9),
(23, 'Creatinina sérica', 10),
(24, 'Urea sérica', 11),
(25, 'Ácido Úrico', 12),
(26, 'Colesterol Total', 13),
(27, 'Triglicéridos', 14),
(28, 'Transaminasa TGO/AST', 15),
(29, 'Bilirrubina Total', 16), (30, 'Bilirrubina Directa', 16), (31, 'Bilirrubina Indirecta', 16),
-- PARAMETROS PARA SEROLOGIA (id_examen 17-25)
(32, 'Antígeno O (Tifico)', 17), (33, 'Antígeno H (Tifico)', 17),
(34, 'Resultado H. Pylori', 18),
(35, 'Resultado VDRL', 19), (36, 'Títulos (Dilusiones)', 19),
(37, 'Resultado Chagas ELISA', 20), (38, 'Valor de Cut-off', 20),
(39, 'Toxoplasmosis IgG', 21), (40, 'Toxoplasmosis IgM', 21),
(41, 'Factor Reumatoideo', 22),
(42, 'Dengue NS1', 23), (43, 'Dengue IgG', 23), (44, 'Dengue IgM', 23),
(45, 'Resultado VIH', 24),
(46, 'Títulos ASTO', 25),
-- PARAMETROS PARA COPROLOGIA Y UROANALISIS (id_examen 26-31)
(47, 'Color/Consistencia', 26), (48, 'Examen Directo (Quistes/Huevos)', 26),
(49, 'Leucocitos en Heces', 27), (50, 'Eritrocitos en Heces', 27),
(51, 'Sangre Oculta', 28),
(52, 'Examen Físico (Color/Olor)', 29), (53, 'Examen Químico (Densidad/pH)', 29), (54, 'Sedimento (Células/Bacterias)', 29),
(55, 'HCG Cualitativo', 30),
(56, 'Proteínas Totales/24h', 31), (57, 'Volumen Urinario', 31),
-- PARAMETROS BACTERIOLOGIA Y HORMONAS (id_examen 32-40)
(58, 'Recuento de Colonias (UFC)', 32), (59, 'Microorganismo Aislado', 32), (60, 'Antibiograma', 32),
(61, 'Resultado Cultivo', 33),
(62, 'Resultado Gram', 34),
(63, 'Concentración TSH', 35),
(64, 'Concentración T4 Libre', 36),
(65, 'Concentración T3 Total', 37),
(66, 'B-HCG Cuantitativa', 38),
(67, 'Concentración Prolactina', 39),
(68, 'Insulina Basal', 40),
-- MARCADORES, TOXICOLOGIA Y MOL. MOLECULAR (id_examen 41-52)
(69, 'PSA Total', 41), (70, 'Marcador CEA', 42), (71, 'AFP Valor', 43), (72, 'Marcador CA-125', 44),
(73, 'Cocaína', 45), (74, 'Marihuana (THC)', 46), (75, 'Alcohol Sangre', 47), (76, 'Nivel Plomo', 48),
(77, 'PCR COVID-19', 49), (78, 'Carga Viral (Copias)', 50), (79, 'VPH Tipificación', 51), (80, 'Índice de Paternidad', 52);

insert into tipo_muestra values 
(1, 'SANGRE TOTAL'),
(2, 'SUERO SANGUINEO'),
(3, 'PLASMA ANTICOAGULANTE'),
(4, 'ORINA DE CHORRO MEDIO'),
(5, 'ORINA DE 24 HORAS'),
(6, 'MATERIA FECAL'),
(7, 'SECRECION FARINGEA'),
(8, 'SECRECION VAGINAL'),
(9, 'LIQUIDO CEFALORRAQUIDEO (LCR)'),
(10, 'HISOPADO NASOFARINGEO');

insert into examen_requisito_muestra(id_examen, id_tipo_muestra, cantidad_requerida, instrucciones_recoleccion, recipiente)
values
-- 1. HEMOGRAMA COMPLETO
(1, 1, 3, 'Ayuno de 8 horas. Evitar ejercicio físico intenso 24h antes.', 'Tubo Tapón Lila (EDTA)'),

-- 2. GRUPO SANGUINEO Y FACTOR RH
(2, 1, 2, 'No requiere ayuno estricto.', 'Tubo Tapón Lila (EDTA)'),

-- 3. RECUENTO DE RETICULOCITOS
(3, 1, 3, 'Ayuno de 8 horas.', 'Tubo Tapón Lila (EDTA)'),

-- 4. TIEMPO DE PROTROMBINA (TP)
(4, 3, 3, 'Ayuno de 8 horas.', 'Tubo Tapón Azul (Citrato)'),

-- 5. VELOCIDAD DE ERITROSEDIMENTACION (VSG)
(5, 1, 3, 'Ayuno de 8 horas. Muestra debe procesarse antes de las 2 horas de toma.', 'Tubo Tapón Negro o Lila'),

-- 6. FROTIS DE SANGRE PERIFERICA
(6, 1, 2, 'No requiere ayuno. Muestra fresca para evitar artefactos celulares.', 'Tubo Tapón Lila (EDTA)'),

-- 7. RECUENTO DE PLAQUETAS
(7, 1, 3, 'Ayuno de 8 horas. No consumir aspirina o antiagregantes 3 días antes.', 'Tubo Tapón Lila (EDTA)'),

-- 8. HEMOGLOBINA GLICOSILADA (HBA1C)
(8, 1, 2, 'No requiere ayuno estricto.', 'Tubo Tapón Lila (EDTA)'),
--- 
-- 9. GLICEMIA EN AYUNAS
(9, 2, 5, 'Ayuno estricto de 8 a 12 horas. No ingerir chicles ni café.', 'Tubo Tapón Rojo (Seco)'),

-- 10. CREATININA
(10, 2, 5, 'Ayuno de 8 horas. Evitar consumo excesivo de carne roja 24h antes.', 'Tubo Tapón Rojo (Seco)'),

-- 11. UREA
(11, 2, 5, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo (Seco)'),

-- 12. ACIDO URICO
(12, 2, 5, 'Ayuno de 8 horas. Evitar bebidas alcohólicas 24h antes.', 'Tubo Tapón Rojo (Seco)'),

-- 13. COLESTEROL TOTAL
(13, 2, 5, 'Ayuno de 12 horas. Cena liviana la noche anterior.', 'Tubo Tapón Rojo o Amarillo'),

-- 14. TRIGLICERIDOS
(14, 2, 5, 'Ayuno estricto de 12 a 14 horas. No consumir alcohol 72h antes.', 'Tubo Tapón Rojo o Amarillo'),

-- 15. TRANSAMINASA TGO (AST)
(15, 2, 5, 'Ayuno de 8 horas. Evitar ejercicio físico intenso antes de la toma.', 'Tubo Tapón Rojo (Seco)'),

-- 16. BILIRRUBINAS (TOTAL, DIRECTA, INDIRECTA)
(16, 2, 5, 'Ayuno de 8 horas. Proteger la muestra de la luz (fotosensible).', 'Tubo Tapón Rojo (Seco)'),

(17, 2, 5, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo'), -- Widal
(18, 2, 3, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo'), -- H. Pylori
(19, 2, 3, 'No requiere ayuno.', 'Tubo Tapón Rojo'), -- VDRL
(20, 2, 5, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo'), -- Chagas
(21, 2, 5, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo'), -- Toxoplasmosis
(22, 2, 3, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo'), -- Factor Reumatoideo
(23, 2, 5, 'Indicar días de síntomas.', 'Tubo Tapón Rojo'), -- Dengue
(24, 2, 3, 'No requiere ayuno.', 'Tubo Tapón Rojo'), -- VIH
(25, 2, 3, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo'), -- ASTO
-- 26. EXAMEN COPROPARASITOLOGICO SIMPLE
(26, 6, 20, 'Muestra del tamaño de una nuez. Evitar contaminar con orina o agua. Entregar antes de las 2 horas.', 'Frasco para Heces (Limpio)'),

-- 27. MOCO FECAL (CITOLOGIA FECAL)
(27, 6, 20, 'Muestra reciente. No usar laxantes ni supositorios antes de la toma.', 'Frasco para Heces (Limpio)'),

-- 28. SANGRE OCULTA EN HECES
(28, 6, 20, 'No ingerir carnes rojas, embutidos o vitamina C 3 días antes del examen.', 'Frasco para Heces (Limpio)'),
-- 29. EXAMEN GENERAL DE ORINA (EGO)
(29, 4, 50, 'Primera orina de la mañana. Descartar el primer chorro y recolectar el medio en frasco limpio.', 'Frasco para Orina (50-100 mL)'),

-- 30. PRUEBA DE EMBARAZO EN ORINA (HCG)
(30, 4, 20, 'Preferible la primera orina de la mañana por mayor concentración de la hormona.', 'Frasco para Orina (Limpio)'),

-- 31. PROTEINURIA DE 24 HORAS
(31, 5, 2000, 'Recolectar TODA la orina de 24 horas en un bidón, descartando la primera del primer día.', 'Bidón / Recolector de 2 a 3 Litros'),

-- 32. UROCULTIVO Y ANTIBIOGRAMA
(32, 4, 30, 'Aseo genital riguroso. Chorro medio en frasco estéril. No estar bajo tratamiento antibiótico (mínimo 3 días).', 'Frasco Estéril (Sellado)'),

-- 33. CULTIVO DE SECRECION (FARINGEO/HERIDA)
(33, 7, 1, 'Faringeo: En ayunas, sin aseo bucal. Herida: Limpieza previa con solución salina si hay costra.', 'Hisopo con Medio de Transporte (Stuart/Amies)'),

-- 34. TINCION GRAM
(34, 7, 1, 'Muestra tomada directamente de la zona de sospecha de infección.', 'Portaobjetos o Hisopo Estéril'),

-- 35. TSH (TIROIDES)
(35, 2, 5, 'Ayuno de 8 horas. Muestra debe tomarse preferentemente antes de las 10:00 AM.', 'Tubo Tapón Rojo/Amarillo'),

-- 36. T4 LIBRE
(36, 2, 5, 'Ayuno de 8 horas. Informar si toma medicación para la tiroides (Levotiroxina).', 'Tubo Tapón Rojo/Amarillo'),

-- 37. T3 TOTAL
(37, 2, 5, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo/Amarillo'),

-- 38. B-HCG CUANTITATIVA (EMBARAZO EN SANGRE)
(38, 2, 3, 'No requiere ayuno. Útil para determinar semanas de gestación.', 'Tubo Tapón Rojo/Amarillo'),

-- 39. PROLACTINA
(39, 2, 5, 'Ayuno de 8 horas. Paciente debe estar en reposo 20-30 min antes de la toma. Evitar estrés.', 'Tubo Tapón Rojo/Amarillo'),

-- 40. INSULINA EN AYUNAS
(40, 2, 5, 'Ayuno estricto de 8 a 10 horas. No realizar ejercicio previo.', 'Tubo Tapón Rojo/Amarillo'),

-- 1. MARCADORES TUMORALES (Suero - ID 2)
(41, 2, 5, 'Abstinencia sexual 48h. No realizar ejercicio intenso ni tacto rectal 3 días antes.', 'Tubo Tapón Rojo/Amarillo'), -- PSA Total
(42, 2, 5, 'No requiere ayuno estricto. Informar si el paciente es fumador (eleva niveles).', 'Tubo Tapón Rojo/Amarillo'), -- CEA
(43, 2, 5, 'Ayuno de 8 horas.', 'Tubo Tapón Rojo/Amarillo'), -- AFP
(44, 2, 5, 'No realizar durante el periodo menstrual.', 'Tubo Tapón Rojo/Amarillo'), -- CA-125

-- 2. TOXICOLOGÍA (Orina y Sangre - IDs 4, 1, 2)
(45, 4, 30, 'Recolección bajo vigilancia directa del personal (Cadena de Custodia).', 'Frasco para Orina'), -- Cocaina
(46, 4, 30, 'Recolección bajo vigilancia directa del personal (Cadena de Custodia).', 'Frasco para Orina'), -- Marihuana
(47, 1, 5, 'No limpiar la zona de punción con alcohol o pañitos alcoholizados.', 'Tubo Tapón Gris o Rojo'), -- Alcoholemia
(48, 1, 5, 'Evitar exposición a fuentes de contaminación 24h antes.', 'Tubo Tapón Lila (EDTA)'), -- Plomo
-- 49. RT-PCR PARA COVID-19
(49, 10, 1, 'No aplicar medicamentos nasales 24h antes. Hisopado profundo de nasofaringe.', 'Tubo con Medio de Transporte Viral'),

-- 50. CARGA VIRAL VIH-1
(50, 1, 5, 'Ayuno de 8 horas. La muestra debe centrifugarse y congelarse antes de las 6 horas.', 'Tubo Tapón Lila (EDTA)'),

-- 51. DETECCION DE VPH (VIRUS PAPILOMA HUMANO)
(51, 8, 1, 'No estar en periodo menstrual. No tener relaciones sexuales 48h antes ni usar óvulos.', 'Tubo con Solución Preservante (Base Líquida)'),

-- 52. PRUEBA DE PATERNIDAD (DNA)
(52, 1, 3, 'Identificación oficial de todos los involucrados. Cadena de custodia estricta.', 'Tubo Tapón Lila (EDTA) o Hisopo Bucal');

insert into bioquimico values 
(1, 'Marcos', 'Vaca', 'Pinto'),
(2, 'Elena', 'Rojas', 'Mendez'),
(3, 'Ricardo', 'Suarez', 'Justiniano'),
(4, 'Claudia', 'Paz', 'Soldan'),
(5, 'Jorge', 'Saucedo', 'Arrien'),
(6, 'Mariela', 'Terrazas', 'Soto'),
(7, 'Carlos', 'Heredia', 'Guzman'),
(8, 'Paola', 'Zabala', 'Castillo'),
(9, 'Fernando', 'Ribera', 'Chavez'),
(10, 'Silvia', 'Antelo', 'Dorado'),
(11, 'Hugo', 'Banzer', 'Luz'),
(12, 'Monica', 'Cuellar', 'Tellez'),
(13, 'Ramiro', 'Velasco', 'Melgar'),
(14, 'Tatiana', 'Mendoza', 'Balcazar'),
(15, 'Andrés', 'Soliz', 'Peinado'),
(16, 'Patricia', 'Aguilera', 'Justiniano'),
(17, 'Gustavo', 'Arteaga', 'Landivar'),
(18, 'Lorena', 'Camacho', 'Villarroel'),
(19, 'Oscar', 'Ortiz', 'Gutiérrez'),
(20, 'Beatriz', 'Peralta', 'Torrico');

insert into valor_referencia(id_valor_ref, descripcion, rango_minimo, rango_maximo, unidad_medida, id_parametro)
values 
-- Hemoglobina (ID 2)
(1, 'Mujeres Adultas', 12.00, 16.00, 'g/dL', 2),
(2, 'Varones Adultos', 13.50, 18.00, 'g/dL', 2),

-- Hematocrito (ID 3)
(3, 'Mujeres Adultas', 37.00, 47.00, '%', 3),
(4, 'Varones Adultos', 40.00, 54.00, '%', 3),

-- Glóbulos Rojos (ID 1)
(5, 'Mujeres Adultas', 4.00, 5.20, 'mill/mm3', 1),
(6, 'Varones Adultos', 4.50, 5.90, 'mill/mm3', 1),

-- Volumen Corpuscular Medio (ID 4)
(7, 'Rango General', 80.00, 100.00, 'fL', 4),
-- Leucocitos Totales (ID 5)
(8, 'Rango General', 4500.00, 11000.00, 'mm3', 5),

-- Segmentados / Neutrófilos (ID 6)
(9, 'Rango General (%)', 55.00, 70.00, '%', 6),

-- Linfocitos (ID 7)
(10, 'Rango General (%)', 20.00, 40.00, '%', 7),

-- Monocitos (ID 8)
(11, 'Rango General (%)', 2.00, 8.00, '%', 8),

-- Eosinófilos (ID 9)
(12, 'Rango General (%)', 1.00, 4.00, '%', 9),

-- Basófilos (ID 10)
(13, 'Rango General (%)', 0.00, 1.00, '%', 10),

(14, 'Adultos en Ayuno', 70.00, 105.00, 'mg/dL', 22),      -- Glucosa
(15, 'Varones Adultos', 0.70, 1.30, 'mg/dL', 23),         -- Creatinina Varón
(16, 'Mujeres Adultas', 0.60, 1.10, 'mg/dL', 23),         -- Creatinina Mujer
(17, 'Rango General', 15.00, 45.00, 'mg/dL', 24),         -- Urea
(18, 'Varones Adultos', 3.40, 7.00, 'mg/dL', 25),         -- Ácido Úrico Varón
(19, 'Mujeres Adultas', 2.40, 5.70, 'mg/dL', 25),         -- Ácido Úrico Mujer
(20, 'Deseable', 0.00, 200.00, 'mg/dL', 26),              -- Colesterol Total
(21, 'Deseable', 0.00, 150.00, 'mg/dL', 27),              -- Triglicéridos
(22, 'Varones Adultos', 0.00, 40.00, 'U/L', 28),          -- TGO Varón
(23, 'Mujeres Adultas', 0.00, 32.00, 'U/L', 28),          -- TGO Mujer
(24, 'Rango General', 0.20, 1.20, 'mg/dL', 29),           -- Bilirrubina Total
(25, 'Rango General', 0.00, 0.30, 'mg/dL', 30),           -- Bilirrubina Directa
(26, 'Rango General', 0.10, 0.90, 'mg/dL', 31),           -- Bilirrubina Indirecta

(27, 'Negativo', 0.00, 80.00, 'Título', 32),           -- Antígeno O (Tifico)
(28, 'Negativo', 0.00, 80.00, 'Título', 33),           -- Antígeno H (Tifico)
(29, 'No Reactivo', 0.00, 8.00, 'UI/mL', 41),          -- Factor Reumatoideo
(30, 'Negativo', 0.00, 200.00, 'UI/mL', 46),           -- ASTO (Antiestreptolisina O)

(31, 'Resultado Normal', 0.00, 0.00, 'Cualitativo', 34), -- H. Pylori (No Reactivo)
(32, 'Resultado Normal', 0.00, 0.00, 'Cualitativo', 35), -- VDRL (No Reactivo)
(33, 'Resultado Normal', 0.00, 0.00, 'Cualitativo', 42), -- Dengue NS1 (No Reactivo)
(34, 'Resultado Normal', 0.00, 0.00, 'Cualitativo', 43), -- Dengue IgG (No Reactivo)
(35, 'Resultado Normal', 0.00, 0.00, 'Cualitativo', 44), -- Dengue IgM (No Reactivo)
(36, 'Resultado Normal', 0.00, 0.00, 'Cualitativo', 45), -- VIH (No Reactivo)

(37, 'No Reactivo', 0.00, 0.90, 'Index', 37),          -- Chagas ELISA
(38, 'No Reactivo', 0.00, 6.00, 'UI/mL', 39),          -- Toxoplasmosis IgG
(39, 'No Reactivo', 0.00, 0.80, 'Index', 40),          -- Toxoplasmosis IgM

(40, 'Normal (Pardo/Pastosa)', 0.00, 0.00, 'Descriptivo', 47), -- Color/Consistencia
(41, 'Ausencia de Parásitos', 0.00, 0.00, 'Negativo', 48),    -- Directo (Quistes/Huevos)
(42, 'Rango Normal', 0.00, 2.00, 'por campo', 49),           -- Leucocitos en Heces
(43, 'Rango Normal', 0.00, 0.00, 'por campo', 50),           -- Eritrocitos en Heces
(44, 'Negativo', 0.00, 0.00, 'Cualitativo', 51),             -- Sangre Oculta

(45, 'Amarillo/Suigéneris', 0.00, 0.00, 'Descriptivo', 52),  -- Físico (Color/Olor)
(46, 'Densidad Normal', 1.010, 1.030, 'g/mL', 53),           -- Densidad
(47, 'pH Urinario', 5.00, 7.50, 'pH', 53),                   -- pH
(48, 'Escasas/Ausentes', 0.00, 0.00, 'Descriptivo', 54),     -- Sedimento
(49, 'Negativo', 0.00, 0.00, 'Cualitativo', 55),             -- HCG Orina

(50, 'Rango Normal 24h', 0.00, 150.00, 'mg/24h', 56),        -- Proteínas Totales
(51, 'Volumen Normal Adulto', 800.00, 2000.00, 'mL', 57),     -- Volumen Urinario


(52, 'Negativo (Sin desarrollo)', 0.00, 0.00, 'UFC/mL', 58), -- Recuento de Colonias
(53, 'No se aislaron patógenos', 0.00, 0.00, 'Texto', 59),      -- Microorganismo
(54, 'Flora normal o negativo', 0.00, 0.00, 'Texto', 61),      -- Resultado Cultivo
(55, 'Flora habitual', 0.00, 0.00, 'Texto', 62),               -- Resultado Gram

(56, 'Adultos (Eutiroideo)', 0.27, 4.20, 'uUI/mL', 63),        -- TSH
(57, 'Adultos', 0.93, 1.70, 'ng/dL', 64),                     -- T4 Libre
(58, 'Adultos', 0.80, 2.00, 'ng/mL', 65),                     -- T3 Total
(59, 'No Embarazada', 0.00, 5.00, 'mUI/mL', 66),              -- B-HCG Cuantitativa

(60, 'Mujeres (No embarazadas)', 4.80, 23.30, 'ng/mL', 67),    -- Prolactina Mujer
(61, 'Varones Adultos', 4.00, 15.20, 'ng/mL', 67),            -- Prolactina Varón
(62, 'Rango en Ayunas', 2.60, 24.90, 'uUI/mL', 68),           -- Insulina Basal
(63, 'Varones < 40 años', 0.00, 2.00, 'ng/mL', 69),        -- PSA Total (Adulto joven)
(64, 'Varones > 40 años', 0.00, 4.00, 'ng/mL', 69),        -- PSA Total (Adulto)
(65, 'No fumadores', 0.00, 3.00, 'ng/mL', 70),             -- Marcador CEA
(66, 'Fumadores', 0.00, 5.00, 'ng/mL', 70),                -- Marcador CEA (Fumadores)
(67, 'Adultos', 0.00, 10.00, 'UI/mL', 71),                 -- AFP (Alfafetoproteína)
(68, 'Mujeres Adultas', 0.00, 35.00, 'U/mL', 72),         -- CA-125 (Marcador Ovario)

(69, 'Negativo', 0.00, 300.00, 'ng/mL', 73),               -- Cocaína (Punto de corte)
(70, 'Negativo', 0.00, 50.00, 'ng/mL', 74),                -- Marihuana (Punto de corte)
(71, 'Límite Legal (Conducción)', 0.00, 0.50, 'g/L', 75),  -- Alcoholemia
(72, 'Población General', 0.00, 10.00, 'ug/dL', 76),       -- Plomo en sangre

(73, 'No Detectado', 0.00, 0.00, 'Cualitativo', 77),       -- PCR COVID-19
(74, 'No Detectado / Indetectable', 0.00, 20.00, 'Copias/mL', 78), -- Carga Viral VIH
(75, 'Negativo', 0.00, 0.00, 'Cualitativo', 79),           -- VPH
 -- Paternidad
(76, 'Probabilidad > 99.99%', 0.00, 0.00, 'Porcentaje', 80);