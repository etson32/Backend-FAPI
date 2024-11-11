INSERT INTO "tesis" (titulo, resumen, especialidad, keywords, autor1, autor2, asesor, creacion_en, actividad_focus, revisor1, revisor2, asesorado)
VALUES 
('Optimización de Algoritmos de Búsqueda en Inteligencia Artificial',
 'Esta tesis presenta técnicas avanzadas de optimización en algoritmos de búsqueda heurística aplicados en sistemas de inteligencia artificial, analizando su rendimiento en distintas configuraciones.',
 'Inteligencia Artificial',
  ARRAY['algoritmos', 'búsqueda heurística', 'IA', 'optimización'],
 10, NULL, 1, NOW(), 'Revisión final', NULL, NULL, FALSE),

('Análisis Comparativo de Tecnologías Blockchain en Sistemas Financieros',
 'Este trabajo evalúa el impacto y la viabilidad de implementar distintas tecnologías blockchain en la banca digital, abordando los beneficios y desafíos asociados.',
 'Finanzas y Tecnología',
  ARRAY['blockchain', 'sistemas financieros', 'banca digital', 'criptografía'],
 11, 12, 5, NOW(), 'Desarrollo de contenido', NULL, NULL, FALSE),

('Diseño de Redes Neuronales Convolucionales para Detección de Imágenes Médicas',
 'Explora el uso de redes neuronales convolucionales en la detección temprana de enfermedades a través de imágenes médicas, destacando mejoras en precisión y velocidad.',
 'Ingeniería Biomédica',
  ARRAY['redes neuronales', 'detección de imágenes', 'medicina', 'aprendizaje profundo'],
 13, NULL, 2, NOW(), 'Recopilación de datos', NULL, NULL, FALSE),

('Evaluación de Modelos de Energía Renovable en Zonas Rurales',
 'Investiga diferentes modelos de implementación de energías renovables para zonas rurales, identificando el impacto en el desarrollo económico y ambiental de las comunidades.',
 'Ingeniería Ambiental',
  ARRAY['energías renovables', 'zonas rurales', 'impacto ambiental', 'economía'],
14, NULL, 3, NOW(), 'Análisis de datos', NULL, NULL, FALSE),

('Desarrollo de Sistemas Predictivos para Análisis de Datos en el Transporte Público',
 'Desarrolla y valida un modelo predictivo para la optimización de tiempos de viaje en rutas de transporte público, utilizando técnicas de machine learning.',
 'Data Science',
  ARRAY['machine learning', 'transporte público', 'análisis predictivo', 'big data'],
15, 16, 4, NOW(), 'Desarrollo de modelo', NULL, NULL, FALSE);
 