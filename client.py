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
    print('Iniciando cliente...')
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        while True:
            print(selectLocate)
            local = int(input('Digite o número do local: '))
            if 0 <= local <= 8:
                break
            if local == 99:
                print('Fechando...')
                clientSock.sendto(bytes('sair', 'utf-8'), (IP, PORT))
                sys.exit()
            print('Local incorreto, verifique')

        while True:
            print(selectCommand)
            comando = int(input('Digite o número do comando: '))
            if comando == 0 or comando == 1:
                break
            print('Comando incorreto, verifique')

        enviar = {
            'command': commands[comando],
            'locate': locates[local],
        }
        if comando == 1:
            while True:
                print(selectStatus)
                valor = int(input('Digite o número do status: '))
                if valor == 0 or valor == 1:
                    break
                print('Valor incorreto, verifique')

            enviar['value'] = values[valor]

        print(f'Enviado: {enviar}')
        clientSock.sendto(bytes(json.dumps(enviar), 'utf-8'), (IP, PORT))
        msgRecv = json.loads(clientSock.recv(1024))
        print(f'Recebido: {msgRecv}', end='\n\n\n')


if __name__ == '__main__':
    main()
