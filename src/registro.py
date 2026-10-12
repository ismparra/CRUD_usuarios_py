import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class RegisterFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            corner_radius=15,
            fg_color="#1E1E2E",
            scrollbar_button_color="#45475A",
            scrollbar_button_hover_color="#89B4FA",
        )
        self.controller = controller
        self.editando = controller.modo == "editar"
        self.original = controller.usuario_editando
        # titulo
        ctk.CTkLabel(
            self, text=f"Modificar a {self.original.username}" if self.editando else "Crear Cuenta",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self, text="Completa tus datos",
            font=ctk.CTkFont(size=13),
            text_color="#A6ADC8"
        ).pack(pady=(0, 20))

        # campos de entrada
        # Usuario
        self.user_entry = ctk.CTkEntry(
            self, placeholder_text="Nombre de Usuario",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.user_entry.pack(pady=8)
        # Nombre
        self.name_entry = ctk.CTkEntry(
            self, placeholder_text="Nombre Personal",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.name_entry.pack(pady=8)
        # Apellidos
        self.lastname_entry = ctk.CTkEntry(
            self, placeholder_text="Apellidos",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.lastname_entry.pack(pady=8)
        # Fecha de nacimiento
        self.birth_entry = ctk.CTkEntry(
            self, placeholder_text="Fecha de nacimiento (DD/MM/AAAA)",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.birth_entry.pack(pady=8)
        # Correo
        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="Correo Electrónico (example@email.com)",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.email_entry.pack(pady=8)
        
        # Telefono
        self.phone_entry = ctk.CTkEntry(
            self, placeholder_text="Telefono (10 dígitos)",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.phone_entry.pack(pady=8)
        # Contrasenia
        self.pass_entry = ctk.CTkEntry(
            self, placeholder_text="Nueva contraseña (vacío = no cambiar)" if self.editando else "Contraseña", show="•",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.pass_entry.pack(pady=8)
        # Confirmacion constrasenia
        self.confirm_pass_entry = ctk.CTkEntry(
            self, placeholder_text="Confirmar Contraseña", show="•",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.confirm_pass_entry.pack(pady=8)
        
        
        # es admin
        self.admin_var = ctk.StringVar(value = 'off')
        self.admin_entry = ctk.CTkSwitch(
            self, text="ADMIN",
            width=280, height=22, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF",
            variable = self.admin_var,
            onvalue = 'on',
            offvalue = 'off'
        )
        # es admin (solo visible para administradores)
        if self.controller.usuario_actual and self.controller.usuario_actual.admin:
            self.admin_entry.pack(pady=8)

        # boton continuar
        ctk.CTkButton(
            self, text="Continuar", command=self.submit_register,
            width=280, height=45, corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#A6E3A1", hover_color="#94E2D5", text_color="#11111B"
        ).pack(pady=(20, 10))

        # enlace a login
        destino = "ListaFrame" if (self.editando or self.controller.usuario_actual) else "LoginFrame"
        toggle_label = ctk.CTkLabel(
            self, text="Cancelar" if destino == "ListaFrame" else "¿Ya tienes cuenta? Inicia sesion",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="#89B4FA", cursor="hand2"
        )
        toggle_label.pack(pady=(10, 0))
        toggle_label.bind("<Button-1>", lambda e: self._cancelar(destino))
        self._prellenar()

    def _prellenar(self):
        campos = ["username", "nombre", "apellidos", "FechaNacimiento",
                "email", "numero_Telefono", "admin"]
        if self.controller.datos_registro:
            fuente = self.controller.datos_registro
        elif self.editando:
            fuente = {k: getattr(self.original, k) for k in campos}
        else:
            return

        fecha = datetime.strptime(str(fuente["FechaNacimiento"]), "%Y-%m-%d").strftime("%d/%m/%Y")

        self.user_entry.insert(0, fuente["username"])
        self.name_entry.insert(0, fuente["nombre"])
        self.lastname_entry.insert(0, fuente["apellidos"])
        self.birth_entry.insert(0, fecha)
        self.email_entry.insert(0, fuente["email"])
        self.phone_entry.insert(0, fuente["numero_Telefono"])
        self.admin_var.set("on" if fuente["admin"] else "off")

    def _cancelar(self, destino):
        if self.editando:
            self.controller.terminar_flujo()
        self.controller.show_frame(destino)

    def submit_register(self):
        user = self.user_entry.get().strip()
        name = self.name_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        birth = self.birth_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.pass_entry.get().strip()
        confirm_pass = self.confirm_pass_entry.get().strip()
        is_admin = self.admin_var.get() == 'on'

        # Campos obligatorios
        campos = [user, name, lastname, birth, email, phone]
        if not self.editando:
            campos += [password, confirm_pass]
        if not all(campos):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        # Fecha de nacimiento (formato DD/MM/AAAA)
        try:
            birth_date = datetime.strptime(birth, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showwarning("Atención", "La fecha debe tener el formato DD/MM/AAAA.")
            return

        if birth_date > datetime.now().date():
            messagebox.showwarning("Atención", "La fecha de nacimiento no puede ser futura.")
            return

        # Correo
        if "@" not in email or "." not in email:
            messagebox.showwarning("Atención", "Por favor ingresa un correo electrónico válido.")
            return

        # Teléfono (10 dígitos)
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning("Atención", "El teléfono debe tener 10 dígitos numéricos.")
            return

        # Contraseña (al editar solo se valida si escribieron una nueva)
        if password or not self.editando:
            if len(password) < 6:
                messagebox.showwarning("Atención", "La contraseña debe tener al menos 6 caracteres.")
                return

            if password != confirm_pass:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return

        # Solo se guardan en memoria; todavía NO se envían a la BD
        self.controller.datos_registro = {
            "username": user,
            "nombre": name,
            "apellidos": lastname,
            "FechaNacimiento": birth_date.strftime("%Y-%m-%d"),
            "email": email,
            "numero_Telefono": phone,
            "password": password or None,   # None = el usuario no quiere cambiar la contrasena
            "admin": is_admin,
        }

        if not self.editando:
            messagebox.showinfo("Éxito", "Por favor ingrese sus datos de tarjeta")
        self.controller.show_frame("TarjetaFrame")
