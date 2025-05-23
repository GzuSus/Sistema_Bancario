import textwrap
from datetime import datetime

def home():
    nome = input("\nDigite seu nome para continuar: ")
    nome_formatado = nome.title()
    return nome_formatado

def menu(nome):
    menu_texto = f'''\

    ۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩ ᴍᴇɴᴜ ۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩
    Olá, {nome}!

    ➀ Depositar
    ➁ Sacar
    ➂ Extrato
    ➃ Contato
    ➄ Sair
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

def main():
    nome = home()  # Primeiro chama o home

    LIMITE_SAQUES = 3
    LIMITE_OPERACOES_DIARIAS = 10

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    contador_operacoes_dia = 0
    data_ultima_operacao = datetime.now().date()

    while True:
        # Verifica se mudou o dia para resetar o contador
        data_atual = datetime.now().date()
        if data_atual != data_ultima_operacao:
            contador_operacoes_dia = 0
            numero_saques = 0  # reseta também os saques diários
            data_ultima_operacao = data_atual

        opcao = menu(nome)

        # Antes de qualquer operação que conta, verifica limite diário
        if opcao in ["1", "2"]:
            if contador_operacoes_dia >= LIMITE_OPERACOES_DIARIAS:
                print("\n△△△ Limite diário de 10 operações atingido. Tente novamente amanhã. △△△")
                continue

        if opcao == "1":
            valor = input("Informe o valor do depósito: ")
            saldo, extrato = depositar(saldo, valor, extrato)
            # Se depósito válido, conta a operação
            if valor and validar_valor(valor) is not None:
                contador_operacoes_dia += 1

        elif opcao == "2":
            valor = input("Informe o valor do saque: ")
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            # Se saque válido (saldo suficiente, limite e saques OK), conta a operação
            if valor and validar_valor(valor) is not None:
                contador_operacoes_dia += 1

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            print('''\nEntre em contato com a agência:
            ☏ (00) 12345-6789
            ✆ (10) 98765-4321
            ✉ contato@bancodio.com\n''')
        
        elif opcao == "5":
            print(f"\nAté logo, {nome}!\n")
            break

        else:
            print("\n△ Operação inválida. Tente novamente. △")

main()
