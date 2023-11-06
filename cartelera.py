import tkinter as tk
# import os
# import qrcode

# GET /cinemas/{cinema_id}/movies
# Request headers:
# “Authorization”: “Bearer token”
# Response type: JSON
# Response body:

ventana = tk.Tk(className = "Cartelera")
ventana.geometry("500x500")

ubicacion = tk.Label(ventana, text = "Palermo, Belgrano, Villa Crespo")
ubicacion.pack()

print("hola")

ventana.mainloop()