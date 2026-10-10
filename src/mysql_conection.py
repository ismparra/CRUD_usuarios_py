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
    
    def get_connection(self):
        return self.connection

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
