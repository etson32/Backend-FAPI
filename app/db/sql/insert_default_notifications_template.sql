INSERT INTO notification_entities (entity, entity_kind, type, template, is_deleted, created_at, updated_at)
VALUES
    ('propuesta_tesis', 'inclusión', 'tesista_invita', '{usuario_nombres} ha sido invitado para ser autor en la tesis.', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'inclusión', 'tesista_invitado', '{usuario_nombres} te invitó para ser autor en la tesis: {tesis_titulo}.', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'inclusión', 'tesista_acepta', '{usuario_nombres} ha aceptado ser autor de la tesis.', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'inclusión', 'tesista_rechaza', '{usuario_nombres} rechazó ser autor de la tesis.', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'propuesta', 'propuesta_enviada', 'Se envio la propuesta de tesis al docente: {usuario_nombres}', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'corrección', 'correccion_requerida', 'El docente {usuario_nombres} ha solicitado correcciones en la propuesta de tesis.', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'corrección', 'correccion_completada', 'Las correcciones solicitadas del trabajo: {tesis_titulo} han sido completadas y revisadas.', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'propuesta', 'propuesta_aceptada', 'La propuesta de tesis ha sido aceptada por el docente: {usuario_nombres}.', FALSE, NOW(), NOW()),
    ('propuesta_tesis', 'propuesta', 'propuesta_rechazada', 'La propuesta de tesis ha sido rechazada por el docente: {usuario_nombres}.', FALSE, NOW(), NOW()),
    ('plan_tesis', 'revisión', 'revisor_asignado', 'Se ha asignado como revisor a la tesis: {usuario_nombres}.', FALSE, NOW(), NOW()),
    ('plan_tesis', 'revisión', 'revisión_completada', 'El revisor ha completado la revisión de la tesis.', FALSE, NOW(), NOW());
   
    --('usuario', 'registro', 'nuevo_registro', 'Un nuevo usuario se ha registrado: {{ usuario }}.', FALSE, NOW(), NOW()),
    --('usuario', 'perfil', 'perfil_actualizado', 'El perfil de usuario ha sido actualizado.', FALSE, NOW(), NOW()),
    --('usuario', 'actividad', 'actividad_completada', 'El usuario {{ usuario }} ha completado la actividad: {{ actividad }}.', FALSE, NOW(), NOW());



