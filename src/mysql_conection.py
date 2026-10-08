import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost', database='control_itsur', user='root', password='root'
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Conexión exitosa a MySQL.")
        except Error as e:
            print(f"Error al conectar: {e}")

    # Consultas
    def get_all_users(self):
        self.cursor.execute("select * from USERS")
        return self.cursor.fetchall()
    
    def get_user(self,usuario):
        self.cursor.execute("select * from USERS where USERNAME = %s",(usuario,))
        return self.cursor.fetchone()
    
    def get_userByPassword(self,usuario,password):
        self.cursor.execute("select * from USERS where USERNAME = %s and PASSWORD = sha2(%s,256)",(usuario,password))
        return self.cursor.fetchone()

    def insert_user(self, usuario, nombre, apellidos, password,email, numeroTarjeta, titularTarjeta,fecha_de_vencimiento, CVV, admin, numero_Telefono, FechaNacimiento):
        try:
            self.cursor.execute("insert into USERS(USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL, NUMEROTARJETA, TITULARTARJETA, FECHA_DE_VENCIMIENTO, CVV, ADMIN, PHONE_NUMBER, DATE_OF_BIRTH, CREATED_AT, UPDATED_AT, LAST_LOGIN, IS_ACTIVE) \
            values(%s,%s,%s,sha2(%s,256),%s,aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'),%s,%s,%s,NOW(),NOW(),NOW(),1)",(usuario, nombre, apellidos, password,email, numeroTarjeta, titularTarjeta, fecha_de_vencimiento, CVV, admin, numero_Telefono, FechaNacimiento))
            self.connection.commit()
            print("usuario insertado correctamente")
        except Error as e:
            print(f"Error al insertar usuario: {e}")
            self.connection.rollback()

    def modify_user(self, usuario, nombre, apellidos, password,email, numeroTarjeta, titularTarjeta,fecha_de_vencimiento, CVV, admin, numero_Telefono, FechaNacimiento):
        try:
            self.cursor.execute("UPDATE USERS SET USERNAME = %s, FIRSTNAME = %s, LASTNAME = %s, PASSWORD = SHA2(%s, 256),\
                                 EMAIL = %s, NUMEROTARJETA = AES_ENCRYPT(%s, '**PRIvada002233'),\
                                 TITULARTARJETA = AES_ENCRYPT(%s, '**PRIvada002233'), FECHA_DE_VENCIMIENTO = AES_ENCRYPT(%s, '**PRIvada002233'),\
                                 CVV = AES_ENCRYPT(%s, '**PRIvada002233'), ADMIN = %s, PHONE_NUMBER = %s, DATE_OF_BIRTH = %s, CREATED_AT = NOW(), UPDATED_AT = NOW(),\
                                 LAST_LOGIN = NOW(), IS_ACTIVE = %s WHERE USERNAME = %s;",(usuario, nombre, apellidos, password,email, numeroTarjeta, titularTarjeta, fecha_de_vencimiento, CVV, admin, numero_Telefono, FechaNacimiento))
            self.connection.commit()
            print("usuario modificado correctamente")
        except Error as e:
            print(f"Error al modificar el usuario: {e}")
            self.connection.rollback()

    def DELETEUSER(usuario):
        try:
            self.cursor.execute("UPDATE USERS SET IS_ACTIVE = FALSE WHERE USERNAME = %s", (usuario))
            self.connection.commit()
            print("Usuario dado de baja")
        except Error as e:
            print(f"Error al dar de baja al usuario: {e}")
            self.connection.rollback()

    def close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")

    

# use de clase:
db = Database()

db.insert_user('S24120166','Pancho123','Francisco','Nunes Gomez','panchito123','pancho@email','123123123123123','543')
usuario = db.get_userByPassword('Ismael10','isma123')
print(usuario)
usuarios = db.get_all_users()
for u in usuarios:
    print(u)

db.close()
