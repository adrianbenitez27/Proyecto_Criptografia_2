import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import GCM_ECDH as procesos

ruta_llave_privada = ""
ruta_llave_publica = ""
ruta_secreto_aes_cif = ""
ruta_secreto_aes_des = ""
ruta_documento_cif = ""
ruta_documento_des = ""

def reiniciar_rutas():
    global ruta_llave_privada, ruta_llave_publica, ruta_secreto_aes_cif, ruta_secreto_aes_des, ruta_documento_cif, ruta_documento_des
    ruta_llave_privada = ""
    ruta_llave_publica = ""
    ruta_secreto_aes_cif = ""
    ruta_secreto_aes_des = ""
    ruta_documento_cif = ""
    ruta_documento_des = ""
    etiqueta_llave_privada.config(text="")
    etiqueta_llave_publica.config(text="")
    etiqueta_secreto_aes_cif.config(text="")
    etiqueta_secreto_aes_des.config(text="")
    etiqueta_documento_cif.config(text="")
    etiqueta_documento_des.config(text="")

def seleccionar_llave_privada():
    global ruta_llave_privada
    ruta_llave_privada = filedialog.askopenfilename(title="Seleccione una clave privada")
    etiqueta_llave_privada.config(text=ruta_llave_privada)

def seleccionar_llave_publica():
    global ruta_llave_publica
    ruta_llave_publica = filedialog.askopenfilename(title="Seleccione una clave pública")
    etiqueta_llave_publica.config(text=ruta_llave_publica)

def seleccionar_sereto_aes_cif():
    global ruta_secreto_aes_cif
    ruta_secreto_aes_cif = filedialog.askopenfilename(title="Seleccione el secreto AES")
    etiqueta_secreto_aes_cif.config(text=ruta_secreto_aes_cif)

def seleccionar_sereto_aes_des():
    global ruta_secreto_aes_des
    ruta_secreto_aes_des = filedialog.askopenfilename(title="Seleccione el secreto AES")
    etiqueta_secreto_aes_des.config(text=ruta_secreto_aes_des)

def seleccionar_documento_cif():
    global ruta_documento_cif
    ruta_documento_cif = filedialog.askopenfilename(title="Seleccione un archivo a cifrar")
    etiqueta_documento_cif.config(text=ruta_documento_cif)

def seleccionar_documento_des():
    global ruta_documento_des
    ruta_documento_des = filedialog.askopenfilename(title="Seleccione un archivo a descifrar")
    etiqueta_documento_des.config(text=ruta_documento_des)

def generar_llaves():
    clave_privada_A, clave_publica_A = procesos.generar_par_claves_ecdh()

    nom_cla = simpledialog.askstring("Guardado de claves", "Ingresa su nombre para identificar las claves:")
    if nom_cla:
        procesos.serializar_claves(clave_publica_A, clave_privada_A, nom_cla)
        messagebox.showinfo("Éxito", "Llaves generadas")
    else:
        messagebox.showinfo("Error", "Debe ingresar un nombre válido para las claves")

def calcular_secreto():
    clave_publica_recibida_B = procesos.deserializar_clave(ruta_llave_publica, 0)
    clave_privada_A = procesos.deserializar_clave(ruta_llave_privada, 1)

    secreto_compartido_A = procesos.calcular_secreto_compartido(clave_privada_A, clave_publica_recibida_B)
    procesos.derivar_clave_aes(secreto_compartido_A)

    messagebox.showinfo("Éxito", "Secreto AES calculado")

def cifra():
    procesos.cifrar_archivo_gcm(ruta_documento_cif, ruta_secreto_aes_cif)
    reiniciar_rutas()

    messagebox.showinfo("Éxito", "Cifrado correcto")

def descifra():
    procesos.descifrar_archivo_gcm(ruta_documento_des, ruta_secreto_aes_des)
    reiniciar_rutas()

    messagebox.showinfo("Éxito", "Descifrado correcto")

root = tk.Tk()
root.title("Interfaz para retrato digital")

# Marco para generar llaves
marco_generar_llaves = tk.LabelFrame(root, text="Generar Llaves", padx=5, pady=5)
marco_generar_llaves.pack(padx=10, pady=10, fill="both", expand="yes", side="top")

