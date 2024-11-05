INSERT INTO "tesis" (titulo, resumen, especialidad, keywords, autor1, autor2, asesor, creacion_en, actividad_focus, revisor1, revisor2, asesorado)
VALUES 
('Optimización de Algoritmos de Búsqueda en Inteligencia Artificial',
 'Esta tesis presenta técnicas avanzadas de optimización en algoritmos de búsqueda heurística aplicados en sistemas de inteligencia artificial, analizando su rendimiento en distintas configuraciones.',
 'Inteligencia Artificial',
 'algoritmos, búsqueda heurística, IA, optimización',
 35, NULL, 10, NOW(), 'Revisión final', 15, NULL, TRUE),

('Análisis Comparativo de Tecnologías Blockchain en Sistemas Financieros',
 'Este trabajo evalúa el impacto y la viabilidad de implementar distintas tecnologías blockchain en la banca digital, abordando los beneficios y desafíos asociados.',
 'Finanzas y Tecnología',
 'blockchain, sistemas financieros, banca digital, criptografía',
 36, 37, 11, NOW(), 'Desarrollo de contenido', 16, NULL, TRUE),

('Diseño de Redes Neuronales Convolucionales para Detección de Imágenes Médicas',
 'Explora el uso de redes neuronales convolucionales en la detección temprana de enfermedades a través de imágenes médicas, destacando mejoras en precisión y velocidad.',
 'Ingeniería Biomédica',
 'redes neuronales, detección de imágenes, medicina, aprendizaje profundo',
 38, NULL, 12, NOW(), 'Recopilación de datos', NULL, 17, TRUE),

('Evaluación de Modelos de Energía Renovable en Zonas Rurales',
 'Investiga diferentes modelos de implementación de energías renovables para zonas rurales, identificando el impacto en el desarrollo económico y ambiental de las comunidades.',
 'Ingeniería Ambiental',
 'energías renovables, zonas rurales, impacto ambiental, economía',
 39, NULL, 13, NOW(), 'Análisis de datos', 18, NULL, FALSE),

('Desarrollo de Sistemas Predictivos para Análisis de Datos en el Transporte Público',
 'Desarrolla y valida un modelo predictivo para la optimización de tiempos de viaje en rutas de transporte público, utilizando técnicas de machine learning.',
 'Data Science',
 'machine learning, transporte público, análisis predictivo, big data',
 44, 45, 14, NOW(), 'Desarrollo de modelo', NULL, 19, FALSE);
