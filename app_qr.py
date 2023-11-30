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

        self.mostrar_frame(MenuPrincipal)

    def mostrar_frame(self, clase) -> None:
        '''
        Pre: Recibe la clase
        Post: Cambia al frame que se recibe por parametro
        '''
         
        frame = self.frames[clase]
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

        boton_camara = tk.Button(
            self,
            text="Leer QR",
            command=lambda: controller.mostrar_frame(LeerQR),
        )
        boton_camara.pack(side="bottom", fill=tk.X)

        boton_id = tk.Button(
            self,
            text="Ingresar ID",
            command=lambda: controller.mostrar_frame(IngresarID),
        )
        boton_id.pack(side="bottom", fill=tk.X)


class IngresarID(tk.Frame):
    
    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Ingresar ID")
        label.pack(padx=10, pady=10)

        volver_al_menu = tk.Button(
            self,
            text="Volver al menu",
            command=lambda: controller.mostrar_frame(MenuPrincipal),
        )
        volver_al_menu.pack(side="bottom", fill=tk.X)

        validacion = (self.register(validar_mensaje), "%P")

        entry = tk.Entry(self, width=35, borderwidth=2, validate = "key", validatecommand = validacion)
        entry.pack(padx=10, pady=10, fill=tk.X)

        entry_boton = tk.Button(
            self,
            text="OK",
            command=lambda: (detectar_qr_archivo(entry.get()), entry.delete(0, tk.END)),
        )
        entry_boton.pack(padx=10, pady=10, fill=tk.X)


class LeerQR(tk.Frame):

    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Leer QR")
        label.pack(padx=10, pady=10)

        volver_al_menu = tk.Button(
            self,
            text="Volver al menu",
            command=lambda: controller.mostrar_frame(MenuPrincipal),
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
    '''
        Pre: Recibe un texto de str
        Post: Valida que el texto sea el deseado y 
        devuelve true si lo es 
    '''

    validacion: bool = False
    
    if texto.isnumeric() == True or texto == "":
        validacion = True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números enteros.")

    return validacion


def guardar(informacion: str) -> None:
    '''
    Pre: Recibe un str de informacion
    Post: Escribi la inforamcion recibida en el archivo ingresos.txt
    '''
    
    with open("ingresos.txt", "a") as archivo:
    
        linea = informacion + "\n"
        archivo.write(linea)
    
    messagebox.showinfo("Info", "Se leyo el QR correctamente")


def extraer_datos(string: str) -> str: 
    '''
    Pre: Recibe un string
    Post: Devuelve un str con la informacion del qr ordenada
    '''
    
    lista_datos = string.split("_")
    
    id_qr = lista_datos[0]
    nombre_pelicula = lista_datos[1]
    cant_entradas = lista_datos[3]
    total_consumido = lista_datos[4]
    timestamp = lista_datos[5]
    
    string_ordenado = f"{timestamp}, {id_qr}, {nombre_pelicula}, {cant_entradas}, {total_consumido}"

    return string_ordenado


def detectar_qr_archivo(id_qr: str) -> None:
    '''
    Pre: REcibe un str de id_qr
    Post: Lee y guarde la informacion del qr, si el id ingresado
    es incorrecto se le indica al usuario 
    '''
    
    if os.path.isfile(f"QR/qr{id_qr}.pdf"):
    
        img = cv2.imread(f"QR/qr{id_qr}.pdf")
        detectar = cv2.QRCodeDetector()
        valor = detectar.detectAndDecode(img)
        guardar(extraer_datos(valor[0]))
    
    else:
        messagebox.showerror("Error", "El ID especificado no existe.")


def detectar_qr_webcam() -> None:
    '''
    Pre: XXX
    Post: Lee con la camara el qr proporcionado y guarda la informacion
    '''
    
    camara_id: int = 0
    delay: int = 1
    nombre_ventana: str = 'OpenCV QR Code'

    qcd = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(camara_id)

    exit: bool = False

    if cap.isOpened():
    
        while not exit:
            ret, frame = cap.read()

            if ret:
    
                ret_qr, decoded_info, _, _ = qcd.detectAndDecodeMulti(frame)
    
                if ret_qr and decoded_info[0]:
    
                    guardar(extraer_datos(decoded_info[0]))
                    exit = True
    
                cv2.imshow(nombre_ventana, frame)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                exit = True

        cv2.destroyWindow(nombre_ventana)
    
    else:
        messagebox.showerror("Error", "Camara no detectada.")


def main() -> None:
    
    app = ventanas()
    app.mainloop()

main()
