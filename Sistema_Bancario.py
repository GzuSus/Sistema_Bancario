from abc import ABC, abstractmethod


# Transações
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# Histórico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


# Conta
class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor:.2f} realizado.")
            return True
        print("Saque não permitido.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(f"Depósito de R${valor:.2f} realizado.")
            return True
        print("Valor inválido para depósito.")
        return False


# Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False
        if valor <= (self.saldo + self.limite):
            if super().sacar(valor):
                self.saques_realizados += 1
                return True
        print("Saldo insuficiente com limite.")
        return False


# Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# Pessoa Física
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# Listas de clientes e contas
clientes = []
contas = []

def exibir_clientes():
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    print("\n=== Lista de Clientes ===")
    for cliente in clientes:
        print(f"Nome: {cliente.nome} | CPF: {cliente.cpf} | Contas: {len(cliente.contas)}")
    print("=========================\n")

# Funções auxiliares
def encontrar_cliente(cpf):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None


# Ações do menu
def criar_cliente():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço: ")

    if encontrar_cliente(cpf):
        print("Cliente já existe.")
        return

    cliente = PessoaFisica(nome, cpf, nascimento, endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso.")


def criar_conta():
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente(cpf)

    if not cliente:
        print("Cliente não encontrado.")
        return

    numero = len(contas) + 1
    conta = ContaCorrente(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("Conta criada com sucesso.")


def depositar():
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente(cpf)

    if not cliente or not cliente.contas:
        print("Cliente ou conta não encontrada.")
        return

    valor = float(input("Valor do depósito: "))
    conta = cliente.contas[0]
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar():
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente(cpf)

    if not cliente or not cliente.contas:
        print("Cliente ou conta não encontrada.")
        return

    valor = float(input("Valor do saque: "))
    conta = cliente.contas[0]
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato():
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente(cpf)

    if not cliente or not cliente.contas:
        print("Cliente ou conta não encontrada.")
        return

    conta = cliente.contas[0]
    print(f"=== Extrato da Conta {conta.numero} ===")
    print(f"Saldo atual: R${conta.saldo:.2f}")
    print("Transações:")
    for t in conta.historico.transacoes:
        tipo = t.__class__.__name__
        print(f"{tipo}: R${t.valor:.2f}")
    print("===============================")

def exibir_contato():
    print('''\nEntre em contato com a agência:
            ☏ (00) 12345-6789
            ✆ (10) 98765-4321
            ✉ contato@bancodio.com\n''')

# Menu principal
def menu():
    opcoes = {
        "1": criar_cliente,
        "2": criar_conta,
        "3": depositar,
        "4": sacar,
        "5": exibir_extrato,
        "6": exibir_clientes,
        "7": exibir_contato,
        "0": lambda: print("Saindo do sistema...")
    }

    while True:
        print("""
        ۩۩۩۩۩۩ DIOBANK ۩۩۩۩۩۩
        1 - Criar cliente
        2 - Criar conta
        3 - Depositar
        4 - Sacar
        5 - Extrato
        6 - Mostrar Clientes
        7 - Contato
        0 - Sair
        """)
        opcao = input("Escolha: ")

        acao = opcoes.get(opcao)
        if acao:
            acao()
            if opcao == "0":
                break
        else:
            print("Opção inválida!")


# Executar o menu
if __name__ == "__main__":
    menu()
