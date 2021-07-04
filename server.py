import socket
import json
import sys

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
    print("start server")
    IP = "0.0.0.0"
    PORT = 50000
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((IP, PORT))
    while True:
        msg, client = serverSock.recvfrom(1024)
        if(msg.decode() == 'sair'):
            print("Fechando")
            sys.exit()

        msg = json.loads(msg)
        print(f'recebido: {msg}')
        locate = msg['locate']
        retorno = controle[locate]

        if(msg['command'] == 'SET'):
            retorno = msg['value']
            controle[locate] = retorno

        if retorno:
            status = 'on'
        else:
            status = 'off'

        enviar = {
            'locate': locate,
            'status': status,
        }
        msg = json.dumps(enviar)
        print(f"enviado: {msg} \n\n")
        serverSock.sendto(bytes(msg, 'utf-8'), client)


if __name__ == "__main__":
    main()
