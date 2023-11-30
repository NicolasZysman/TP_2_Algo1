import tkinter as tk
from tkinter import messagebox
import os
import cv2

class ventanas(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.wm_title("App QR")
        self.geometry("300x300")
        
        container = tk.Frame(self, height=300, width=300)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (MenuPrincipal, IngresarID, LeerQR):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MenuPrincipal)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MenuPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Menu principal")
        label.pack(padx=10, pady=10)
        
        salir = tk.Button(
            self,
            text="Salir",
            command=controller.destroy
        )
        salir.pack(side="bottom", fill=tk.X)

        switch_window_button1 = tk.Button(
            self,
            text="Leer QR",
            command=lambda: controller.show_frame(LeerQR),
        )
        switch_window_button1.pack(side="bottom", fill=tk.X)

        switch_window_button2 = tk.Button(
            self,
            text="Ingresar ID",
            command=lambda: controller.show_frame(IngresarID),
        )
        switch_window_button2.pack(side="bottom", fill=tk.X)


class IngresarID(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Ingresar ID")
        label.pack(padx=10, pady=10)

        volver_al_menu = tk.Button(
            self,
            text="Volver al menu",
            command=lambda: controller.show_frame(MenuPrincipal),
        )
        volver_al_menu.pack(side="bottom", fill=tk.X)

        validacion = (self.register(validar_mensaje), "%P")

        entry = tk.Entry(self, width=35, borderwidth=2, validate = "key", validatecommand = validacion)
        entry.pack(padx=10, pady=10, fill=tk.X)

        entry_button = tk.Button(
            self,
            text="OK",
            command=lambda: (detectar_qr_archivo(entry.get()), entry.delete(0, tk.END)),
        )
        entry_button.pack(padx=10, pady=10, fill=tk.X)


class LeerQR(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Leer QR")
        label.pack(padx=10, pady=10)

        volver_al_menu = tk.Button(
            self,
            text="Volver al menu",
            command=lambda: controller.show_frame(MenuPrincipal),
        )
        volver_al_menu.pack(side="bottom", fill=tk.X)

        instrucciones = tk.Label(self, text="Click para escanear el QR con la webcam.\nPresione 'q' para cancelar.")
        instrucciones.pack(side="bottom", padx=10, pady=30, fill=tk.X)

        escanear = tk.Button(
            self,
            text="Escanear QR",
            command=lambda: detectar_qr_webcam(),
        )
        escanear.pack(side="bottom", padx=10, pady=10, fill=tk.X)

def validar_mensaje(texto: str) -> bool:
    validacion: bool = False
    if texto.isnumeric() == True or texto == "":
        validacion = True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números enteros.")

    return validacion

def guardar(informacion: str): # timestamp, Id_QR, nombre_pelicula, cant_entradas, total_consumido
    with open("ingresos.txt", "a") as archivo:
        linea = informacion + "\n"
        archivo.write(linea)
    messagebox.showinfo("Info", "Se leyo el QR correctamente")

def extraer_datos(string): # Id_QR, nombre_pelicula, ubicacion, cant_entradas, total_consumido, timestamp
    lista_datos = string.split("_")
    
    id_qr = lista_datos[0]
    nombre_pelicula = lista_datos[1]
    cant_entradas = lista_datos[3]
    total_consumido = lista_datos[4]
    timestamp = lista_datos[5]
    
    string_ordenado = f"{timestamp}, {id_qr}, {nombre_pelicula}, {cant_entradas}, {total_consumido}"

    return string_ordenado

def detectar_qr_archivo(id_qr: str):
    if os.path.isfile(f"QR/qr{id_qr}.pdf"):
        img = cv2.imread(f"QR/qr{id_qr}.pdf")
        detect = cv2.QRCodeDetector()
        value = detect.detectAndDecode(img)
        guardar(extraer_datos(value[0]))
    else:
        messagebox.showerror("Error", "El ID especificado no existe.")

def detectar_qr_webcam():
    camera_id = 0
    delay = 1
    window_name = 'OpenCV QR Code'

    qcd = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(camera_id)

    exit = False

    if cap.isOpened():
        while not exit:
            ret, frame = cap.read()

            if ret:
                ret_qr, decoded_info, _, _ = qcd.detectAndDecodeMulti(frame)
                if ret_qr and decoded_info[0]:
                    guardar(extraer_datos(decoded_info[0]))
                    exit = True
                cv2.imshow(window_name, frame)

            if cv2.waitKey(delay) & 0xFF == ord('q'): # q para salir
                exit = True

        cv2.destroyWindow(window_name)
    else:
        messagebox.showerror("Error", "Camara no detectada.")

def main():
    app = ventanas()
    app.mainloop()

main()