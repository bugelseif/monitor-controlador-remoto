import json
import socket
import sys


# Configuração

IP = '127.0.0.1'
PORT = 50000


# Valores

locates = [
    'luz_guarita', 'ar_guarita', 'luz_estacionamento',
    'luz_galpao_externo', 'luz_galpao_interno', 'luz_escritorio',
    'ar_escritorio', 'luz_sala_reunioes', 'ar_sala_reunioes',
]

commands = ['GET', 'SET']

values = [False, True]


# Mensagens

selectLocate = '''Selecione o local pelo número:
    0- luz_guarita          1- ar_guarita           2- luz_estacionamento
    3- luz_galpao_externo   4- luz_galpao_interno   5- luz_escritorio
    6- ar_escritorio        7- luz_sala_reunioes    8- ar_sala_reunioes
    99- sair'''

selectCommand = '''Digite o comando pelo número:
    0- GET      1- SET'''

selectStatus = '''Digite o status pelo número:
    0- Desligar      1- Ligar'''


def main():
    print("start client")
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        print(selectLocate)
        local = int(input("digite o numero do local: "))
        while 8 < local or 0 > local:
            if local == 99:
                print("Fechando")
                clientSock.sendto(bytes('sair', 'utf-8'), (IP, PORT))
                sys.exit()
            print("Local incorreto, verifique")
            local = int(input("digite o numero do local: "))
        print(selectCommand)
        comando = int(input("digite o numero do comando: "))
        while 1 < comando or 0 > comando:
            print("Comando incorreto, verifique")
            comando = int(input("digite o numero do comando: "))

        if(comando == 1):
            print(selectStatus)
            valor = int(input("digite o numero do status: "))
            enviar = {
                'command': commands[comando],
                'locate': locates[local],
                'value': values[valor]
            }
        else:
            enviar = {
                'command': commands[comando],
                'locate': locates[local]
            }

        msg = json.dumps(enviar)
        print(f"enviado: {msg}")
        clientSock.sendto(bytes(msg, 'utf-8'), (IP, PORT))
        msgRecv = clientSock.recv(1024)
        msgRecv = json.loads(msgRecv)

        print(f"recebido: {msgRecv} \n\n")


if __name__ == "__main__":
    main()
