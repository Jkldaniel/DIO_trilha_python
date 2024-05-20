# Definição das classes baseadas no diagrama UML

from datetime import date

class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_nascimento: date):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Cliente(PessoaFisica):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(cpf, nome, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def nova_conta(cls, cliente, numero):
        return cls(0.0, numero, "0001", cliente)

    def sacar(self, valor: float):
        if valor <= self.saldo:
            self.saldo -= valor
            self.historico.adicionar_transacao(Saque(valor))
            return True
        return False

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(Deposito(valor))
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, limite: float, limite_saques: int):
        super().__init__(saldo, numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: Conta):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses")

class Deposito(Transacao):
    def registrar(self, conta: Conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def registrar(self, conta: Conta):
        conta.sacar(self.valor)

# Vamos agora atualizar as funções principais do sistema para utilizarem as classes modeladas.

import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(conta: Conta, valor: float):
    if conta.depositar(valor):
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

def sacar(conta: Conta, valor: float):
    if conta.sacar(valor):
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! Saldo insuficiente ou valor inválido. @@@")

def exibir_extrato(conta: Conta):
    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            tipo = "Depósito" if isinstance(transacao, Deposito) else "Saque"
            print(f"{tipo}:\tR$ {transacao.valor:.2f}")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_usuario(clientes: list):
    cpf = input("Informe o CPF (somente número): ")
    if any(cliente.cpf == cpf for cliente in clientes):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = Cliente(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)
    print("=== Usuário criado com sucesso! ===")

def criar_conta(clientes: list, contas: list):
    cpf = input("Informe o CPF do usuário: ")
    cliente = next((cliente for cliente in clientes if cliente.cpf == cpf), None)
    if not cliente:
        print("\n@@@ Usuário não encontrado! @@@")
        return

    numero_conta = len(contas) + 1
    conta = Conta(0.0, numero_conta, "0001", cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas: list):
    for conta in contas:
        print("=" * 100)
        print(f"Agência:\t{conta.agencia}")
        print(f"C/C:\t\t{conta.numero}")
        print(f"Titular:\t{conta.cliente.nome}")

def main():
    LIMITE_SAQUES = 3
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if not conta:
                print("\n@@@ Conta não encontrada! @@@")
                continue

            valor = float(input("Informe o valor do depósito: "))
            depositar(conta, valor)

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if not conta:
                print("\n@@@ Conta não encontrada! @@@")
                continue

            valor = float(input("Informe o valor do saque: "))
            sacar(conta, valor)

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if not conta:
                print("\n@@@ Conta não encontrada! @@@")
                continue

            exibir_extrato(conta)

        elif opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "nc":
            criar_conta(clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Descomentar a chamada da função main para execução
main()
