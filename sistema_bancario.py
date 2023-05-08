from datetime import datetime
from textwrap import dedent


def menu(lvl):
    menu_login = """\n
========== MENU ==========

[a] \tAcessar(Login)
[nu]\tCriar_Novo_Usuário
[lu]\tListar_Usuários
[lc]\tListar_Contas
[q] \tSair

=> """
    menu_inicial = """\n
========== MENU ==========

[sc]\tSelecionar_Conta
[lc]\tListar_Contas
[cc]\tCriar_Nova_Conta_Corrente
[r] \tRetornar_ao_Menu_Anterior(Logout)
[q] \tSair

=> """
    menu_principal = """\n
========== MENU ==========

[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[r]\tRetornar_ao_menu_anterior
[q]\tSair

=> """
    match lvl:
        case 0:
            return menu_login
        case 1:
            return menu_inicial
        case 2:
            return menu_principal


def getValor(mensagem):
    try:
        valor = float(dedent(input(mensagem).replace(',', '.').replace(' ', '')))
    except ValueError:
        valor = 0
        print('Operação falhou! O valor informado é inválido.')
    return valor


#args only
def depositar(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R$ {valor:.2f} data: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n'
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
    return saldo, extrato
            

#kwargs only
def sacar(*, valor, saldo, limite_valor, numero, limite_saques, extrato):
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
    return saldo, extrato, numero


#args e kwargs
def exibirExtrato(saldo, /, *, extrato):
    print("\n================== EXTRATO ==================")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print(extrato if extrato else 'Não foram realizadas movimentações nessa conta.')
    print("\n=============================================")


def criarUsuario(usuarios):
    cpf = input('Digite seu CPF (somente números): ').replace('.', '').replace('-', '').replace(' ', '').strip()
    # Verificar se o CPF já existe
    usuario = getUserByCPF(cpf, usuarios)
    
    if usuario:
        print('\n!!! Usuário existente no banco de dados !!!')
        return
    
    nome = input('Digite seu Nome: ').strip()
    data_nacimento = input('Digite sua data de nascimento (dd-mm-aaaa): ').strip()
    print('\n Digite seu endereço comlpeto: ')
    logradouro = input('Logradouro: ').strip()
    numero = input('Número: ').strip()
    bairro = input('Bairro: ').strip()
    cidade = input('Cidade: ').strip()
    estado = input('Sigla do Estado (AA): ').strip()
    
    usuarios.append({
    'cpf': cpf, # pk
    'nome':nome,
    'data_nascimento': data_nacimento,
    'endereco': f'{logradouro}/{numero}/{bairro}/{cidade}/{estado}'
    })
    
    print('=== Usuário criado com sucesso" ===')
        
        
def criarContaCorrente(agencia, contas, usuario):
    proximo_numero = max([i['numero'] for i in contas]) + 1 if contas else 1
    
    contas.append({
    'agencia': agencia,
    'numero': proximo_numero,
    'cliente': usuario['cpf'], # fk cpf cliente
    'saldo': 0,
    'extrato': '',
    'qtd_saques': 0,
    'limite_saque': 500,
    'saques_diarios': 3,
    })
    
    print(f"Conta número: {proximo_numero} criada com sucesso!")


def getUserByCPF(cpf, usuarios): # fazer login também
    validUser = [i for i in usuarios if i['cpf'] == cpf]
    if validUser:
        return validUser[0]
    else:
        return validUser


def listarUsuarios(usuarios):
    print('\n========== USUARIOS ==========')
    for u in usuarios:
        print(f'CPF: {u["cpf"]}\t | NOME: {u["nome"]}')
    print('\n==============================')


def listarContas(contas, usuario={}):
    if not usuario:
        print('\n========== CONTAS ==========')
        for c in contas:
            print(f'CLIENTE: {c["cliente"]}\t | CONTA: {c["numero"]}')
        print('\n==============================')
    else:
        print('\n========== CONTAS ==========')
        for c in [i for i in contas if i['cliente'] == usuario['cpf']]:
            print(f'CLIENTE: {c["cliente"]}\t | CONTA: {c["numero"]}')
        print('\n==============================')


def selecionarConta(numero, contas, usuario):
    validAccount = [i for i in contas if i['numero'] == numero and i['cliente'] == usuario['cpf']]
    if validAccount:
        print(f'==== Conta selecionada: {numero} ====')
        return validAccount[0]
    else:
        print(f'Não foi possível encontrar a conta {numero}.')
        return validAccount


def fazerLogin(cpf, usuarios):
    usuario = getUserByCPF(cpf, usuarios)
    if usuario:
        print(f'Login feito com sucesso para: {usuario["nome"]}')
        return usuario
    else:
        print('Não foi possivel encontrar o cpf informado')    
        return {}
    

def fazerLogout(usuario):
    print('Logout feito com sucesso!')
    return {}


def main():
    lista_clientes = []
    lista_contas = []
    
    # Usuário logado
    current_user = {}
    current_account = 0
    
    # Nível menu
    menu_lvl = 0
    
    # inicio da aplicação
    while True:
        opcao = input(menu(menu_lvl))
        
        match opcao:
            case 'd': # depositar
                valor = getValor('Favor informar o valor a ser depositado: ')
                current_account['saldo'], current_account['extrato'] = depositar(valor, current_account['saldo'], current_account['extrato'])
            
            case 's': # sacar
                valor = getValor('Favor informar o valor a ser sacado: ')
                current_account['saldo'], current_account['extrato'], current_account['qtd_saques'] =  sacar(valor=valor, saldo=current_account['saldo'], limite_valor=current_account['limite_saque'], numero=current_account['qtd_saques'], limite_saques=current_account['saques_diarios'], extrato=current_account['extrato'])
            
            case 'e': # extrato
                exibirExtrato(current_account['saldo'], extrato=current_account['extrato'])
            
            case 'sc': # selecionar conta
                try:
                    numero = int(input('Digite o número da conta: ').strip())
                except ValueError:
                    numero = 0
                    print('Digite um numero válido.')
                    continue
                current_account = selecionarConta(numero, lista_contas, current_user)
                if current_account:
                    menu_lvl += 1
           
            case 'lc': # listar contas
                listarContas(lista_contas, current_user)
            
            case 'cc':
                criarContaCorrente('0001', lista_contas, current_user)
            
            case 'a': # acessar
                cpf = input('Digite seu CPF (somente números): ').replace('.', '').replace('-', '').replace(' ', '').strip()
                current_user = fazerLogin(cpf, lista_clientes)
                if current_user:
                    menu_lvl += 1
            
            case 'nu':  # criar novo usuario
                criarUsuario(lista_clientes)
           
            case 'lu': # listar usuários
                listarUsuarios(lista_clientes)
            
            case 'r': # retornar
                menu_lvl -= 1
                if menu_lvl < 1:
                    current_user = fazerLogout(current_user)
            
            case 'q': # sair
                print('Obrigado por utilizar os nossos serviços.')
                break
            
            case _:
                print('Favor selecionar uma opção válida.')
        
        


main()

