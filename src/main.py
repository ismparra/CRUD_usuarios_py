import customtkinter as ctk
from login import LoginFrame
from registro import RegisterFrame
from tarjeta import TarjetaFrame
from dao import DAO
from mysql_conection import Database
# tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AuthApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Autenticación")
        self.geometry("1280x720")
        self.resizable(False, False)
        
        # Base de datos
        self.db = Database()

        # Cargar DAO
        self.dao = DAO(self.db.get_connection())

        # Lista para los valores del registro
        self.datos_registro = {} 

        # Variable para el frame actual
        self.current_frame = None

        # Cerrar conexion
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.show_frame("LoginFrame")
        self.after(0, lambda: self.state("zoomed"))
    def show_frame(self, frame_name):
        """Alterna dinámicamente entre los módulos importados."""
        if self.current_frame is not None:
            self.current_frame.destroy()

        if frame_name == "LoginFrame":
            self.current_frame = LoginFrame(master=self, controller=self)
        elif frame_name == "RegisterFrame":
            self.current_frame = RegisterFrame(master=self, controller=self)
        elif frame_name == "TarjetaFrame":
            self.current_frame = TarjetaFrame(master = self, controller = self)

        self.current_frame.pack(pady=30, padx=30, fill="both", expand=True)

    def on_close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()