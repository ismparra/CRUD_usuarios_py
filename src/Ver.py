import customtkinter as ctk

class VistFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(master, corner_radius =15, fg_color="#1E1E2E", scrollbar_button_color="#45475A", scrollbar_button_hover_color="#89B4FA")
        self.controller = controller
        self.es_admin = False
        
        if self.controller.usuario_actual:
            self.es_admin = self.controller.usuario_actual.admin

        user_A_Ver = getattr(self.controller, 'usuario_viendo', None)

        if not user_A_Ver:
            ctk.CTkLabel(
                self, text="Error: No se ha seleccionado un usuario para ver.", 
                font=ctk.CTkFont(size=15), text_color="#FFFFFF"
            ).pack(pady=10)
            return

        # Si es que el usuario esta revisando su propia info puede verla sin censura
        es_Propio = (self.controller.usuario_actual and self.controller.usuario_actual.username == user_A_Ver.username)

        if self.es_admin or es_Propio:
            usuario_Completo = self.controller.dao.get_user_con_tarjeta(user_A_Ver.username)
        else:
            usuario_Completo = user_A_Ver

        # Título 
        ctk.CTkLabel(
            self, text=f"Información de {usuario_Completo.username}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        ).pack(pady=(25, 5), padx=20, fill="x")

        # Contenedores de datos
        datos_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=10)
        datos_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Base para mostrar los datos
        def mostrar_dato(label, valor):
            fila = ctk.CTkFrame(datos_frame, fg_color="transparent")
            fila.pack(fill="x", pady=8, padx=15)
            # Ancho (width) de 180 para evitar que el texto grande se encime
            ctk.CTkLabel(fila, text=f"{label}:", font=ctk.CTkFont(size=15, weight="bold"), text_color="#A6ADC8", width=180, anchor="w").pack(side="left")
            ctk.CTkLabel(fila, text=str(valor), font=ctk.CTkFont(size=15), text_color="#FFFFFF", anchor="w", wraplength=500).pack(side="left", fill="x", expand=True)

        # Datos generales
        mostrar_dato("Nombre Completo", f"{usuario_Completo.nombre} {usuario_Completo.apellidos}")
        mostrar_dato("Correo Electrónico", usuario_Completo.email)
        mostrar_dato("Teléfono", usuario_Completo.numero_Telefono)
        mostrar_dato("Estado", "Activo" if usuario_Completo.UsuarioActivo else "Dado de baja")
        mostrar_dato("Rol", "Administrador" if usuario_Completo.admin else "Usuario Regular")

        # Datos más sensibles, solo para admins o el propio usuario
        if self.es_admin:
            
            # Subtítulo 
            ctk.CTkLabel(
                datos_frame, text="- Información Privada -", 
                text_color="#F38BA8", font=ctk.CTkFont(size=18, weight="bold"),
                anchor="w"
            ).pack(pady=(20, 10), padx=15, fill="x")
            
            mostrar_dato("Fecha de Nacimiento", usuario_Completo.FechaNacimiento)      
            
            # password
            hash_pass = usuario_Completo.password if usuario_Completo.password else "No disponible"
            mostrar_dato("Hash Contraseña (SHA256)", hash_pass)      
            
            # Datos de la tarjeta
            mostrar_dato("Número de Tarjeta", usuario_Completo.numeroTarjeta)
            mostrar_dato("Titular de Tarjeta", usuario_Completo.titularTarjeta)
            mostrar_dato("Fecha de Vencimiento", usuario_Completo.fecha_de_vencimiento)
            mostrar_dato("CVV", usuario_Completo.CVV)

            # Timestamps
            ctk.CTkLabel(
                datos_frame, text="- Registros del Sistema -", 
                text_color="#F9E2AF", font=ctk.CTkFont(size=18, weight="bold"),
                anchor="w"
            ).pack(pady=(20, 10), padx=15, fill="x")
            
            mostrar_dato("Fecha de Creación ", usuario_Completo.created_at)
            mostrar_dato("Última Actualización ", usuario_Completo.updated_at)
            mostrar_dato("Último Inicio de Sesión ", usuario_Completo.last_login)

        # Botón volver
        ctk.CTkButton(
            self, text="Volver", command=lambda: self.controller.show_frame("ListaFrame"),
            width=200, height=40, corner_radius=15, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#89B4FA", hover_color="#74C7EC", text_color="#11111B"
        ).pack(pady=20)
