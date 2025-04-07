menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[lu] Listar usuários
[cc] Criar conta corrente
[lc] Listar contas
[q] Sair

=> """

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excede_val = valor > saldo
    excede_num_limite = numero_saques >= limite_saques 
    excede_limite = valor > limite

    if excede_num_limite:
        print("O número de saques já alcançou o seu limite.")
    elif excede_val:
        print("O valor pretendido supera o seu saldo.")
    elif excede_limite:
        print(f"O seu plano não cobre valores acima de R$ {limite:.2f}")
    else:
        saldo -= valor
        extrato += f"\nSaque: R$ {valor:.2f}"
        numero_saques += 1
    return saldo, extrato

def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"\nDepósito: R$ {valor:.2f}"
    else:
        print("Valor inválido para depósito.")
    return saldo, extrato

def visualizar_historico(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato.strip() else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=========================================")

def cadastrar_usuario(usuarios):
    cpf = input("Insira seu CPF: ")

    if cpf in usuarios:
        print("⚠️ CPF já cadastrado. Usuário não será criado.")
        return

    nome = input("Insira seu nome: ")
    data_nascimento = input("Insira a data de nascimento DD-MM-YYYY: ")
    nro = input("Insira o número da sua residência: ")
    bairro = input("Insira o seu bairro: ")
    cidade = input("Insira Cidade/UF: ")

    endereco = f"{nro} - {bairro} - {cidade}"
    print("Endereço completo:", endereco)

    usuario_dado = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }

    usuarios[cpf] = usuario_dado
    print("Usuário cadastrado com sucesso!")

def listar_usuarios(usuarios):
    print("\n=== Usuários cadastrados ===")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    for cpf_key, dados in usuarios.items():
        print(f"\nCPF: {cpf_key}")
        print("Nome:", dados["nome"])
        print("Nascimento:", dados["data_nascimento"])
        print("Endereço:", dados["endereco"])
    print("=============================")

def nova_conta_corrente(agencia, usuarios, contas, num_conta):
    cpf = input("Informe o CPF do titular da conta: ")

    if cpf not in usuarios:
        print("CPF não encontrado. Cadastre o usuário antes de criar uma conta.")
        return num_conta 
    nome = usuarios[cpf]["nome"]

    conta = {
        "agencia": agencia,
        "num_conta": num_conta,
        "titular": nome,
        "cpf": cpf  
    }

    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {agencia}, Conta: {num_conta}, Titular: {nome}")

    return num_conta + 1 

num_conta = 1
saldo = 0
limite = 500
contas = []
extrato = ""
usuarios = {} 
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = deposito(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato = saque(
            saldo=saldo,
            valor=valor,
            extrato=extrato, 
            limite=limite, 
            numero_saques=numero_saques, 
            limite_saques=LIMITE_SAQUES
        )
        numero_saques += 1  # Atualiza fora da função para não perder valor

    elif opcao == "e":
        visualizar_historico(saldo, extrato=extrato)

    elif opcao == "nu":
        cadastrar_usuario(usuarios)

    elif opcao == "lu":
        listar_usuarios(usuarios)

    elif opcao == "cc":
        num_conta = nova_conta_corrente(AGENCIA, usuarios, contas, num_conta)
    
    elif opcao == "lc":
        if not contas:
            print("Nenhuma conta cadastrada.")
        else:
            print("\n=== Contas cadastradas ===")
            for conta in contas:
                print(f"Agência: {conta['agencia']} | Conta: {conta['num_conta']} | Titular: {conta['titular']} | CPF: {conta['cpf']}")
    elif opcao == "q":
        print("Saindo... até logo!")
        break

    else:
        print("Operação inválida. Tente novamente.")
