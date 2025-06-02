def menu():
    menu_texto = '''
    ╔══════════════════════════════════╗
      𓂀  SEJA BEM-VINDO AO DIOBANK 𓂀
    ╚══════════════════════════════════╝
    Escolha uma opção:

    ➀ Depositar
    ➁ Sacar
    ➂ Extrato
    ➃ Contato
    ➄ Criar Usuário
    ➅ Criar Conta
    ➆ Sair
    '''
    return input(menu_texto + "=> ")

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n☰☰☰ Depósito realizado com sucesso! ☰☰☰")
    else:
        print("\n△ Operação falhou! O valor informado é inválido. △")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("\n△ Operação falhou! Você não tem saldo suficiente. △")
    elif valor > limite:
        print("\n△ Operação falhou! O valor do saque excede o limite. △")
    elif numero_saques >= limite_saques:
        print("\n△ Operação falhou! Número máximo de saques excedido. △")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n☰☰☰ Saque realizado com sucesso! ☰☰☰")
    else:
        print("\n△ Operação falhou! O valor informado é inválido. △")
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato):
    print("\n══════════════ EXTRATO ══════════════")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("═════════════════════════════════════")

def contato():
    print("\n╔═══════════════════════════════╗")
    print("      𓂀  CONTATO DIOBANK      ")
    print("╚═══════════════════════════════╝")
    print("E-mail: diobank@email.com")
    print("Telefone: (12) 3456-7890")
    print("Site: www.diobank.com.br")

def criar_usuario():
    cpf = input("Informe o CPF (somente números): ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n△ Usuário já cadastrado com esse CPF. △")
        return
    nome = input("Nome completo: ").strip().title()
    nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Endereço (logradouro, nro, bairro, cidade/UF): ").strip()
    usuarios.append({
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("\n☰☰☰ Usuário criado com sucesso! ☰☰☰")

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_conta():
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n△ Usuário não encontrado. Crie o usuário primeiro. △")
        return
    numero_conta = len(contas) + 1
    conta = {
        "agencia": "0001",
        "numero_conta": numero_conta,
        "usuario": usuario
    }
    contas.append(conta)
    print("\n☰☰☰ Conta criada com sucesso! ☰☰☰")
    print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}")

def main():
    nome = input("Digite seu nome: ").strip().title()
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: R$ "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "3":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            contato()

        elif opcao == "5":
            criar_usuario()

        elif opcao == "6":
            criar_conta()

        elif opcao == "7":
            print(f"\nAté logo, {nome}!\n")
            break

        else:
            print("\n△ Opção inválida, tente novamente. △")

# Listas globais para usuários e contas
usuarios = []
contas = []

main()
