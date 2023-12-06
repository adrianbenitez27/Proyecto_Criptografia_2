import tkinter as tk
from tkinter import messagebox, simpledialog
import GCM_ECDH as procesos
import requests

def generar_llaves():
    clave_privada_A, clave_publica_A = procesos.generar_par_claves_ecdh()
    nom_cla = "pintor"
    if nom_cla:
        ruta_clave_publica = procesos.serializar_claves(clave_publica_A, clave_privada_A, nom_cla)[0]  # Asegúrate de seleccionar solo la ruta de la clave pública
        with open(ruta_clave_publica, "rb") as f:
            files = {'file': f}
            response = requests.post('http://localhost:5000/upload/key', files=files)
            if response.ok:
                messagebox.showinfo("Éxito", "Llaves generadas y clave pública subida")
            else:
                messagebox.showerror("Error", "No se pudo subir la clave pública")
    else:
        messagebox.showinfo("Error", "Debe ingresar un nombre válido para las claves")

root = tk.Tk()
root.title("Interfaz del pintor para generar llaves")

# Marco para generar llaves
marco_generar_llaves = tk.LabelFrame(root, text="Generar Llaves", padx=5, pady=5)
marco_generar_llaves.pack(padx=10, pady=10, fill="both", expand="yes")

boton_generar = tk.Button(marco_generar_llaves, text="Generar Llaves", command=generar_llaves)
boton_generar.pack(pady=10)

root.mainloop()