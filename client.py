import socket
from cryptography.fernet import Fernet

HOST = '192.168.0.2'  # endereço IP do servidor
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
    # Recebe e descriptogra