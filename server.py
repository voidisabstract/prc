import socket
import threading

HOST = '213.148.16.116'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print(f"Сервер запущен на {HOST}:{PORT}")
print("Ожидание подключения двух клиентов...")

clients = []
nicknames = []

# Принимаем двух клиентов
for i in range(2):
    client, addr = server.accept()
    nickname = client.recv(1024).decode()
    clients.append(client)
    nicknames.append(nickname)
    print(f"Клиент {i+1} ({nickname}) подключен: {addr}")
    client.send(f"Вы подключены как {nickname}".encode())

print("Оба клиента подключены! Начинаем чат...\n")

def handle_client(client, other_client, nickname, other_nickname):
    """Обработка сообщений от одного клиента"""
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                print(f"{nickname}: {msg}")
                other_client.send(f"{nickname}: {msg}".encode())
            else:
                break
        except:
            break
    
    print(f"{nickname} отключился")
    other_client.send(f"Система: {nickname} покинул чат".encode())
    client.close()
    other_client.close()

# Запускаем потоки для каждого клиента
thread1 = threading.Thread(target=handle_client, 
                          args=(clients[0], clients[1], nicknames[0], nicknames[1]))
thread2 = threading.Thread(target=handle_client, 
                          args=(clients[1], clients[0], nicknames[1], nicknames[0]))

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()

thread1.join()
thread2.join()

server.close()