boton_generar = tk.Button(marco_generar_llaves, text="Generar Llaves", command=generar_llaves)
boton_generar.pack(pady=10)

# Marco para calcular secreto aes
marco_calcular_secreto = tk.LabelFrame(root, text="Calcular secreto AES", padx=5, pady=5)
marco_calcular_secreto.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

btn_seleccionar_llave_publica = tk.Button(marco_calcular_secreto, text="Seleccionar Clave Pública de B", command=seleccionar_llave_publica)
btn_seleccionar_llave_publica.pack(pady=1)
etiqueta_llave_publica = tk.Label(marco_calcular_secreto, text="")
etiqueta_llave_publica.pack(pady=1)

btn_seleccionar_llave_privada = tk.Button(marco_calcular_secreto, text="Seleccionar Clave Privada de A", command=seleccionar_llave_privada)
btn_seleccionar_llave_privada.pack(pady=1)
etiqueta_llave_privada = tk.Label(marco_calcular_secreto, text="")
etiqueta_llave_privada.pack(pady=1)

boton_calcular_aes = tk.Button(marco_calcular_secreto, text="Calcular Secreto AES", command=calcular_secreto)
boton_calcular_aes.pack(pady=10)

# Marco para cifrar por GCM
marco_cifrar = tk.LabelFrame(root, text="Cifrar Archivo", padx=5, pady=5)
marco_cifrar.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

btn_seleccionar_secreto_aes_cif = tk.Button(marco_cifrar, text="Seleccionar Secreto AES", command=seleccionar_sereto_aes_cif)
btn_seleccionar_secreto_aes_cif.pack(pady=1)
etiqueta_secreto_aes_cif = tk.Label(marco_cifrar, text="")
etiqueta_secreto_aes_cif.pack(pady=1)

btn_seleccionar_documento_cif = tk.Button(marco_cifrar, text="Seleccionar Documento", command=seleccionar_documento_cif)
btn_seleccionar_documento_cif.pack(pady=1)
etiqueta_documento_cif = tk.Label(marco_cifrar, text="")
etiqueta_documento_cif.pack(pady=1)

boton_cifrar = tk.Button(marco_cifrar, text="Cifrar Archivo", command=cifra)
boton_cifrar.pack(pady=10)

# Marco para descifrar por GCM
marco_descifrar = tk.LabelFrame(root, text="Descifrar Archivo", padx=5, pady=5)
marco_descifrar.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

btn_seleccionar_secreto_aes_des = tk.Button(marco_descifrar, text="Seleccionar Secreto AES", command=seleccionar_sereto_aes_des)
btn_seleccionar_secreto_aes_des.pack(pady=1)
etiqueta_secreto_aes_des = tk.Label(marco_descifrar, text="")
etiqueta_secreto_aes_des.pack(pady=1)

btn_seleccionar_documento_des = tk.Button(marco_descifrar, text="Seleccionar Documento", command=seleccionar_documento_des)
btn_seleccionar_documento_des.pack(pady=1)
etiqueta_documento_des = tk.Label(marco_descifrar, text="")
etiqueta_documento_des.pack(pady=1)

boton_descifrar = tk.Button(marco_descifrar, text="Descifrar Archivo", command=descifra)
boton_descifrar.pack(pady=1)

# Marco para firmar con ECDSA
marco_firmar = tk.LabelFrame(root, text="Firmar Solicitud", padx=5, pady=5)
marco_firmar.pack(padx=10, pady=10, fill="both", expand="yes")

btn_seleccionar_secreto_aes_des = tk.Button(marco_firmar, text="Seleccionar Secreto AES", command=seleccionar_sereto_aes_des)
btn_seleccionar_secreto_aes_des.pack(pady=1)
etiqueta_secreto_aes_des = tk.Label(marco_firmar, text="")
etiqueta_secreto_aes_des.pack(pady=1)

btn_seleccionar_documento_des = tk.Button(marco_firmar, text="Seleccionar Documento", command=seleccionar_documento_des)
btn_seleccionar_documento_des.pack(pady=1)
etiqueta_documento_des = tk.Label(marco_firmar, text="")
etiqueta_documento_des.pack(pady=1)

boton_descifrar = tk.Button(marco_firmar, text="Firmar Documento", command=descifra)
boton_descifrar.pack(pady=1)

root.mainloop()