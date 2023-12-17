import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import GCM_ECDH as procesos
import requests
import os
import shutil

nombre_cliente = ""
apellido_cliente = ""
numero_cliente = ""

ruta_llave_privada = ""
ruta_llave_publica = ""
ruta_secreto_aes_cif = ""
ruta_secreto_aes_des = ""
ruta_documento_cif = ""
ruta_documento_des = ""
ruta_llave_publica_verifica = ""
ruta_documento_firmado = ""
ruta_documento_original = ""

# Función para solicitar nombre, apellido y número de cliente al inicio
def solicitar_datos_usuario():
    global nombre_cliente, apellido_cliente, numero_cliente
    nombre_cliente = simpledialog.askstring("Nombre", "Ingresa el nombre del cliente (minusculas):")
    apellido_cliente = simpledialog.askstring("Apellido", "Ingresa el apellido del cliente (minusculas):")
    numero_cliente = simpledialog.askstring("Número de Cliente", "Ingresa el numero del cliente:")

    # Actualiza la interfaz con la información del usuario
    info_usuario.config(text=f"Nombre Completo: {nombre_cliente} {apellido_cliente}\nNúmero de Cliente: {numero_cliente}")

def reiniciar_rutas():
    global ruta_llave_privada, ruta_llave_publica, ruta_secreto_aes_cif, ruta_secreto_aes_des
    global ruta_documento_cif, ruta_documento_des, ruta_llave_publica_verifica, ruta_documento_firmado, ruta_documento_original 
    ruta_llave_privada = ""
    ruta_llave_publica = ""
    ruta_secreto_aes_cif = ""
    ruta_secreto_aes_des = ""
    ruta_documento_cif = ""
    ruta_documento_des = ""
    ruta_llave_publica_verifica = ""
    ruta_documento_firmado = ""
    ruta_documento_original = ""
    etiqueta_llave_privada.config(text="")
    etiqueta_llave_publica.config(text="")
    etiqueta_secreto_aes_cif.config(text="")
    etiqueta_secreto_aes_des.config(text="")
    etiqueta_documento_cif.config(text="")
    etiqueta_documento_des.config(text="")
    etiqueta_llave_publica_verifica.config(text="")
    etiqueta_documento_firmado.config(text="")
    etiqueta_documento_original.config(text="")

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

def seleccionar_llave_publica_verifica():
    global ruta_llave_publica_verifica
    ruta_llave_publica_verifica = filedialog.askopenfilename(title="Seleccione una clave pública")
    etiqueta_llave_publica_verifica.config(text=ruta_llave_publica_verifica)

def descargar_solicitud_y_firma():
    global nombre_cliente, apellido_cliente, numero_cliente

    if nombre_cliente and apellido_cliente and numero_cliente:
        # Descargar la solicitud
        nombre_archivo_solicitud = f"{nombre_cliente}_{apellido_cliente}_{numero_cliente}.txt"
        response_solicitud = requests.get(f'http://localhost:5000/download/solicitudes/{nombre_archivo_solicitud}')
        if response_solicitud.ok:
            with open(nombre_archivo_solicitud, "wb") as file:
                file.write(response_solicitud.content)

        # Descargar la firma
        nombre_archivo_firma = f"firma_{nombre_cliente}_{apellido_cliente}_{numero_cliente}.txt"
        response_firma = requests.get(f'http://localhost:5000/download/firmas/{nombre_archivo_firma}')
        if response_firma.ok:
            with open(nombre_archivo_firma, "wb") as file:
                file.write(response_firma.content)

        messagebox.showinfo("Descarga Completa", "Solicitud y firma del cliente descargadas correctamente.")
    else:
        messagebox.showerror("Error de Descarga", "Debe ingresar nombre y apellido del cliente.")

def seleccionar_documento_firmado():
    global ruta_documento_firmado
    ruta_documento_firmado = filedialog.askopenfilename(title="Seleccione un archivo a verificar")
    etiqueta_documento_firmado.config(text=ruta_documento_firmado)

def seleccionar_documento_original():
    global ruta_documento_original
    ruta_documento_original = filedialog.askopenfilename(title="Seleccione el archivo original")
    etiqueta_documento_original.config(text=ruta_documento_original)

def calcular_secreto():
    clave_publica_recibida_B = procesos.deserializar_clave(ruta_llave_publica, 0)
    clave_privada_A = procesos.deserializar_clave(ruta_llave_privada, 1)

    secreto_compartido_A = procesos.calcular_secreto_compartido(clave_privada_A, clave_publica_recibida_B)
    procesos.derivar_clave_aes(secreto_compartido_A)

    messagebox.showinfo("Éxito", "Secreto AES calculado")

