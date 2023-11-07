import tkinter as tk
# import os
# import qrcode
import requests


API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

def autorizacion() -> dict:
    
    Headers: dict = { "Authorization" : f"Bearer {API_KEY}" }

    return Headers

def get_cinemas(Headers: dict) -> list[dict]:

    r_ubicacion = requests.get("http://vps-3701198-x.dattaweb.com:4000/cinemas", headers=Headers)
    info_cinemas: list[dict] = r_ubicacion.json()

    return info_cinemas

def main() -> None:
    
    Headers = autorizacion()

    info_cinemas = get_cinemas(Headers)

main()


# ventana = tk.Tk(className = "Cartelera")
# ventana.geometry("500x500")

# ubicacion = tk.Label(ventana, text = "Palermo, Belgrano, Villa Crespo")
# ubicacion.pack()


# ventana.mainloop()