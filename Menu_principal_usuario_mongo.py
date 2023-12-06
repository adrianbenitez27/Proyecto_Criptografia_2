import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import GCM_ECDH as procesos
import requests

ruta_llave_privada = ""
ruta_llave_publica = ""
ruta_secreto_aes_cif = ""
ruta_secreto_aes_des = ""
ruta_documento_cif = ""
ruta_documento_des = ""
ruta_llave_privada_firma = ""
ruta_documento_firma = ""

def reiniciar_rutas():
    global ruta_llave_privada, ruta_llave_publica, ruta_secreto_aes_cif, ruta_secreto_aes_des
    global ruta_documento_cif, ruta_documento_des, ruta_llave_privada_firma, ruta_documento_firma 
    ruta_llave_privada = ""
    ruta_llave_publica = ""
    ruta_secreto_aes_cif = ""
    ruta_secreto_aes_des = ""
    ruta_documento_cif = ""
    ruta_documento_des = ""
    ruta_llave_privada_firma = ""
    ruta_documento_firma = ""
    etiqueta_llave_privada.config(text="")
    etiqueta_llave_publica.config(text="")
    etiqueta_secreto_aes_cif.config(text="")
    etiqueta_secreto_aes_des.config(text="")
    etiqueta_documento_cif.config(text="")
    etiqueta_documento_des.config(text="")
    etiqueta_llave_privada_firma.config(text="")
    etiqueta_documento_firma.config(text="")

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

def seleccionar_llave_privada_firma():
    global ruta_llave_privada_firma
    ruta_llave_privada_firma = filedialog.askopenfilename(title="Seleccione una clave privada")
    etiqueta_llave_privada_firma.config(text=ruta_llave_privada_firma)

def seleccionar_documento_firma():
    global ruta_documento_firma
    ruta_documento_firma = filedialog.askopenfilename(title="Seleccione un archivo a firmar")
    etiqueta_documento_firma.config(text=ruta_documento_firma)

def generar_llaves():
    clave_privada_A, clave_publica_A = procesos.generar_par_claves_ecdh()

    nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre (todo en minúsculas):")
    apellido = simpledialog.askstring("Apellido", "Ingresa tu apellido (todo en minúsculas):")

    if nombre and apellido:
        nombre_claves = f"{nombre}_{apellido}"
        ruta_clave_publica, ruta_clave_privada = procesos.serializar_claves(clave_publica_A, clave_privada_A, nombre_claves)
        with open(ruta_clave_publica, "rb") as f:
            files = {'file': f}
            response = requests.post('http://localhost:5000/upload/key', files=files)
            if response.ok:
                messagebox.showinfo("Éxito", "Llaves generadas y clave pública subida")
            else:
                messagebox.showerror("Error", "No se pudo subir la clave pública")
    else:
        messagebox.showinfo("Error", "Debe ingresar un nombre y apellido válidos para las claves")

def descargar_clave_publica_pintor():
    # Aquí se realiza una solicitud GET para obtener la clave pública del pintor
    response = requests.get('http://localhost:5000/download/key/pintor')
    if response.ok:
        with open("clave_publica_P-256_pintor.pem", "wb") as file:
            file.write(response.content)
        messagebox.showinfo("Descarga Completa", "La clave pública del pintor se ha descargado correctamente.")
    else:
        messagebox.showerror("Error de Descarga", "No se pudo descargar la clave pública del pintor.")

def calcular_secreto():
    clave_publica_recibida_B = procesos.deserializar_clave(ruta_llave_publica, 0)
    clave_privada_A = procesos.deserializar_clave(ruta_llave_privada, 1)

    secreto_compartido_A = procesos.calcular_secreto_compartido(clave_privada_A, clave_publica_recibida_B)
    procesos.derivar_clave_aes(secreto_compartido_A)

    messagebox.showinfo("Éxito", "Secreto AES calculado")

