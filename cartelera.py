import tkinter as tk
# import os
# import qrcode
import requests


API_KEY: int = 1 #Todavia no esta

# GET /cinemas/{cinema_id}/movies
# Request headers:
# “Authorization”: “Bearer token”
# Response type: JSON
# Response body:


r = requests.get("https://cinemas")
r_json = r.json()


ventana = tk.Tk(className = "Cartelera")
ventana.geometry("500x500")

ubicacion = tk.Label(ventana, text = "Palermo, Belgrano, Villa Crespo")
ubicacion.pack()

print("prueba rama")

ventana.mainloop()