def descargar_clave_publica_cliente():
    global nombre_cliente, apellido_cliente, numero_cliente

    if nombre_cliente and apellido_cliente and numero_cliente:
        nombre_archivo = f"clave_publica_P-256_{nombre_cliente}_{apellido_cliente}_{numero_cliente}.pem"
        response = requests.get(f'http://localhost:5000/download/key/{nombre_archivo}')
        if response.ok:
            with open(nombre_archivo, "wb") as file:
                file.write(response.content)
            messagebox.showinfo("Descarga Completa", "La clave pública del cliente se ha descargado correctamente.")
        else:
            messagebox.showerror("Error de Descarga", "No se pudo descargar la clave pública del cliente.")

def cifra():
    global nombre_cliente, apellido_cliente, numero_cliente
    # Asegúrate de que se han ingresado el nombre, apellido y número de cliente
    if not (nombre_cliente and apellido_cliente and numero_cliente):
        messagebox.showerror("Error", "Debe ingresar el nombre, apellido y número de cliente antes de cifrar.")
        return

    # Cifra el archivo
    ruta_archivo_cifrado = procesos.cifrar_archivo_gcm(ruta_documento_cif, ruta_secreto_aes_cif)

    # Cambia el nombre del archivo cifrado para incluir nombre, apellido, número de cliente y "_terminado"
    nombre_archivo_cifrado = f"{nombre_cliente}_{apellido_cliente}_{numero_cliente}_terminado.jpg.cifrado_gcm"
    os.rename(ruta_archivo_cifrado, nombre_archivo_cifrado)

    # Sube el archivo cifrado
    with open(nombre_archivo_cifrado, "rb") as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/upload/pedidos_terminados', files=files)
        if response.ok:
            messagebox.showinfo("Éxito", "Archivo cifrado y subido con éxito")
        else:
            messagebox.showerror("Error", "No se pudo subir el archivo cifrado")
    reiniciar_rutas()


def descifra():
    procesos.descifrar_archivo_gcm(ruta_documento_des, ruta_secreto_aes_des)
    reiniciar_rutas()

    messagebox.showinfo("Éxito", "Descifrado correcto")

def descargar_pedido_cifrado():
    global nombre_cliente, apellido_cliente, numero_cliente

    if nombre_cliente and apellido_cliente and numero_cliente:
        nombre_archivo = f"{nombre_cliente}_{apellido_cliente}_{numero_cliente}.jpg.cifrado_gcm"
        response = requests.get(f'http://localhost:5000/download/pedidos/{nombre_archivo}')
        if response.ok:
            with open(nombre_archivo, "wb") as file:
                file.write(response.content)
            messagebox.showinfo("Descarga Completa", "El pedido cifrado se ha descargado correctamente.")
        else:
            messagebox.showerror("Error de Descarga", "No se pudo descargar el pedido cifrado.")


def verifica():
    resultado = procesos.verificar_firma(ruta_documento_firmado, ruta_documento_original, ruta_llave_publica_verifica)
    reiniciar_rutas()

    if resultado:
        messagebox.showinfo("Éxito", "La firma es correcta y ha sido verificada con éxito.")
    else:
        messagebox.showerror("Error", "La firma no es correcta o no pudo ser verificada.")


root = tk.Tk()
root.title("Interfaz del pintor para retrato digital")

# Recuadro para mostrar la información del usuario
marco_usuario = tk.LabelFrame(root, text="Información del Cliente", padx=5, pady=5)
marco_usuario.pack(padx=10, pady=10, fill="both", expand="yes", side="top")
info_usuario = tk.Label(marco_usuario, text="", justify=tk.LEFT)
info_usuario.pack()

# Solicitar datos al usuario al inicio
solicitar_datos_usuario()

# Marco para calcular secreto aes
marco_calcular_secreto = tk.LabelFrame(root, text="Calcular secreto AES", padx=5, pady=5)
marco_calcular_secreto.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

boton_descargar_clave_cliente = tk.Button(marco_calcular_secreto, text="Descargar Clave Pública del Cliente", command=descargar_clave_publica_cliente)
boton_descargar_clave_cliente.pack(pady=10)

btn_seleccionar_llave_publica = tk.Button(marco_calcular_secreto, text="Seleccionar Clave Pública del Cliente", command=seleccionar_llave_publica)
btn_seleccionar_llave_publica.pack(pady=1)
etiqueta_llave_publica = tk.Label(marco_calcular_secreto, text="")
etiqueta_llave_publica.pack(pady=1)

