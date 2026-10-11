import customtkinter as ctk
from tkinter import messagebox

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, corner_radius=15, fg_color="#1E1E2E")
        self.controller = controller

        # titulo
        ctk.CTkLabel(
            self, text="¡Bienvenido!",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self, text="Inicia sesión en tu cuenta",
            font=ctk.CTkFont(size=13),
            text_color="#A6ADC8"
        ).pack(pady=(0, 25))

        # campos de entrada
        # Usuario
        self.user_entry = ctk.CTkEntry(
            self, placeholder_text="Usuario o Email",
            width=280, height=45, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.user_entry.pack(pady=10)
        # Contrasenia
        self.pass_entry = ctk.CTkEntry(
            self, placeholder_text="Contraseña", show="•",
            width=280, height=45, corner_radius=10,
            fg_color="#313244", border_color="#45475A", text_color="#FFFFFF"
        )
        self.pass_entry.pack(pady=10)


        # iniciar sesion
        ctk.CTkButton(
            self, text="Iniciar Sesión", command=self.submit_login,
            width=280, height=45, corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#89B4FA", hover_color="#74C7EC", text_color="#11111B"
        ).pack(pady=10)

        # enlace a registro
        toggle_label = ctk.CTkLabel(
            self, text="¿No tienes cuenta? Regístrate aquí",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="#89B4FA", cursor="hand2"
        )
        toggle_label.pack(pady=(20, 0))
        toggle_label.bind("<Button-1>", lambda e: self.controller.iniciar_registro())
    def submit_login(self):
        user = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not user or not password:
            messagebox.showwarning("Atención", "Por favor, ingresa tu usuario y contraseña.")
            return
        
        usuario_logueado = self.controller.dao.get_userByPassword(user, password)

        if usuario_logueado:
            # Validar si el usuario está dado de baja
            if not usuario_logueado.UsuarioActivo:
                messagebox.showerror("Error", "Esta cuenta está dada de baja.")
                return

            # Guardar el objeto Usuario en el controlador principal
            self.controller.usuario_actual = usuario_logueado
            messagebox.showinfo("Éxito", f"¡Bienvenido, {usuario_logueado.nombre}!")

            self.controller.show_frame("ListaFrame")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
