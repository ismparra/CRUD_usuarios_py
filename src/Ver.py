import customtkinter as ctk
from datetime import datetime
from dao import usuario

class VistFrame(ctk.CTkScrollableFrame):
  def __init__(self, master, controller):
    super().__init__(master, corner_radius =15, fg_color="1E1E2E", scrollbar_button_color="45475A", scrollbar_button_hover_color="89B4FA")
    self.controller = controller
    self.es_admin = False
    if self.controller.usuario_actual:
      self.es_admin = self.controller.usuario_actual.admin

    # titulo
        ctk.CTkLabel(
            self, text="Información del usuario",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(25, 5))
