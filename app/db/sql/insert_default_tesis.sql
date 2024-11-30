INSERT INTO "tesis" (titulo, resumen, especialidad, keywords, creacion_en, actividad_focus, asesorado)
VALUES 
('Optimización de Algoritmos de Búsqueda en Inteligencia Artificial',
 'Esta tesis presenta técnicas avanzadas de optimización en algoritmos de búsqueda heurística aplicados en sistemas de inteligencia artificial, analizando su rendimiento en distintas configuraciones.',
 'Inteligencia Artificial',
  ARRAY['algoritmos', 'búsqueda heurística', 'IA', 'optimización'], NOW(), 'Revisión final', FALSE),

('Análisis Comparativo de Tecnologías Blockchain en Sistemas Financieros',
 'Este trabajo evalúa el impacto y la viabilidad de implementar distintas tecnologías blockchain en la banca digital, abordando los beneficios y desafíos asociados.',
 'Finanzas y Tecnología',
  ARRAY['blockchain', 'sistemas financieros', 'banca digital', 'criptografía'], NOW(), 'Desarrollo de contenido', FALSE),

('Diseño de Redes Neuronales Convolucionales para Detección de Imágenes Médicas',
 'Explora el uso de redes neuronales convolucionales en la detección temprana de enfermedades a través de imágenes médicas, destacando mejoras en precisión y velocidad.',
 'Ingeniería Biomédica',
  ARRAY['redes neuronales', 'detección de imágenes', 'medicina', 'aprendizaje profundo'], NOW(), 'Recopilación de datos', FALSE),

('Evaluación de Modelos de Energía Renovable en Zonas Rurales',
 'Investiga diferentes modelos de implementación de energías renovables para zonas rurales, identificando el impacto en el desarrollo económico y ambiental de las comunidades.',
 'Ingeniería Ambiental',
  ARRAY['energías renovables', 'zonas rurales', 'impacto ambiental', 'economía'], NOW(), 'Análisis de datos', FALSE),

('Desarrollo de Sistemas Predictivos para Análisis de Datos en el Transporte Público',
 'Desarrolla y valida un modelo predictivo para la optimización de tiempos de viaje en rutas de transporte público, utilizando técnicas de machine learning.',
 'Data Science',
  ARRAY['machine learning', 'transporte público', 'análisis predictivo', 'big data'], NOW(), 'Desarrollo de modelo', FALSE);
 
INSERT INTO "integrantes_tesis" (id_tesis, id_usuario, id_rol)
VALUES 
(1,10,(SELECT id_rol FROM rol WHERE nombre_rol = 'Autor')),
(1,1,(SELECT id_rol FROM rol WHERE nombre_rol = 'Asesor')),

(2,11,(SELECT id_rol FROM rol WHERE nombre_rol = 'Autor')),
(2,12,(SELECT id_rol FROM rol WHERE nombre_rol = 'Autor')),
(2,5,(SELECT id_rol FROM rol WHERE nombre_rol = 'Asesor')),

(3,13,(SELECT id_rol FROM rol WHERE nombre_rol = 'Autor')),
(3,2,(SELECT id_rol FROM rol WHERE nombre_rol = 'Asesor')),

(4,14,(SELECT id_rol FROM rol WHERE nombre_rol = 'Autor')),
(4,3,(SELECT id_rol FROM rol WHERE nombre_rol = 'Asesor')),
 
(5,15,(SELECT id_rol FROM rol WHERE nombre_rol = 'Autor')),
(5,16,(SELECT id_rol FROM rol WHERE nombre_rol = 'Autor')),
(5,4,(SELECT id_rol FROM rol WHERE nombre_rol = 'Asesor'));