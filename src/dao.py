from dataclasses import dataclass
from mysql.connector import Error
from typing import List, Optional

@dataclass
class Usuario:
    id: Optional[int]
    username: str
    nombre: str
    apellidos: str
    email: str
    password: str
    numeroTarjeta: str 
    titularTarjeta: str
    fecha_de_vencimiento: str
    CVV: str
    admin: bool
    numero_Telefono: str
    FechaNacimiento: str
    UsuarioActivo: bool

#DAO
class dao:
    def __unit__(self, connection):
        self.connection = connection
        # Consultas
    def get_all_users(self):
        cursor = self.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS")
        filas = cursor.fetchall()
        cursor.close()
        return [self.MapeoDeObjetos(fila) for fila in filas]
    
    def get_user(self,usuario: str):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = %s", (usuario,))
        fila = cursor.fetchone()
        cursor.close()
        return self.MapeoDeObjetos(fila) if fila else None
    
    def get_userByPassword(self,usuario: str,password: str):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = %s AND PASSWORD = SHA2(%s, 256)", (usuario,password))
        fila = cursor.fetchone()
        cursor.close()
        return self.MapeoDeObjetos(fila) if fila else None

    def insert_user(self, usuario, nombre, apellidos, password,email, numeroTarjeta, titularTarjeta,fecha_de_vencimiento, CVV, admin, numero_Telefono, FechaNacimiento):
        try:
            cursor = self.connection.cursor()
            query ="insert into USERS(USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL, NUMEROTARJETA, TITULARTARJETA, FECHA_DE_VENCIMIENTO, CVV, ADMIN, PHONE_NUMBER, DATE_OF_BIRTH, CREATED_AT, UPDATED_AT, LAST_LOGIN, IS_ACTIVE) \
            values(%s,%s,%s,sha2(%s,256),%s,aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),%s,%s,%s,NOW(),NOW(),NOW(),1)"
            valores = (usuario, nombre, apellidos, password,email, numeroTarjeta, titularTarjeta, fecha_de_vencimiento, CVV, admin, numero_Telefono, FechaNacimiento)
            cursor.execute(query, valores)
            self.connection.commit()
            print("usuario insertado correctamente")
        except Error as e:
            print(f"Error al insertar usuario: {e}")
            self.connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def modify_user(self, usuario):
        try:
            cursor = self.connection.cursor()
            # Nota: Cambié el primer %s de USERNAME por el WHERE al final.
            query = """UPDATE USERS SET USERNAME = %s, FIRSTNAME = %s, LASTNAME = %s, PASSWORD = SHA2(%s, 256),
                EMAIL = %s, NUMEROTARJETA = AES_ENCRYPT(%s, '**PRIvada002233'),
                TITULARTARJETA = AES_ENCRYPT(%s, '**PRIvada002233'), FECHA_DE_VENCIMIENTO = AES_ENCRYPT(%s, '**PRIvada002233'),
                CVV = AES_ENCRYPT(%s, '**PRIvada002233'), ADMIN = %s, PHONE_NUMBER = %s, 
                DATE_OF_BIRTH = %s, UPDATED_AT = NOW(), IS_ACTIVE = %s 
                WHERE USERNAME = %s"""
            valores = (
                usuario.firstname, usuario.lastname, usuario.password, usuario.email, 
                usuario.numero_tarjeta, usuario.titular_tarjeta, usuario.fecha_vencimiento, 
                usuario.cvv, usuario.admin, usuario.phone_number, usuario.date_of_birth, usuario.is_active,
                usuario.username)
            cursor.execute(query, valores)
            self.connection.commit()
            print("Usuario modificado correctamente")
        except Error as e:
            print(f"Error al modificar el usuario: {e}")
            self.connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def Unsuscribe(self, usuario):
            try:
                cursor = self.connection.cursor()
                cursor.execute("UPDATE USERS SET IS_ACTIVE = FALSE WHERE USERNAME = %s", (usuario))
                self.connection.commit()
                print("Usuario dado de baja")
            except Error as e:
                print(f"Error al dar de baja al usuario: {e}")
                self.connection.rollback()
            finally:
                if 'cursor' in locals():
                    cursor.close()

    def DELETEUSER(self,usuario):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM USERS WHERE USERNAME = %s", (usuario))
            self.connection.commit()
            print("Usuario eliminado")
        except Error as e:
            print(f"Error al eliminar el usuario: {e}")
            self.connection.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def MapeoDeObjetos(self, fila: dict) -> Usuario:
        #Convierte el diccionario de MySQL a un objeto en Python
        return Usuario(
            username=fila['USERNAME'],
            firstname=fila['FIRSTNAME'],
            lastname=fila['LASTNAME'],
            password=fila['PASSWORD'],
            email=fila['EMAIL'],
            numero_tarjeta=fila.get('NUMEROTARJETA', ''),  #.get() por que se puede dar el caso de que el valor sea null
            titular_tarjeta=fila.get('TITULARTARJETA', ''),
            fecha_vencimiento=fila.get('FECHA_DE_VENCIMIENTO', ''),
            cvv=fila.get('CVV', ''),
            admin=bool(fila['ADMIN']),
            phone_number=fila['PHONE_NUMBER'],
            date_of_birth=fila['DATE_OF_BIRTH'],
            is_active=bool(fila['IS_ACTIVE'])
        )