btn_seleccionar_llave_privada = tk.Button(marco_calcular_secreto, text="Seleccionar su Clave Privada", command=seleccionar_llave_privada)
btn_seleccionar_llave_privada.pack(pady=1)
etiqueta_llave_privada = tk.Label(marco_calcular_secreto, text="")
etiqueta_llave_privada.pack(pady=1)

boton_calcular_aes = tk.Button(marco_calcular_secreto, text="Calcular Secreto AES", command=calcular_secreto)
boton_calcular_aes.pack(pady=10)

# Marco para verificar con ECDSA
marco_verificar = tk.LabelFrame(root, text="Verificar Firma de Solicitud", padx=5, pady=5)
marco_verificar.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

boton_descargar_solicitud_firma = tk.Button(marco_verificar, text="Descargar Solicitud y Firma de Solicitud", command=descargar_solicitud_y_firma)
boton_descargar_solicitud_firma.pack(pady=10)

btn_seleccionar_llave_publica_verifica = tk.Button(marco_verificar, text="Seleccionar Clave Pública del Cliente", command=seleccionar_llave_publica_verifica)
btn_seleccionar_llave_publica_verifica.pack(pady=1)
etiqueta_llave_publica_verifica = tk.Label(marco_verificar, text="")
etiqueta_llave_publica_verifica.pack(pady=1)

btn_seleccionar_documento_firmado = tk.Button(marco_verificar, text="Seleccionar Documento de Solicitud Firmado", command=seleccionar_documento_firmado)
btn_seleccionar_documento_firmado.pack(pady=1)
etiqueta_documento_firmado = tk.Label(marco_verificar, text="")
etiqueta_documento_firmado.pack(pady=1)

btn_seleccionar_documento_original = tk.Button(marco_verificar, text="Seleccionar Documento de Solicitud Original", command=seleccionar_documento_original)
btn_seleccionar_documento_original.pack(pady=1)
etiqueta_documento_original = tk.Label(marco_verificar, text="")
etiqueta_documento_original.pack(pady=1)

boton_firmar = tk.Button(marco_verificar, text="Verificar Firma de Documento", command=verifica)
boton_firmar.pack(pady=10)

# Marco para descifrar por GCM
marco_descifrar = tk.LabelFrame(root, text="Descifrar Pedido", padx=5, pady=5)
marco_descifrar.pack(padx=10, pady=10, fill="both", expand="yes", side="left")

boton_descargar_pedido_cifrado = tk.Button(marco_descifrar, text="Descargar Pedido Cifrado", command=descargar_pedido_cifrado)
boton_descargar_pedido_cifrado.pack(pady=10)

btn_seleccionar_secreto_aes_des = tk.Button(marco_descifrar, text="Seleccionar Secreto AES", command=seleccionar_sereto_aes_des)
btn_seleccionar_secreto_aes_des.pack(pady=1)
etiqueta_secreto_aes_des = tk.Label(marco_descifrar, text="")
etiqueta_secreto_aes_des.pack(pady=1)

btn_seleccionar_documento_des = tk.Button(marco_descifrar, text="Seleccionar Foto Cifrada", command=seleccionar_documento_des)
btn_seleccionar_documento_des.pack(pady=1)
etiqueta_documento_des = tk.Label(marco_descifrar, text="")
etiqueta_documento_des.pack(pady=1)

boton_descifrar = tk.Button(marco_descifrar, text="Descifrar Pedido", command=descifra)
boton_descifrar.pack(pady=10)

# Marco para cifrar por GCM
marco_cifrar = tk.LabelFrame(root, text="Cifrar Pedido Terminado", padx=5, pady=5)
marco_cifrar.pack(padx=10, pady=10, fill="both", expand="yes")

btn_seleccionar_secreto_aes_cif = tk.Button(marco_cifrar, text="Seleccionar Secreto AES", command=seleccionar_sereto_aes_cif)
btn_seleccionar_secreto_aes_cif.pack(pady=1)
etiqueta_secreto_aes_cif = tk.Label(marco_cifrar, text="")
etiqueta_secreto_aes_cif.pack(pady=1)

btn_seleccionar_documento_cif = tk.Button(marco_cifrar, text="Seleccionar Foto", command=seleccionar_documento_cif)
btn_seleccionar_documento_cif.pack(pady=1)
etiqueta_documento_cif = tk.Label(marco_cifrar, text="")
etiqueta_documento_cif.pack(pady=1)

boton_cifrar = tk.Button(marco_cifrar, text="Cifrar y Enviar Foto", command=cifra)
boton_cifrar.pack(pady=10)

root.mainloop()