import customtkinter as ctk
from tkinter import messagebox

class ListaFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(master,corner_radius=15,fg_color="#1E1E2E",scrollbar_button_color="#45475A",scrollbar_button_hover_color="#89B4FA",)
        self.controller = controller

        self.es_admin = False
        if self.controller.usuario_actual:
            self.es_admin = self.controller.usuario_actual.admin

        # titulo
        ctk.CTkLabel(
            self, text="Lista de Usuarios",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(25, 5))

        top_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_buttons_frame.pack(pady=(0, 20), fill="x", padx=20)

        # Botón para Cerrar Sesión 
        ctk.CTkButton(
            top_buttons_frame, text="Cerrar Sesión",
            command=self.cerrar_sesion,
            width=120, height=35, corner_radius=10,
            fg_color="#45475A", hover_color="#585B70", text_color="#FFFFFF"
        ).pack(side="left", padx=5)

        # Botón Crear Nuevo Usuario
        if self.es_admin:
            ctk.CTkButton(
                top_buttons_frame, text="Crear Nuevo Usuario",
                command=self.controller.iniciar_registro,
                width=160, height=35, corner_radius=10,
                font=ctk.CTkFont(weight="bold"),
                fg_color="#A6E3A1", hover_color="#94E2D5", text_color="#11111B"
            ).pack(side="right", padx=5)

        self.lista_contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.lista_contenedor.pack(fill="both", expand=True)

        self.cargar_usuarios()

    def cerrar_sesion(self):
        self.controller.usuario_actual = None
        self.controller.show_frame("LoginFrame")
    
    def cargar_usuarios(self):
        for widget in self.lista_contenedor.winfo_children():
            widget.destroy()

        try:
            usuarios = self.controller.dao.get_all_users()
        
            if not usuarios:
                ctk.CTkLabel(self.lista_contenedor, text="No hay usuarios registrados.", text_color="#FFFFFF").pack(pady=10)
                return

            for user in usuarios:
                if not self.es_admin and user.admin:
                    continue
                card = ctk.CTkFrame(self.lista_contenedor, fg_color="#313244", corner_radius=10)
                card.pack(pady=5, padx=20, fill="x")

                # Info del usuario
                info_texto = f"{user.username}  -  {user.nombre}  |  {user.email}"
                texto_color = "#FFFFFF" if user.UsuarioActivo else"#F38BA8"
                if not user.UsuarioActivo:
                    info_texto += " | INACTIVO"
                if user.admin:
                    info_texto += " | ADMIN"

                ctk.CTkLabel(
                    card, text=info_texto, 
                    text_color=texto_color, justify="left",
                    font=ctk.CTkFont(weight="bold")
                ).pack(side="left", pady=15, padx=15)

                action_frame = ctk.CTkFrame(card, fg_color="transparent")
                action_frame.pack(side="right", padx=10)

                # Botón VER 
                ctk.CTkButton(
                    action_frame, text="Ver", width=60, height=28,
                    fg_color="#89B4FA", hover_color="#74C7EC", text_color="#11111B",
                    command=lambda u=user: self.ver_usuario(u)
                ).pack(side="left", padx=5)

                # Botones solo para los admins
                if self.es_admin:
                    # Botón Modificar
                    ctk.CTkButton(
                        action_frame, text="Modificar", width=80, height=28,
                        fg_color="#F9E2AF", hover_color="#F38BA8", text_color="#11111B",
                        command=lambda u=user: self.modificar_usuario(u)
                    ).pack(side="left", padx=5)

                    # Botón Dar de Baja (Si está activo y no es el usuario actual)
                    if user.UsuarioActivo and user.username != self.controller.usuario_actual.username:
                        ctk.CTkButton(
                            action_frame, text="Dar de Baja", width=90, height=28,
                            fg_color="#F38BA8", hover_color="#EBA0AC", text_color="#11111B",
                            command=lambda u=user: self.dar_de_baja(u)
                        ).pack(side="left", padx=5)

                    # Botón Eliminar (No autoeliminacion)
                    if user.username != self.controller.usuario_actual.username:
                        ctk.CTkButton(
                            action_frame, text="Eliminar", width=80, height=28,
                            fg_color="#ff5555", hover_color="#ff7777", text_color="#FFFFFF",
                            command=lambda u=user: self.eliminar_usuario(u)
                        ).pack(side="left", padx=5)

        except Exception as e:
            ctk.CTkLabel(self.lista_contenedor, text=f"Error de conexión: {e}", text_color="#F38BA8").pack(pady=10)
    # Metodos para los botones
    def ver_usuario(self, user):
        self.controller.usuario_viendo = user
        self.controller.show_frame("VistFrame")
        
    # Ya jala
    def modificar_usuario(self, user):
        self.controller.iniciar_edicion(user)

    def dar_de_baja(self, user):
        if messagebox.askyesno("Confirmación", f"¿Dar de baja a '{user.username}'? No podrá iniciar sesión."):
            self.controller.dao.Unsuscribe(user.username)
            messagebox.showinfo("Éxito", "Usuario dado de baja.")
            self.cargar_usuarios()

    def eliminar_usuario(self, user):
        # Doble confirmación por si te llegaras a arrepentir pillin 
        if messagebox.askyesno("¡ADVERTENCIA!", f"¿Estás seguro de ELIMINAR DEFINITIVAMENTE a '{user.username}'?"):
            self.controller.dao.DELETEUSER(user.username)
            messagebox.showinfo("Eliminado", f"El usuario {user.username} ha sido borrado")
            self.cargar_usuarios()
