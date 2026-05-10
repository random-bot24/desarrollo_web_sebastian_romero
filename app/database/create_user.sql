-- Crear Usuario
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';

GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';

FLUSH PRIVILEGES;

-- Eliminar usuarios de ser necesario
DROP USER 'cc5002'@'localhost';