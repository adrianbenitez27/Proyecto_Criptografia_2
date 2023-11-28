import base64
import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes, ciphers
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

def generar_par_claves_ecdh():
    """Genera un par de claves ECDH usando la curva P-256."""
    clave_privada = ec.generate_private_key(ec.SECP256R1())
    clave_publica = clave_privada.public_key()
    return clave_privada, clave_publica

def serializar_claves(clave_publica, clave_privada, nom_clav):
    """Serializa la clave pública y privada al formato PEM."""
    with open(f"clave_privada_P-256_{nom_clav}.pem", "wb") as f:
            f.write(clave_privada.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
        
    with open(f"clave_publica_P-256_{nom_clav}.pem", "wb") as f:
        f.write(clave_publica.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo))

def deserializar_clave(datos_pem, sel):
    """Deserializa la clave pública o privada en formato PEM."""
    if(sel):
        with open(datos_pem, "rb") as archivo:
            clave = serialization.load_pem_private_key(archivo.read(),password=None)
    else:
        with open(datos_pem, "rb") as archivo:
            clave = serialization.load_pem_public_key(archivo.read())

    return clave

def calcular_secreto_compartido(clave_privada, clave_publica_otra_entidad):
    """Calcula el secreto compartido usando la clave privada propia y la clave pública de la otra entidad."""
    secreto_compartido = clave_privada.exchange(ec.ECDH(), clave_publica_otra_entidad)
    return secreto_compartido

def derivar_clave_aes(secreto_compartido, longitud_clave=32):
    """Deriva una clave AES a partir de un secreto compartido usando HKDF."""
    derivador = HKDF(
        algorithm=hashes.SHA256(),
        length=longitud_clave,
        salt=None,
        info=b"clave derivada para AES",
    )
    clave_aes = derivador.derive(secreto_compartido)

    clave_aes = base64.b64encode(clave_aes)
    
    with open(f"secreto_aes_ABA.pem", "wb") as f:
            f.write(clave_aes)

def cifrar_archivo_gcm(ruta_archivo, clave_aes):
    """Cifra un archivo usando AES-GCM."""
    # Generar un nonce (número usado una sola vez) para AES-GCM
    nonce = os.urandom(12)

    with open(clave_aes, "rb") as archivo:
        clave_aes = base64.b64decode(archivo.read())

    cifrador = ciphers.Cipher(ciphers.algorithms.AES(clave_aes), ciphers.modes.GCM(nonce), backend=default_backend()).encryptor()

    with open(ruta_archivo, 'rb') as f:
        contenido = f.read()

    contenido_cifrado = cifrador.update(contenido) + cifrador.finalize()

    # Guardar el nonce, el tag de autenticación y el contenido cifrado
    with open(ruta_archivo + ".cifrado_gcm", 'wb') as f:
        f.write(base64.b64encode(nonce + contenido_cifrado + cifrador.tag))

def descifrar_archivo_gcm(ruta_archivo_cifrado, clave_aes):
    """Descifra un archivo cifrado usando AES-GCM."""
    with open(clave_aes, "rb") as archivo:
        clave_aes = base64.b64decode(archivo.read())

    with open(ruta_archivo_cifrado, 'rb') as f:
        # Leer el nonce, el tag de autenticación y el contenido cifrado
        archivo = base64.b64decode(f.read())

        nonce = archivo[:12]
        contenido_cifrado = archivo[12:-16]
        tag = archivo[-16:]

    descifrador = ciphers.Cipher(ciphers.algorithms.AES(clave_aes), ciphers.modes.GCM(nonce, tag), backend=default_backend()).decryptor()
    contenido = descifrador.update(contenido_cifrado) + descifrador.finalize()

    # Determinar el nombre del archivo descifrado
    nombre_base = os.path.basename(ruta_archivo_cifrado).replace(".cifrado_gcm", "")
    ruta_descifrado = os.path.join(os.path.dirname(ruta_archivo_cifrado), nombre_base.rsplit('.', 1)[0] + "_descifrado_gcm." + nombre_base.rsplit('.', 1)[1])

    # Guardar el contenido descifrado
    with open(ruta_descifrado, 'wb') as f:
        f.write(contenido)

def firmar_documento(ruta_documento, clave_privada):
    with open(clave_privada, "rb") as archivo:
        llave_privada = serialization.load_pem_private_key(archivo.read(),password=None)
    
    with open(ruta_documento, "rb") as archivo:
        documento = archivo.read()
    
    firma = llave_privada.sign(documento, ec.ECDSA(hashes.SHA256()))
    
    nombre_documento = os.path.basename(ruta_documento).split('.')[0]
    with open(f"firma_{nombre_documento}.txt", "w") as archivo:
        archivo.write(base64.b64encode(firma).decode('utf-8'))

    #reiniciar_rutas()
    #messagebox.showinfo("Éxito", "Documento firmado")

def verificar_firma(ruta_documento_firmado, ruta_documento, clave_publica):
    with open(clave_publica, "rb") as archivo:
        llave_publica = serialization.load_pem_public_key(archivo.read())
    
    with open(ruta_documento, "rb") as archivo:
        documento = archivo.read()
    
    with open(ruta_documento_firmado, "r") as archivo:
        firma = base64.b64decode(archivo.read().encode('utf-8'))
    
    try:
        llave_publica.verify(firma, documento, ec.ECDSA(hashes.SHA256()))
        print("Éxito")
        #messagebox.showinfo("Resultado", "La firma es válida.")
    except:
        print("Error")
        #messagebox.showerror("Error", "La firma es inválida.")
    
    #reiniciar_rutas()

#firmar_documento("documentos/prueba_1_(medicamentos).txt", "clave_privada_P-256_Adrian Benitez.pem")
#verificar_firma("firma_prueba_1_(medicamentos).txt", "documentos/prueba_1_(medicamentos).txt", "clave_pública_P-256_Adrian Benitez.pem")