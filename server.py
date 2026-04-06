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

# Принимаем двух клиентов
client1, addr1 = server.accept()
print(f"Клиент 1 подключен: {addr1}")
client1.send("Вы подключены как Клиент 1".encode())
clients.append(client1)

client2, addr2 = server.accept()
print(f"Клиент 2 подключен: {addr2}")
client2.send("Вы подключены как Клиент 2".encode())
clients.append(client2)

print("Оба клиента подключены! Начинаем чат...\n")

def handle_client(client, other_client, client_num):
    """Обрабатывает сообщения от одного клиента и пересылает другому"""
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                print(f"Клиент {client_num}: {msg}")
                other_client.send(f"Клиент {client_num}: {msg}".encode())
            else:
                break
        except:
            break
    
    print(f"Клиент {client_num} отключился")
    other_client.send(f"Клиент {client_num} покинул чат".encode())
    client.close()
    other_client.close()

# Запускаем отдельный поток для каждого клиента
thread1 = threading.Thread(target=handle_client, args=(client1, client2, 1))
thread2 = threading.Thread(target=handle_client, args=(client2, client1, 2))

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()

# Ждем завершения потоков
thread1.join()
thread2.join()

server.close()
