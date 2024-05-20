from datetime import date, datetime
import textwrap

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
        if isinstance(transacao, Deposito):
            conta.depositar(transacao.valor)
        elif isinstance(transacao, Saque):
            conta.sacar(transacao.valor)
        conta.historico.adicionar_transacao(transacao)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @staticmethod
    def nova_conta(cliente, numero):
        return Conta(0, numero, "0001", cliente)

    def sacar(self, valor: float):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, limite: float, limite_saques: int):
        super().__init__(saldo, numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor: float):
        if self.numero_saques < self.limite_saques and valor <= self.limite:
            if super().sacar(valor):
                self.numero_saques += 1
                return True
        return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

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

def depositar(conta, valor):
    if valor <= 0:
        print("\n@@@ Valor de depósito inválido. @@@")
        return
    transacao = Deposito(valor)
    conta.cliente.realizar_transacao(conta, transacao)
    print("\n=== Depósito realizado com sucesso! ===")

def sacar(conta, valor):
    if valor <= 0:
        print("\n@@@ Valor de saque inválido. @@@")
        return
    transacao = Saque(valor)
    if conta.cliente.realizar_transacao(conta, transacao):
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Falha na operação de saque. Verifique saldo e limite. @@@")

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao.__class__.__name__}:\tR$ {transacao.valor:.2f}")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    if cpf in usuarios:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = datetime.strptime(input("Informe a data de nascimento (dd-mm-aaaa): "), "%d-%m-%Y").date()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = Cliente(cpf, nome, data_nascimento, endereco)
    usuarios[cpf] = usuario

    print("=== Usuário criado com sucesso! ===")

def criar_conta(numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = usuarios.get(cpf)

    if usuario:
        conta = ContaCorrente(0, numero_conta, "0001", usuario, 500, 3)
        usuario.adicionar_conta(conta)
        contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = {}
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do depósito: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)

            if conta:
                depositar(conta, valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do saque: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)

            if conta:
                sacar(conta, valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)

            if conta:
                exibir_extrato(conta)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()