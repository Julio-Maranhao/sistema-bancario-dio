from datetime import datetime


def getValor(mensagem):
    try:
        valor = float(input(mensagem).replace(',', '.'))
    except ValueError:
        valor = 0
        print('Operação falhou! O valor informado é inválido.')
    
    return valor


def depositar(valor, saldo, extrato):
    if valor > 0:
            saldo += valor
            extrato += f'Depósito: R$ {valor:.2f} data: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n'
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
            
            
def sacar(valor, saldo, limite_valor, numero, limite_saques):
    if limite_saques <= numero:
            print('Você atingiu o número máximo de saques diários.')
    elif valor > saldo:
        print('Saldo insuficiente.')
    elif valor > limite_valor:
        print('O valor do saque informado excede o seu limite por saque, favor inserir um valor menor ou contactar o banco.')
    else:
        saldo -= valor
        numero += 1
        extrato += f'Saque: R$ {valor:.2f} data: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n'
        print(f'Saque de R$ {valor:.2f} realizado com sucesso!')


def exibirExtrato(saldo, extrato):
    print("\n================== EXTRATO ==================")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print(extrato if extrato else 'Não foram realizadas movimentações nessa conta.')
    print("\n=============================================")


menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite_por_saque = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)
    
    if opcao == 'd':
        try:
            valor = float(input('Favor informar o valor a ser depositado: ').replace(',', '.'))
        except ValueError:
            valor = 0
            print('Operação falhou! O valor informado é inválido.')
            continue
        
        if valor > 0:
            saldo += valor
            extrato += f'Depósito: R$ {valor:.2f} data: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n'
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
            
    elif opcao == 's':
        try:
            valor = float(input('Favor informar o valor a ser sacado: ').replace(',', '.'))
        except ValueError:
            valor = 0
            print('Operação falhou! O valor informado é inválido.')
            continue
        
        if LIMITE_SAQUES <= numero_saques:
            print('Você atingiu o número máximo de saques diários.')
            continue
        elif valor > saldo:
            print('Saldo insuficiente.')
            continue
        elif valor > limite_por_saque:
            print('O valor do saque informado excede o seu limite por saque, favor inserir um valor menor ou contactar o banco.')
            continue
        else:
            saldo -= valor
            numero_saques += 1
            extrato += f'Saque: R$ {valor:.2f} data: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n'
            print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
        
        
    elif opcao == 'e':
        print("\n================== EXTRATO ==================")
        print(f"\nSaldo: R$ {saldo:.2f}")
        print(extrato if extrato else 'Não foram realizadas movimentações nessa conta.')
        print("\n=============================================")
        
    elif opcao == 'q':
        print('Obrigado por utilizar os nossos serviços.')
        break
    else:
        print('Favor selecionar uma opção válida.')
