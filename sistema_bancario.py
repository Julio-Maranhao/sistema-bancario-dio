from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from textwrap import dedent


class Cliente:
    endereco:str
    contas:list
    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def relizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Conta:
    _saldo:float
    _numero:int
    _agencia:str
    _cliente:any
    _historico:any
    
    def __init__(self, numero, cliente):
      self._saldo = 0
      self._numero = numero
      self._agencia = "0001"
      self._cliente = cliente
      self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor) -> bool:
        if valor > self.saldo:
            print('Saldo insuficiente.')
        elif valor > 0:
            self._saldo -= valor
            print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
            return True
        else:
            print('Favor informar um valor válido.')
        return False
        
    def depositar(self, valor) -> bool:
        if valor > 0:
            self._saldo += valor
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
            return True
        else:
            print('Favor informar um valor válido.')
        return False
    

class Historico:
    _transacoes:list
    def __init__(self):
      self._transacoes = []
      
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Transacao(ABC):
    
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass


class PessoaFisica(Cliente):
    cpf:str
    nome:str
    data_nascimento:datetime
    
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

        
        
class ContaCorrente(Conta):
    limite:float
    limite_saques:int
    
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor) -> bool:
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao.tipo == Saque.__name__])
        
        if valor > self.limite:
            print('O valor do saque informado excede o seu limite por saque, favor inserir um valor menor ou contactar o banco.')
        elif numero_saques >= self.limite_saques:
            print('Você atingiu o número máximo de saques diários.')
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self) -> str:
        return f"""\n
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

    
class Deposito(Transacao):
    _valor:float
    _tipo:str
    _data:str
    
    def __init__(self, valor):
        super(Transacao, self).__init__()
        self._valor = valor
        self._tipo = self.__class__.__name__
        self._data = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
    @property
    def valor(self):
        return self._valor
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def data(self):
        return self._data
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
    def __str__(self):
        return f'{self.tipo}: R$ {self.valor:.2f} data: {self.data}'
        

class Saque(Transacao):
    _valor:float
    _tipo:str
    _data:str
    
    def __init__(self, valor):
        super(Transacao, self).__init__()
        self._valor = valor
        self._tipo = self.__class__.__name__
        self._data = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
    @property
    def valor(self):
        return self._valor
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def data(self):
        return self._data
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
    def __str__(self):
        return f'{self.tipo}: R$ {self.valor:.2f} data: {self.data}'
    
    
def menu(lvl:int):
    menu_login = """\n
========== MENU ==========

[a] \tAcessar(Login)
[nu]\tCriar_Novo_Usuário
[lu]\tListar_Usuários
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
    

def getValor(mensagem:str):
    try:
        valor = float(dedent(input(mensagem).replace(',', '.').replace(' ', '')))
    except ValueError:
        valor = 0
        print('Operação falhou! O valor informado é inválido.')
    return valor


def getPersonalData():
    nome = input('Informe seu nome: ')
    data_nascimento = input('Informe sua data de nascimento ex: 01-01-2001: ')
    cpf = input('Informe seu CPF(somente números): ')
    # endereço
    logradouro = input('Informe seu logradouro ex: Rua a...: ')
    numero = input('Informe o número da sua casa: ')
    bairro = input('Informe o bairro: ')
    cidade = input('Informe a cidade: ')
    estado = input('Informe a sigla do estado ex: SP: ')
    endereco = [i for i in [logradouro, numero, bairro, cidade, estado] if i]
    if endereco:
        endereco = '/ '.join(endereco)
    
    return nome, data_nascimento, cpf, endereco


def listarUsuarios(usuarios):
    print('\n========== USUARIOS ==========')
    for u in usuarios:
        print(f'CPF: {u.cpf}\t | NOME: {u.nome}')
    print('\n==============================')


def listarContas(usuario):
    print('\n========== CONTAS ==========')
    for c in usuario.contas:
        print(c)
    print('\n==============================')
        
        
def selecionarConta(numero:int, usuario):
    validAccount = [i for i in usuario.contas if i.numero == numero]
    if validAccount:
        print(f'==== Conta selecionada: {numero} ====')
        return validAccount[0]
    else:
        print(f'Não foi possível encontrar a conta {numero}.')
        return None


def getUserByCPF(cpf:str, usuarios:list):
    usuario = [u for u in usuarios if u.cpf == cpf]
    if usuario:
        return usuario[0]
    else:
        return None


def fazerLogin(cpf, usuarios):
    usuario = getUserByCPF(cpf, usuarios)
    if usuario:
        print(f'Login feito com sucesso para: {usuario.nome}')
        return usuario
    else:
        print('Não foi possivel encontrar o cpf informado')    
        return None
    

def fazerLogout(usuario):
    print('Logout feito com sucesso!')
    return None


def main():
    lista_clientes = []
    
    # Usuário logado
    current_user = ''
    current_account = ''
    
    # Nível menu
    menu_lvl = 0
    
    # Sequencial Contas DB
    ultima_conta = 1
    
    # inicio da aplicação
    while True:
        opcao = input(menu(menu_lvl))
        
        match opcao:
            case 'd': # depositar
                valor = getValor('Favor informar o valor a ser Depositado: ')
                transacao = Deposito(valor).registrar(current_account)
            
            case 's': # sacar
                valor = getValor('Favor informar o valor a ser Sacado: ')
                transacao = Saque(valor).registrar(current_account)
            
            case 'e': # extrato
                print('\n========== EXTRATO ==========')
                print(current_account)
                print(f"\tSALDO: R$ {current_account.saldo:.2f}")
                print('\n========= TRANSAÇÕES =========')
                for transacao in current_account.historico.transacoes:
                    print(transacao)
                print('================================')
            
            case 'sc': # selecionar conta
                try:
                    numero = int(input('Digite o número da conta: ').strip())
                except ValueError:
                    numero = 0
                    print('Digite um numero válido.')
                    continue
                current_account = selecionarConta(numero, current_user)
                
                if current_account:
                    menu_lvl += 1

            case 'lc': # listar contas
                print('\n========== CONTAS ==========')
                for conta in current_user.contas:
                    print(conta)
                print('\n============================')
            
            case 'cc': # criar conta
                conta = ContaCorrente.nova_conta(ultima_conta, current_user)
                current_user.adicionar_conta(conta)
                ultima_conta += 1
            
            case 'a': # acessar
                cpf = input('Digite seu CPF: ')
                current_user = fazerLogin(cpf, lista_clientes)
                
                if current_user:
                    menu_lvl += 1
            
            case 'nu':  # criar novo usuario
                data = getPersonalData()
                if all(data):
                    nome, data_nascimento, cpf, endereco = data
                    lista_clientes.append(PessoaFisica(nome, data_nascimento, cpf, endereco))
           
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
