import customtkinter as ctk
from tkinter import messagebox
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
        print("Terminado")
        return