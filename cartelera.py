import tkinter as tk
# import os
# import qrcode
import requests


API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

Headers = { "Authorization" : API_KEY }

r = requests.get("https://cinemas", headers=Headers)
r_json = r.json()


ventana = tk.Tk(className = "Cartelera")
ventana.geometry("500x500")

ubicacion = tk.Label(ventana, text = "Palermo, Belgrano, Villa Crespo")
ubicacion.pack()

print("pepe")

ventana.mainloop()