def cifra():
    ruta_archivo_cifrado = procesos.cifrar_archivo_gcm(ruta_documento_cif, ruta_secreto_aes_cif)
    with open(ruta_archivo_cifrado, "rb") as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/upload/pedidos', files=files)
        if response.ok:
            messagebox.showinfo("Éxito", "Archivo cifrado y subido con éxito")
        else:
            messagebox.showerror("Error", "No se pudo subir el archivo cifrado")
    reiniciar_rutas()

def descifra():
    procesos.descifrar_archivo_gcm(ruta_documento_des, ruta_secreto_aes_des)
    reiniciar_rutas()

    messagebox.showinfo("Éxito", "Descifrado correcto")

def descargar_pedido_terminado():
    nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre (todo en minúsculas):")
    apellido = simpledialog.askstring("Apellido", "Ingresa tu apellido (todo en minúsculas):")

    if nombre and apellido:
        nombre_archivo = f"{nombre}_{apellido}_terminado.jpg.cifrado_gcm"
        response = requests.get(f'http://localhost:5000/download/pedidos_terminados/{nombre_archivo}')
        if response.ok:
            with open(nombre_archivo, "wb") as file:
                file.write(response.content)
            messagebox.showinfo("Descarga Completa", "El pedido terminado se ha descargado correctamente.")
        else:
            messagebox.showerror("Error de Descarga", "No se pudo descargar el pedido terminado.")

def firma():
    ruta_firma = procesos.firmar_documento(ruta_documento_firma, ruta_llave_privada_firma)
    
    # Subir la firma
    with open(ruta_firma, "rb") as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/upload/firmas', files=files)
        if not response.ok:
            messagebox.showerror("Error", "No se pudo subir la firma")
            return

    # Subir el documento original
    with open(ruta_documento_firma, "rb") as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/upload/solicitudes', files=files)
        if response.ok:
            messagebox.showinfo("Éxito", "Firmado correcto y subida de documento y firma exitosa")
        else:
            messagebox.showerror("Error", "No se pudo subir el documento")

    reiniciar_rutas()


root = tk.Tk()
root.title("Interfaz del cliente para retrato digital")

marco_informacion = tk.LabelFrame(root, text="Consideraciones Importantes", padx=5, pady=5)
marco_informacion.pack(padx=10, pady=10, fill="both", expand="yes", side="top")
tk.Label(marco_informacion, text="1. Para generar las llaves, ingrese su nombre y apellido en minúsculas.\n2. Las fotos a seleccionar deben ser jpg\n3. El archivo de solicitud debe tener el siguiente formato: nombre_apellido todo en minusculas y en formato .txt.").pack()

# Marco para generar llaves y descargar la clave pública del pintor
marco_generar_llaves = tk.LabelFrame(root, text="Generar Llaves y Descargar Clave Pública del Pintor", padx=5, pady=5)
marco_generar_llaves.pack(padx=10, pady=10, fill="both", expand="yes", side="top")

boton_generar = tk.Button(marco_generar_llaves, text="Generar Llaves", command=generar_llaves)
boton_generar.pack(side=tk.LEFT, padx=10, pady=10)

boton_descargar_clave_pintor = tk.Button(marco_generar_llaves, text="Descargar Clave Pública del Pintor", command=descargar_clave_publica_pintor)
boton_descargar_clave_pintor.pack(side=tk.RIGHT, padx=10, pady=10)

# Marco para calcular secreto aes
marco_calcular_secreto = tk.LabelFrame(root, text="Calcular secreto AES", padx=5, pady=5)
marco_calcular_secreto.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

btn_seleccionar_llave_publica = tk.Button(marco_calcular_secreto, text="Seleccionar Clave Pública del Pintor", command=seleccionar_llave_publica)
btn_seleccionar_llave_publica.pack(pady=1)
etiqueta_llave_publica = tk.Label(marco_calcular_secreto, text="")
etiqueta_llave_publica.pack(pady=1)

