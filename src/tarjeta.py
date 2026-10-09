import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
# !!!PROVISIONAL!!!: esta función aún no existe, se creará en el DAO
from dao.usuario_dao import registrar_usuario
class TarjetaFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, corner_radius=15, fg_color="#1E1E2E")
        self.controller = controller

        # titulo
        ctk.CTkLabel(
            self, text="Agrega los datos de tu tarjeta",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self, text="¡Ya casi finalizas tu registro!",
            font=ctk.CTkFont(size=13),
            text_color="#A6ADC8"
        ).pack(pady=(0, 20))

        # numeroTarjeta
        self.numero_tarjeta_entry = ctk.CTkEntry(
            self, placeholder_text="Numero Tarjeta",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.numero_tarjeta_entry.pack(pady=8)


        # titularTarjeta
        self.titular_tarjeta_entry = ctk.CTkEntry(
            self, placeholder_text="Titular Tarjeta",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.titular_tarjeta_entry.pack(pady=8)
        
        # fecha vencimiento
        self.fecha_vencimiento_entry = ctk.CTkEntry(
            self, placeholder_text="Fecha de vencimiento",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.fecha_vencimiento_entry.pack(pady=8)

        # cvv
        self.cvv_entry = ctk.CTkEntry(
            self, placeholder_text="CVV",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.cvv_entry.pack(pady=8)

        # boton Finalizar
        ctk.CTkButton(
            self, text="Finalizar Registro", command=self.submit_register,
            width=280, height=45, corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#A6E3A1", hover_color="#94E2D5", text_color="#11111B"
        ).pack(pady=(20, 10))

    def submit_register(self):
        numero = self.numero_tarjeta_entry.get().replace(" ", "").strip()
        titular = self.titular_tarjeta_entry.get().strip()
        vencimiento = self.fecha_vencimiento_entry.get().strip()
        cvv = self.cvv_entry.get().strip()

        if not all([numero, titular, vencimiento, cvv]):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        if not numero.isdigit() or len(numero) != 16:
            messagebox.showwarning("Atención", "El número de tarjeta debe tener 16 dígitos.")
            return

        # Fecha de vencimiento (MM/AA)
        try:
            fecha_venc = datetime.strptime(vencimiento, "%m/%y")
        except ValueError:
            messagebox.showwarning("Atención", "La fecha de vencimiento debe tener el formato MM/AA.")
            return

        hoy = datetime.now()
        if (fecha_venc.year, fecha_venc.month) < (hoy.year, hoy.month):
            messagebox.showwarning("Atención", "La tarjeta está vencida.")
            return

        if not cvv.isdigit() or len(cvv) != 3:
            messagebox.showwarning("Atención", "El CVV debe tener 3 dígitos.")
            return

        # Cargar datos de usuario de la pantalla anterior
        datos_usuario = self.controller.datos_registro

        datos_tarjeta = {
            "numero": numero,
            "titular": titular,
            "vencimiento": fecha_venc.date(),
            "cvv": cvv,
        }

        # PROVISIONAL: llamada al DAO (firma y valor de retorno por definir)
        try:
            registrado = registrar_usuario(datos_usuario, datos_tarjeta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar el registro: {e}")
            return

        if not registrado:
            messagebox.showerror("Error", "El nombre de usuario o correo ya existe.")
            self.controller.show_frame("RegisterFrame")
            return

        # Limpiar datos sensibles de memoria
        self.controller.datos_registro = {}
        messagebox.showinfo("Éxito", "¡Registro completado!")
        # Limpiar campos
        registro = self.controller.frames["RegisterFrame"]
        for entry in (
            registro.user_entry, registro.name_entry, registro.lastname_entry,
            registro.birth_entry, registro.email_entry, registro.phone_entry,
            registro.pass_entry, registro.confirm_pass_entry,
            self.numero_tarjeta_entry, self.titular_tarjeta_entry,
            self.fecha_vencimiento_entry, self.cvv_entry,
        ):
            entry.delete(0, "end")
        registro.admin_var.set('off')
        # Regresar a registro
        self.controller.show_frame("LoginFrame")