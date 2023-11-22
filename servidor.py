import socket
import ssl

server_address = ('localhost', 8443)

# Configuración del servidor
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # Cambia a tus rutas y nombres de archivos

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as server_socket:
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Esperando conexiones...")

    with context.wrap_socket(server_socket, server_side=True) as secure_socket:
        conn, addr = secure_socket.accept()
        with conn:
            print(f"Conexión segura establecida desde: {addr}")

            mensaje = "¡Hola desde el servidor!"
            conn.sendall(mensaje.encode())
            datos_recibidos = conn.recv(1024)
            print(f"Datos recibidos: {datos_recibidos.decode()}")
