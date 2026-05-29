import socket

HOST = "0.0.0.0"
PORT = 7792

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

print(f"Servidor EVO ouvindo na porta {PORT}...")

while True:

    conn, addr = server.accept()

    print(f"\nConectado: {addr}")

    try:

        while True:

            data = conn.recv(4096)

            if not data:
                break

            print("\n===== DADOS RECEBIDOS =====")

            try:
                print(data.decode("utf-8"))
            except:
                print(data)

            print("===========================\n")

            # resposta ACK
            conn.send(b"OK")

    except Exception as e:

        print("Erro:", e)

    finally:

        conn.close()

        print("Conexao encerrada.")