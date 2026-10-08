import customtkinter as ctk
from tkinter import messagebox

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

        # titulo
        ctk.CTkLabel(
            self, text="Crear Cuenta",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self, text="Completa tus datos para registrarte",
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
            self, placeholder_text="Nombre de Usuario",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.lastname_entry.pack(pady=8)
        # Fecha de nacimiento
        self.birth_entry = ctk.CTkEntry(
            self, placeholder_text="Fecha de nacimiento",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.birth_entry.pack(pady=8)
        # Correo
        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="Correo Electrónico",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.email_entry.pack(pady=8)
        
        # Telefono
        self.phone_entry = ctk.CTkEntry(
            self, placeholder_text="Telefono",
            width=280, height=42, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.phone_entry.pack(pady=8)
        # Contrasenia
        self.pass_entry = ctk.CTkEntry(
            self, placeholder_text="Contraseña", show="•",
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
        admin_var = ctk.StringVar(value = 'off')
        self.admin_entry = ctk.CTkSwitch(
            self, text="ADMIN",
            width=280, height=22, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF",
            variable = admin_var,
            onvalue = 'on',
            offvalue = 'off'
        )
        self.admin_entry.pack(pady=8)

        # boton continuar
        ctk.CTkButton(
            self, text="Continuar", command=self.submit_register,
            width=280, height=45, corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#A6E3A1", hover_color="#94E2D5", text_color="#11111B"
        ).pack(pady=(20, 10))

        # enlace a login
        toggle_label = ctk.CTkLabel(
            self, text="¿Ya tienes cuenta? Inicia sesión",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="#89B4FA", cursor="hand2"
        )
        toggle_label.pack(pady=(10, 0))
        toggle_label.bind("<Button-1>", lambda e: self.controller.show_frame("LoginFrame"))

    def submit_register(self):
        user = self.user_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        confirm_pass = self.confirm_pass_entry.get().strip()

        if not user or not email or not password or not confirm_pass:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Atención", "Por favor ingresa un correo electrónico válido.")
            return

        if user in self.controller.users_db:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            return

        if password != confirm_pass:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        self.controller.users_db[user] = password
        messagebox.showinfo("Éxito", "Por favor ingrese sus datos de tarjeta")
        self.controller.show_frame("TarjetaFrame")