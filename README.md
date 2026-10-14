# CRUD_Usuarios

Este proyecto es una aplicación de escritorio desarrollada en Python utilizando CustomTkinter. La aplicación está enfocada en la gestión de usuarios mediante operaciones CRUD, permitiendo el registro, autenticación y administración de perfiles y datos bancarios de forma segura. Implementa cifrado de datos sensibles y se conecta a una base de datos MySQL alojada en la nube (Azure).

## Autores
- Ismael Parra Calderón
- Isaac Pérez Albor

## Main features:
- **Gestión de Usuarios y Roles:** Operaciones completas CRUD (Crear, Leer, Actualizar, Eliminar) con vistas condicionadas según el rol del usuario (Administradores y Usuarios regulares).
- **Seguridad:** Hash de contraseñas utilizando SHA-256 y encriptación bidireccional AES para salvaguardar la información sensible de las tarjetas de crédito (Número, Titular, Vencimiento, CVV).
- **Interfaz Gráfica Moderna:** UI dinámica y estructurada por módulos (Frames) construida íntegramente con CustomTkinter con un tema oscuro.
- **Persistencia en la Nube:** Conexión a base de datos MySQL estructurada para auditoría básica, manteniendo un registro automático de creación, última actualización y último inicio de sesión (`LAST_LOGIN`).
- **Soft Deletes (Bajas Lógicas):** Funcionalidad para desactivar o "dar de baja" cuentas impidiendo su acceso, sin necesidad de borrar permanentemente los registros históricos de la base de datos.

## TECH STACK
- **Lenguaje:** Python
- **Framework GUI:** CustomTkinter
- **DataBase:** MySQL (mediante `mysql-connector-python` apuntando a un servidor Azure).
- **Security:** Funciones criptográficas delegadas a la base de datos (`AES_ENCRYPT`, `AES_DECRYPT`, `SHA2`).
- **Environment:** `python-dotenv` para la gestión segura de claves de cifrado y credenciales de red.

## Prerequisites
- Python 3.8 o superior.
- Instalación de las dependencias requeridas mediante pip: `customtkinter`, `mysql-connector-python` y `python-dotenv`.
- Un servidor MySQL activo con el esquema de base de datos proporcionado en `general_schema.sql` ejecutado.
- Un archivo `.env` configurado en la raíz del proyecto (SRC) que contenga las credenciales de conexión (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) y la clave de cifrado (`AES_KEY`).
