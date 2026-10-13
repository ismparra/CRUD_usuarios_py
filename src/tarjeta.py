from datetime import datetime, date
from tkinter import messagebox
import customtkinter as ctk

from dao import DAO, Usuario


class TarjetaFrame(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master, corner_radius=15, fg_color="#1E1E2E")
        self.controller = controller

        # Modo y usuario original
        self.editando = controller.modo == "editar"
        self.original = controller.usuario_editando

        # Titulo
        ctk.CTkLabel(
            self,
            text=(
                "Modifica los datos de la tarjeta"
                if self.editando
                else "Agrega los datos de tu tarjeta"
            ),
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF",
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self,
            text=(
                f"Usuario: {self.original.username}"
                if self.editando
                else "¡Ya casi finalizas tu registro!"
            ),
            font=ctk.CTkFont(size=13),
            text_color="#A6ADC8",
        ).pack(pady=(0, 20))

        # Numero de Tarjeta
        self.numero_tarjeta_entry = ctk.CTkEntry(
            self,
            placeholder_text="Número Tarjeta (16 dígitos)",
            width=280,
            height=42,
            corner_radius=10,
            fg_color="#313244",
            border_color="#45475A",
            text_color="#FFFFFF",
        )
        self.numero_tarjeta_entry.pack(pady=8)

        # Titular Tarjeta
        self.titular_tarjeta_entry = ctk.CTkEntry(
            self,
            placeholder_text="Titular Tarjeta",
            width=280,
            height=42,
            corner_radius=10,
            fg_color="#313244",
            border_color="#45475A",
            text_color="#FFFFFF",
        )
        self.titular_tarjeta_entry.pack(pady=8)

        # Fecha vencimiento
        self.fecha_vencimiento_entry = ctk.CTkEntry(
            self,
            placeholder_text="Fecha de vencimiento (MM/AA)",
            width=280,
            height=42,
            corner_radius=10,
            fg_color="#313244",
            border_color="#45475A",
            text_color="#FFFFFF",
        )
        self.fecha_vencimiento_entry.pack(pady=8)

        # CVV
        self.cvv_entry = ctk.CTkEntry(
            self,
            placeholder_text="CVV (3 dígitos)",
            width=280,
            height=42,
            corner_radius=10,
            fg_color="#313244",
            border_color="#45475A",
            text_color="#FFFFFF",
        )
        self.cvv_entry.pack(pady=8)

        # Boton Finalizar
        self.boton_finalizar = ctk.CTkButton(
            self,
            text="Guardar Cambios" if self.editando else "Finalizar Registro",
            command=self.submit_register,
            width=280,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#A6E3A1",
            hover_color="#94E2D5",
            text_color="#11111B",
        )
        self.boton_finalizar.pack(pady=(20, 10))

        # Boton para volver
        volver = ctk.CTkLabel(
            self,
            text="Volver",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="#89B4FA",
            cursor="hand2",
        )
        volver.pack(pady=(5, 0))
        volver.bind(
            "<Button-1>", lambda e: self.controller.show_frame("RegisterFrame")
        )

        # Prellenar al editar
        if self.editando:
            self._prellenar()

    def _prellenar(self):
        u = self.original
        self.numero_tarjeta_entry.insert(0, str(u.numeroTarjeta or ""))
        self.titular_tarjeta_entry.insert(0, u.titularTarjeta or "")

        # Convertir de formato YYYY-MM-DD (Base de datos) a MM/AA (Interfaz)
        if u.fecha_de_vencimiento:
            venc = u.fecha_de_vencimiento
            if isinstance(venc, str):
                try:
                    venc = datetime.strptime(venc, "%Y-%m-%d")
                except ValueError:
                    venc = None

            if isinstance(venc, (datetime, date)):
                self.fecha_vencimiento_entry.insert(0, venc.strftime("%m/%y"))

        self.cvv_entry.insert(0, str(u.CVV or ""))

    def submit_register(self):
        numero = self.numero_tarjeta_entry.get().replace(" ", "").strip()
        titular = self.titular_tarjeta_entry.get().strip()
        vencimiento = self.fecha_vencimiento_entry.get().strip()
        cvv = self.cvv_entry.get().strip()

        # 1. Validar que no haya campos vacíos
        if not all([numero, titular, vencimiento, cvv]):
            messagebox.showwarning(
                "Atención", "Todos los campos son obligatorios."
            )
            return

        # 2. Validar que la tarjeta tenga exactamente 16 dígitos
        if not numero.isdigit() or len(numero) != 16:
            messagebox.showwarning(
                "Atención",
                "El número de tarjeta debe contener exactamente 16 dígitos numéricos.",
            )
            return

        # 3. Validar el formato de la fecha de vencimiento (MM/AA)
        try:
            fecha_venc = datetime.strptime(vencimiento, "%m/%y")
        except ValueError:
            messagebox.showwarning(
                "Atención",
                "La fecha de vencimiento debe tener el formato MM/AA (ejemplo: 08/28).",
            )
            return

        # Validar que la tarjeta no esté vencida respecto al mes actual
        hoy = datetime.now()
        if (fecha_venc.year, fecha_venc.month) < (hoy.year, hoy.month):
            messagebox.showwarning("Atención", "La tarjeta ingresada está vencida.")
            return

        # 4. Validar que el CVV sea exactamente de 3 dígitos
        if not cvv.isdigit() or len(cvv) != 3:
            messagebox.showwarning(
                "Atención", "El CVV debe contener exactamente 3 dígitos numéricos."
            )
            return

        # Cargar datos de usuario de la pantalla anterior o del objeto editado
        # Cargar datos de usuario de la pantalla anterior o del objeto editado
        if self.editando:
            datos_usuario = {
                "username": self.original.username,
                "nombre": self.original.nombre,
                "apellidos": self.original.apellidos,
                "password": self.original.password,
                "email": self.original.email,
                "admin": self.original.admin,
                "numero_Telefono": getattr(self.original, 'numero_Telefono', None),
                "FechaNacimiento": getattr(self.original, 'FechaNacimiento', None),
            }
        else:
            datos_usuario = self.controller.datos_registro

        datos = {
            **datos_usuario,
            "numeroTarjeta": numero,
            "titularTarjeta": titular,
            "fecha_de_vencimiento": fecha_venc.strftime(
                "%Y-%m-%d"
            ),  # Formato guardado en BD
            "CVV": cvv,
        }

        # Llamada al DAO (Insertar o Actualizar)
        try:
            if self.editando:
                ok = self.controller.dao.update_user(
                    self.original.username, Usuario(**datos)
                )
            else:
                ok = self.controller.dao.insert_user(Usuario(**datos))
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo completar la operación: {e}"
            )
            return

        if not ok:
            messagebox.showerror(
                "Error", "El nombre de usuario o correo ya existe."
            )
            self.controller.show_frame("RegisterFrame")
            return

        # Refrescar la sesión si el administrador se edita a sí mismo
        if (
            self.editando
            and self.original.username == self.controller.usuario_actual.username
        ):
            self.controller.usuario_actual = self.controller.dao.get_user(
                self.original.username
            )

        # Limpiar datos en memoria y finalizar
        self.controller.terminar_flujo()

        if self.editando:
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            self.controller.show_frame("ListaFrame")
        else:
            messagebox.showinfo("Éxito", "¡Registro completado!")
            destino = (
                "ListaFrame" if self.controller.usuario_actual else "LoginFrame"
            )
            self.controller.show_frame(destino)