btn_seleccionar_llave_privada = tk.Button(marco_calcular_secreto, text="Seleccionar su Clave Privada", command=seleccionar_llave_privada)
btn_seleccionar_llave_privada.pack(pady=1)
etiqueta_llave_privada = tk.Label(marco_calcular_secreto, text="")
etiqueta_llave_privada.pack(pady=1)

boton_calcular_aes = tk.Button(marco_calcular_secreto, text="Calcular Secreto AES", command=calcular_secreto)
boton_calcular_aes.pack(pady=10)

# Marco para cifrar por GCM
marco_cifrar = tk.LabelFrame(root, text="Cifrar Foto", padx=5, pady=5)
marco_cifrar.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

btn_seleccionar_secreto_aes_cif = tk.Button(marco_cifrar, text="Seleccionar Secreto AES", command=seleccionar_sereto_aes_cif)
btn_seleccionar_secreto_aes_cif.pack(pady=1)
etiqueta_secreto_aes_cif = tk.Label(marco_cifrar, text="")
etiqueta_secreto_aes_cif.pack(pady=1)

btn_seleccionar_documento_cif = tk.Button(marco_cifrar, text="Seleccionar Foto", command=seleccionar_documento_cif)
btn_seleccionar_documento_cif.pack(pady=1)
etiqueta_documento_cif = tk.Label(marco_cifrar, text="")
etiqueta_documento_cif.pack(pady=1)

boton_cifrar = tk.Button(marco_cifrar, text="Cifrar Foto y subir Foto Cifrada", command=cifra)
boton_cifrar.pack(pady=10)

# Marco para firmar con ECDSA
marco_firmar = tk.LabelFrame(root, text="Firmar Solicitud", padx=5, pady=5)
marco_firmar.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

btn_seleccionar_llave_privada_firma = tk.Button(marco_firmar, text="Seleccionar su Clave Privada", command=seleccionar_llave_privada_firma)
btn_seleccionar_llave_privada_firma.pack(pady=1)
etiqueta_llave_privada_firma = tk.Label(marco_firmar, text="")
etiqueta_llave_privada_firma.pack(pady=1)

btn_seleccionar_documento_firma = tk.Button(marco_firmar, text="Seleccionar Documento de Solicitud", command=seleccionar_documento_firma)
btn_seleccionar_documento_firma.pack(pady=1)
etiqueta_documento_firma = tk.Label(marco_firmar, text="")
etiqueta_documento_firma.pack(pady=1)

boton_firmar = tk.Button(marco_firmar, text="Firmar Documento y Subir Documento y Firma", command=firma)
boton_firmar.pack(pady=10)

# Marco para descifrar por GCM
marco_descifrar = tk.LabelFrame(root, text="Descifrar Pedido Terminado", padx=5, pady=5)
marco_descifrar.pack(padx=10, pady=10, fill="both", expand="yes")

boton_descargar_pedido = tk.Button(marco_descifrar, text="Descargar Pedido Terminado", command=descargar_pedido_terminado)
boton_descargar_pedido.pack(pady=10)

btn_seleccionar_secreto_aes_des = tk.Button(marco_descifrar, text="Seleccionar Secreto AES", command=seleccionar_sereto_aes_des)
btn_seleccionar_secreto_aes_des.pack(pady=1)
etiqueta_secreto_aes_des = tk.Label(marco_descifrar, text="")
etiqueta_secreto_aes_des.pack(pady=1)

btn_seleccionar_documento_des = tk.Button(marco_descifrar, text="Seleccionar Documento", command=seleccionar_documento_des)
btn_seleccionar_documento_des.pack(pady=1)
etiqueta_documento_des = tk.Label(marco_descifrar, text="")
etiqueta_documento_des.pack(pady=1)

boton_descifrar = tk.Button(marco_descifrar, text="Descifrar Archivo", command=descifra)
boton_descifrar.pack(pady=10)

root.mainloop()