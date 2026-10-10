from dataclasses import dataclass
from mysql.connector import Error
from typing import List, Optional

@dataclass
class Usuario:
    username: str
    nombre: str
    apellidos: str
    password: str
    email: str
    numeroTarjeta: str 
    titularTarjeta: str
    fecha_de_vencimiento: str
    CVV: str
    admin: bool
    numero_Telefono: str
    FechaNacimiento: str
    UsuarioActivo: bool = True
    id: Optional[int] = None

class DAO:
    def __init__(self, connection): 
        self.connection = connection

    def get_all_users(self):
        cursor = self.connection.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM USERS")
        filas = cursor.fetchall()
        cursor.close()
        return [self.MapeoDeObjetos(fila) for fila in filas]
    
    def get_user(self, usuario: str):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = %s", (usuario,))
        fila = cursor.fetchone()
        cursor.close()
        return self.MapeoDeObjetos(fila) if fila else None
    
    def get_userByPassword(self, usuario: str, password: str):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = %s AND PASSWORD = SHA2(%s, 256)", (usuario, password))
        fila = cursor.fetchone()
        cursor.close()
        return self.MapeoDeObjetos(fila) if fila else None

    def insert_user(self, user: Usuario):
        try:
            cursor = self.connection.cursor()
            query ="insert into USERS(USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL, NUMEROTARJETA, TITULARTARJETA, FECHA_DE_VENCIMIENTO, CVV, ADMIN, PHONE_NUMBER, DATE_OF_BIRTH, CREATED_AT, UPDATED_AT, LAST_LOGIN, IS_ACTIVE) \
            values(%s,%s,%s,sha2(%s,256),%s,aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),%s,%s,%s,NOW(),NOW(),NOW(),1)"
            valores = (user.username, user.nombre, user.apellidos, user.password, user.email, 
                       user.numeroTarjeta, user.titularTarjeta, user.fecha_de_vencimiento, 
                       user.CVV, user.admin, user.numero_Telefono, user.FechaNacimiento)
            cursor.execute(query, valores)
            self.connection.commit()
            print("Usuario insertado correctamente")
        except Error as e:
            print(f"Error al insertar usuario: {e}")
            self.connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def modify_user(self, user: Usuario):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE USERS SET FIRSTNAME = %s, LASTNAME = %s, PASSWORD = SHA2(%s, 256),
                EMAIL = %s, NUMEROTARJETA = AES_ENCRYPT(%s, '**PRIvada002233'),
                TITULARTARJETA = AES_ENCRYPT(%s, '**PRIvada002233'), FECHA_DE_VENCIMIENTO = AES_ENCRYPT(%s, '**PRIvada002233'),
                CVV = AES_ENCRYPT(%s, '**PRIvada002233'), ADMIN = %s, PHONE_NUMBER = %s, 
                DATE_OF_BIRTH = %s, UPDATED_AT = NOW(), IS_ACTIVE = %s 
                WHERE USERNAME = %s"""
            # Se unificaron los nombres con el modelo
            valores = (
                user.nombre, user.apellidos, user.password, user.email, 
                user.numeroTarjeta, user.titularTarjeta, user.fecha_de_vencimiento, 
                user.CVV, user.admin, user.numero_Telefono, user.FechaNacimiento, user.UsuarioActivo,
                user.username
            )
            cursor.execute(query, valores)
            self.connection.commit()
            print("Usuario modificado correctamente")
        except Error as e:
            print(f"Error al modificar el usuario: {e}")
            self.connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def Unsuscribe(self, usuario: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE USERS SET IS_ACTIVE = FALSE WHERE USERNAME = %s", (usuario,)) # Agregada coma
            self.connection.commit()
            print("Usuario dado de baja")
        except Error as e:
            print(f"Error al dar de baja al usuario: {e}")
            self.connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def DELETEUSER(self, usuario: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM USERS WHERE USERNAME = %s", (usuario,))
            self.connection.commit()
            print("Usuario eliminado")
        except Error as e:
            print(f"Error al eliminar el usuario: {e}")
            self.connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def MapeoDeObjetos(self, fila: dict) -> Usuario:
        return Usuario(
            username=fila['USERNAME'],
            nombre=fila['FIRSTNAME'],
            apellidos=fila['LASTNAME'],
            password=fila['PASSWORD'],
            email=fila['EMAIL'],
            numeroTarjeta=fila.get('NUMEROTARJETA', ''),  
            titularTarjeta=fila.get('TITULARTARJETA', ''),
            fecha_de_vencimiento=fila.get('FECHA_DE_VENCIMIENTO', ''),
            CVV=fila.get('CVV', ''),
            admin=bool(fila['ADMIN']),
            numero_Telefono=fila['PHONE_NUMBER'],
            FechaNacimiento=fila['DATE_OF_BIRTH'],
            UsuarioActivo=bool(fila['IS_ACTIVE'])
        )
