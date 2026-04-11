import socket
import threading

HOST = '127.0.0.1'
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

print("Оба клиента подключены! Начинаем обмен ключами...\n")

# Пересылаем открытые ключи между клиентами
# Клиент 1 отправляет свой публичный ключ клиенту 2
pubkey1 = clients[0].recv(4096).decode()
clients[1].send(pubkey1.encode())

# Клиент 2 отправляет свой публичный ключ клиенту 1
pubkey2 = clients[1].recv(4096).decode()
clients[0].send(pubkey2.encode())

print("Ключи обменяны! Начинается зашифрованный чат...\n")

def handle_client(client, other_client, nickname):
    """Пересылает зашифрованные сообщения"""
    while True:
        try:
            msg = client.recv(4096).decode()
            if msg:
                print(f"{nickname} (зашифровано): {msg[:50]}...")
                other_client.send(msg.encode())
            else:
                break
        except:
            break
    
    print(f"{nickname} отключился")
    other_client.send("Система: Собеседник покинул чат".encode())
    client.close()
    other_client.close()

# Запускаем потоки
thread1 = threading.Thread(target=handle_client, 
                          args=(clients[0], clients[1], nicknames[0]))
thread2 = threading.Thread(target=handle_client, 
                          args=(clients[1], clients[0], nicknames[1]))

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()

thread1.join()
thread2.join()

server.close()
