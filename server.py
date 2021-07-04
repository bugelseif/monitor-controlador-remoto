import json
import socket
import sys


# Configuração

IP = '0.0.0.0'
PORT = 50000


# Valores

controle = {
    'luz_guarita': False,
    'ar_guarita': False,
    'luz_estacionamento': False,
    'luz_galpao_externo': False,
    'luz_galpao_interno': False,
    'luz_escritorio': False,
    'ar_escritorio': False,
    'luz_sala_reunioes': False,
    'ar_sala_reunioes': False,
}


def main():
    print('Iniciando servidor...', end='\n\n\n')
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((IP, PORT))
    while True:
        msg, client = serverSock.recvfrom(1024)
        msg = msg.decode()
        if msg == 'sair':
            print('Fechando...')
            sys.exit()

        msg = json.loads(msg)
        print(f'Recebido: {msg}')

        locate = msg['locate']
        if msg['command'] == 'SET':
            controle[locate] = msg['value']
        enviar = {
            'locate': locate,
            'status': 'on' if controle[locate] else 'off',
        }

        print(f'Enviado: {enviar}', end='\n\n\n')
        serverSock.sendto(bytes(json.dumps(enviar), 'utf-8'), client)


if __name__ == '__main__':
    main()
