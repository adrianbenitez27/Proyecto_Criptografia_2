import socket
import ssl

server_address = ('localhost', 8443)

# Configuración del cliente
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection(server_address) as client_socket:
    with context.wrap_socket(client_socket, server_hostname='localhost') as secure_socket:
        print("Conexión segura establecida.")

        datos_recibidos = secure_socket.recv(1024)
        print(f"Datos recibidos: {datos_recibidos.decode()}")

        mensaje = "¡Hola desde el cliente!"
        secure_socket.sendall(mensaje.encode())
