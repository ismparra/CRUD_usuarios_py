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
        self.cursor.execute("select * from usuarios")
        return self.cursor.fetchall()
    
    def get_user(self,usuario):
        self.cursor.execute("select * from usuarios where usuario = %s",(usuario,))
        return self.cursor.fetchone()
    
    def get_userByPassword(self,usuario,password):
        self.cursor.execute("select * from usuarios where usuario = %s and password = sha2(%s,256)",(usuario,password))
        return self.cursor.fetchone()

    def insert_user(self,control, usuario, nombre, apellidos, password,email, numeroTarjeta, CVV):
        try:
            self.cursor.execute("insert into usuarios(control, usuario, nombre, apellidos, password,email, NumeroTarjeta, CVV) \
            values(%s,%s,%s,%s,sha2(%s,256),%s,aes_encrypt(%s,'**PRIvada002233'),aes_encrypt(%s,'**PRIvada002233'))",(control, usuario, nombre, apellidos, password,email, numeroTarjeta, CVV))
            self.connection.commit()
            print("usuario insertado correctamente")
        except Error as e:
            print(f"Error al insertar usuario: {e}")
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