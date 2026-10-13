from dataclasses import dataclass
from mysql.connector import Error, IntegrityError
from typing import List, Optional
import os
from dotenv import load_dotenv
# Cargar varibles de entorno
load_dotenv()

# Clave de cifrado
AES_KEY = os.getenv("AES_KEY")
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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    last_login: Optional[str] = None

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
        cursor = None
        try:
            cursor = self.connection.cursor()
            query ="insert into USERS(USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL, NUMEROTARJETA, TITULARTARJETA, FECHA_DE_VENCIMIENTO, CVV, ADMIN, PHONE_NUMBER, DATE_OF_BIRTH, CREATED_AT, UPDATED_AT, LAST_LOGIN, IS_ACTIVE) \
            values(%s,%s,%s,sha2(%s,256),%s,aes_encrypt(%s,%s),aes_encrypt(%s,%s),aes_encrypt(%s,%s),aes_encrypt(%s,%s),%s,%s,%s,NOW(),NOW(),NOW(),1)"
            valores = (user.username, user.nombre, user.apellidos, user.password, user.email,
                user.numeroTarjeta, AES_KEY,
                user.titularTarjeta, AES_KEY,
                user.fecha_de_vencimiento, AES_KEY,
                user.CVV, AES_KEY,
                user.admin, user.numero_Telefono, user.FechaNacimiento
            )
            cursor.execute(query, valores)
            self.connection.commit()
            return True
        except IntegrityError:
            self.connection.rollback()
            return False
        except Error:
            self.connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def modify_user(self, user: Usuario):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE USERS SET FIRSTNAME = %s, LASTNAME = %s, PASSWORD = SHA2(%s, 256),
                EMAIL = %s, NUMEROTARJETA = AES_ENCRYPT(%s, %s),
                TITULARTARJETA = AES_ENCRYPT(%s, %s), FECHA_DE_VENCIMIENTO = AES_ENCRYPT(%s, %s),
                CVV = AES_ENCRYPT(%s, %s), ADMIN = %s, PHONE_NUMBER = %s, 
                DATE_OF_BIRTH = %s, UPDATED_AT = NOW(), IS_ACTIVE = %s 
                WHERE USERNAME = %s"""
            # Se unificaron los nombres con el modelo
            valores = (
                user.nombre, user.apellidos, user.password, user.email,
                user.numeroTarjeta, AES_KEY,
                user.titularTarjeta, AES_KEY,
                user.fecha_de_vencimiento, AES_KEY,
                user.CVV, AES_KEY,
                user.admin, user.numero_Telefono, user.FechaNacimiento, user.UsuarioActivo,
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

    def update_user(self, username_original: str, user: Usuario) -> bool:
        cursor = None
        try:
            cursor = self.connection.cursor()

            # duplicados (otros usuarios que ya usen esos datos), excluyendo al propio usuario
            cursor.execute(
                "SELECT 1 FROM USERS WHERE (USERNAME = %s OR EMAIL = %s) AND USERNAME <> %s LIMIT 1",
                (user.username, user.email, username_original),
            )
            if cursor.fetchone():
                return False

            sets = [
                "USERNAME = %s", "FIRSTNAME = %s", "LASTNAME = %s", "EMAIL = %s",
                "NUMEROTARJETA = AES_ENCRYPT(%s, %s)",
                "TITULARTARJETA = AES_ENCRYPT(%s, %s)",
                "FECHA_DE_VENCIMIENTO = AES_ENCRYPT(%s, %s)",
                "CVV = AES_ENCRYPT(%s, %s)",
                "ADMIN = %s", "PHONE_NUMBER = %s", "DATE_OF_BIRTH = %s",
                "UPDATED_AT = NOW()",
            ]
            valores = [
                user.username, user.nombre, user.apellidos, user.email,
                user.numeroTarjeta, AES_KEY,
                user.titularTarjeta, AES_KEY,
                user.fecha_de_vencimiento, AES_KEY,
                user.CVV, AES_KEY,
                user.admin, user.numero_Telefono, user.FechaNacimiento,
            ]

            # La contrasena solo se cambia si escribieron una nueva, si esta vacia significa que seguira con la misma
            if user.password:
                sets.append("PASSWORD = SHA2(%s, 256)")
                valores.append(user.password)

            valores.append(username_original)
            cursor.execute(f"UPDATE USERS SET {', '.join(sets)} WHERE USERNAME = %s", valores)
            self.connection.commit()
            return True
        except IntegrityError:
            self.connection.rollback()
            return False
        except Error:
            self.connection.rollback()
            raise
        finally:
            if cursor:
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

    @staticmethod
    def _a_texto(valor):
        if valor is None:
            return ''
        if isinstance(valor, (bytes, bytearray)):
            return bytes(valor).decode('utf-8', errors='ignore')
        return str(valor)

    def get_user_con_tarjeta(self, usuario: str):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL,\
                CAST(AES_DECRYPT(NUMEROTARJETA, %s) AS CHAR) AS NUMEROTARJETA,\
                CAST(AES_DECRYPT(TITULARTARJETA, %s) AS CHAR) AS TITULARTARJETA,\
                CAST(AES_DECRYPT(FECHA_DE_VENCIMIENTO, %s) AS CHAR) AS FECHA_DE_VENCIMIENTO,\
                CAST(AES_DECRYPT(CVV, %s) AS CHAR) AS CVV,\
                ADMIN, PHONE_NUMBER, DATE_OF_BIRTH, IS_ACTIVE,\
                CREATED_AT, UPDATED_AT, LAST_LOGIN \
                FROM USERS WHERE USERNAME = %s",
                (AES_KEY, AES_KEY, AES_KEY, AES_KEY, usuario),
            )
            fila = cursor.fetchone()
        finally:
            cursor.close()
        return self.MapeoDeObjetos(fila) if fila else None

    def MapeoDeObjetos(self, fila: dict) -> Usuario:
        return Usuario(
            username=fila['USERNAME'],
            nombre=fila['FIRSTNAME'],
            apellidos=fila['LASTNAME'],
            password=fila['PASSWORD'],
            email=fila['EMAIL'],
            numeroTarjeta=self._a_texto(fila.get('NUMEROTARJETA')),
            titularTarjeta=self._a_texto(fila.get('TITULARTARJETA')),
            fecha_de_vencimiento=self._a_texto(fila.get('FECHA_DE_VENCIMIENTO')),
            CVV=self._a_texto(fila.get('CVV')),
            admin=bool(fila['ADMIN']),
            numero_Telefono=fila['PHONE_NUMBER'],
            FechaNacimiento=fila['DATE_OF_BIRTH'],
            UsuarioActivo=bool(fila['IS_ACTIVE']),
            created_at=self._a_texto(fila.get('CREATED_AT')),
            updated_at=self._a_texto(fila.get('UPDATED_AT')),
            last_login=self._a_texto(fila.get('LAST_LOGIN'))
        )
