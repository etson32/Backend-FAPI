INSERT INTO "usuario" 
    (apellidos_familiar, nombres, email, dni, password_hash, google_sub, fecha_creacion, grado_academico, activo, esta_registrado, id_rol)
VALUES
    ('Rivas Puga', 'Abdón', 'abdon.rivas@unsaac.edu.pe', '12345678', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Licenciado', TRUE, TRUE,(SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Candia Oviedo', 'Dennis Iván', 'dennis.candia@unsaac.edu.pe', '12345679', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Ingeniero', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Aguirre Carbajal', 'Doris Sabina', 'doris.aguirre@unsaac.edu.pe', '12345680', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Magister', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Carrasco Poblete', 'Edwin', 'edwincarrasco@unsaac.edu.pe', '12345681', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Magister', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Cutipa Arapa', 'Efraina Gladys', 'efraina.cutipa@unsaac.edu.pe', '12345682', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Ingeniero', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Palomino Olivera', 'Emilio', 'emiliopalomino@unsaac.edu.pe', '12345683', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Magister', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Gamarra Saldivar', 'Enrique', 'enrique.gamarra@unsaac.edu.pe', '12345684', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Magister', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Pacheco Vasquez', 'Esther Cristina', 'esther.pacheco@unsaac.edu.pe', '12345685', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Ingeniero', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Ticona Pari', 'Guzmán', 'guzman.ticona@unsaac.edu.pe', '12345686', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Ingeniero', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente')),
    ('Vera Olivera', 'Harley', 'harley.vera@unsaac.edu.pe', '12345687', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Magister', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Docente'));


INSERT INTO "usuario" 
     (apellidos_familiar, nombres, email, dni, password_hash, google_sub, fecha_creacion, grado_academico, activo, esta_registrado, id_rol)
VALUES
    ('Gutierrez Salazar', 'Juan Manuel', '173891@unsaac.edu.pe', '12345671', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Gutierrez Taqqquere', 'Luis Fernando', '172145@unsaac.edu.pe', '23456782', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Gutierrez Yucra', 'Pamela', '176782@unsaac.edu.pe', '34567893', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Hancco Chaco', 'Jose Maria', '170394@unsaac.edu.pe', '45678904', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Hancco León', 'Alexander', '175643@unsaac.edu.pe', '56789015', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Hanco Gayona', 'Mariela', '174820@unsaac.edu.pe', '67890126', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Hinojosa Huarca', 'Brayan Alexandert', '172917@unsaac.edu.pe', '78901237', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Holguin Condori', 'Julio Josue', '177059@unsaac.edu.pe', '89012348', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Huaman Atayupanqui', 'Lisbet Paola', '178341@unsaac.edu.pe', '90123459', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1)),
    ('Huaman Cabrera', 'Yonathan', '171578@unsaac.edu.pe', '01234560', '$2b$12$YzoZOf98VW2AAHVO3B0G7eUTP70sIVJb2dopwvS/2QfC5QfJ/0ZBq', NULL, NOW(), 'Estudiante', TRUE, TRUE, (SELECT id_rol FROM rol WHERE nombre_rol = 'Tesista' LIMIT 1));


