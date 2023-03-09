import socket
from cryptography.fernet import Fernet

HOST = ''  # endereço IP do servidor
PORT = 1234  # porta usada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer usado para receber dados

def generate_key():
    # Cria uma nova chave de criptografia e a salva em um arquivo
    key = Fernet.generate_key()
    with open("key.txt", "wb") as key_file:
        key_file.write(key)

def load_key():
    # Carrega a chave de criptografia do arquivo
    with open("key.txt", "rb") as key_file:
        key = key_file.read()
    return key

def enviar_mensagem(mensagem, conexao, fernet):
    # Criptografa e envia a mensagem
    mensagem_bytes = mensagem.encode()
    mensagem_criptografada = fernet.encrypt(mensagem_bytes)
    conexao.send(mensagem_criptografada)

def receber_mensagem(conexao, fernet):
    # Recebe e descriptografa a mensagem
    mensagem_criptografada = conexao.recv(BUFFER_SIZE)
    mensagem_bytes = fernet.decrypt(mensagem_criptografada)
    mensagem = mensagem_bytes.decode()
    return mensagem

if __name__ == '__main__':
    # Gera uma nova chave de criptografia (opcional)
    generate_key()

    # Carrega a chave de criptografia
    key = load_key()
    fernet = Fernet(key)

    # Cria um socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincula o socket a uma porta e endereço IP
    servidor.bind((HOST, PORT))

    # Aguarda uma conexão
    servidor.listen(1)
    print(f"Aguardando conexão em {HOST}:{PORT}...")

    # Aceita a conexão
    conexao, endereco = servidor.accept()
    ip_cliente = endereco[0]  # obtém o endereço IP do cliente
    print(f"Conexão estabelecida com {ip_cliente}")

    while True:
        # Recebe a mensagem do cliente
        mensagem_recebida = receber_mensagem(conexao, fernet)
        print(f"Mensagem recebida do {ip_cliente}: {mensagem_recebida}")

        # Solicita uma nova mensagem para enviar ao cliente
        mensagem_enviar = input("Digite a mensagem que deseja enviar: ")
        enviar_mensagem(mensagem_enviar, conexao, fernet)