from datetime import datetime


menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
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
        
        if valor > 0:
            saldo += valor
            extrato += f'Depósito: R$ {valor:.2f} data: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n'
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
            
    elif opcao == 's':
        pass
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