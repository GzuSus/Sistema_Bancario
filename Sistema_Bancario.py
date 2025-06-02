import textwrap
from datetime import datetime

def menu():
    menu_texto = '''\

    ۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩ ᴍᴇɴᴜ ۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩
    ➀ Criar Usuário
    ➁ Criar Conta
    ➂ Listar Contas
    ➃ Depositar
    ➄ Sacar
    ➅ Extrato
    ➆ Contato
    ➇ Sair
    ► '''
    return input(textwrap.dedent(menu_texto))

def validar_valor(valor):
    try:
        valor = float(valor)
        if valor <= 0:
            print("\n△△△ O valor deve ser maior que zero. △△△")
            return None
        return valor
    except ValueError:
        print("\n△△△ Valor inválido! Por favor, insira um número válido. △△△")
        return None

def depositar(saldo, valor, extrato, /):
    valor = validar_valor(valor)
    if valor is not None:
        saldo += valor
        extrato += f"{datetime.now():%d/%m/%Y %H:%M:%S} - Depósito:\tR$ {valor:.2f}\n"
        print("\n☰☰☰ Depósito realizado com sucesso! ☰☰☰")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    valor = validar_valor(valor)
    if valor is None:
        return saldo, extrato, numero_saques

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n△△△ Operação falhou! Você não tem saldo suficiente. △△△")
    elif excedeu_limite:
        print("\n△△△ Operação falhou! O valor do saque excede o limite. △△△")
    elif excedeu_saques:
        print("\n△△△ Operação falhou! Número máximo de saques excedido. △△△")
    else:
        saldo -= valor
        extrato += f"{datetime.now():%d/%m/%Y %H:%M:%S} - Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n☰☰☰ Saque realizado com sucesso! ☰☰☰")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n☰☰☰☰☰☰☰☰ EXTRATO ☰☰☰☰☰☰☰☰")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("\n△ Usuário com esse CPF já existe! △")
        return
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (logradouro, número - bairro - cidade/sigla estado): ")
    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })
    print("\n☰☰☰ Usuário criado com sucesso! ☰☰☰")

def buscar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = buscar_usuario(cpf, usuarios)
    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        print("\n☰☰☰ Conta criada com sucesso! ☰☰☰")
        return numero_conta + 1
    print("\n△ Usuário não encontrado. △")
    return numero_conta

def listar_contas(contas):
    if not contas:
        print("\n△ Nenhuma conta cadastrada. △")
        return
    for conta in contas:
        print(f'''
☰☰☰ Conta ☰☰☰
Agência:\t{conta["agencia"]}
Conta Nº:\t{conta["numero_conta"]}
Titular:\t{conta["usuario"]["nome"]}
CPF:\t\t{conta["usuario"]["cpf"]}
        ''')

def main():
    LIMITE_SAQUES = 3
    LIMITE_OPERACOES_DIARIAS = 10

    AGENCIA = "0001"
    usuarios = []
    contas = []

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    contador_operacoes_dia = 0
    data_ultima_operacao = datetime.now().date()
    numero_conta = 1

    while True:
        # Verifica se mudou o dia para resetar contadores
        data_atual = datetime.now().date()
        if data_atual != data_ultima_operacao:
            contador_operacoes_dia = 0
            numero_saques = 0
            data_ultima_operacao = data_atual

        opcao = menu()

        if opcao in ["4", "5"]:
            if contador_operacoes_dia >= LIMITE_OPERACOES_DIARIAS:
                print("\n△△△ Limite diário de 10 operações atingido. Tente novamente amanhã. △△△")
                continue

        if opcao == "1":
            criar_usuario(usuarios)

        elif opcao == "2":
            numero_conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "3":
            listar_contas(contas)

        elif opcao == "4":
            valor = input("Informe o valor do depósito: ")
            saldo, extrato = depositar(saldo, valor, extrato)
            if valor and validar_valor(valor) is not None:
                contador_operacoes_dia += 1

        elif opcao == "5":
            valor = input("Informe o valor do saque: ")
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            if valor and validar_valor(valor) is not None:
                contador_operacoes_dia += 1

        elif opcao == "6":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "7":
            print('''\nEntre em contato com a agência:
            ☏ (00) 12345-6789
            ✆ (10) 98765-4321
            ✉ contato@bancodio.com\n''')

        elif opcao == "8":
            print("\nAté logo!\n")
            break

        else:
            print("\n△ Operação inválida. Tente novamente. △")

main()