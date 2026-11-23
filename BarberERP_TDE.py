
# BARBERERP

clientes = []
servicos = []
fila = []
historico = []


# CLIENTES - CRUD

def cadastrar_cliente():
    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()

    if nome == "" or telefone == "":
        print("Preencha todos os campos.")
        return

    cliente = {
        "id": max([c["id"] for c in clientes], default=0) + 1,
        "nome": nome,
        "telefone": telefone
    }

    clientes.append(cliente)
    historico.append(("cliente", cliente))
    print("Cliente cadastrado!")


def listar_clientes():
    for c in clientes:
        print(c)


def alterar_cliente():
    id_cliente = int(input("ID do cliente: "))

    for c in clientes:
        if c["id"] == id_cliente:
            c["nome"] = input("Novo nome: ")
            c["telefone"] = input("Novo telefone: ")
            print("Cliente alterado!")
            return

    print("Cliente nao encontrado.")


def remover_cliente():
    id_cliente = int(input("ID do cliente: "))

    for c in clientes:
        if c["id"] == id_cliente:
            clientes.remove(c)
            historico.append(("remover_cliente", c))
            print("Cliente removido!")
            return

    print("Cliente nao encontrado.")


# SERVICOS - CRUD

def cadastrar_servico():
    nome = input("Nome do servico: ")
    preco = float(input("Preco: "))
    duracao = int(input("Duracao em minutos: "))

    if nome.strip() == "" or preco <= 0 or duracao <= 0:
        print("Dados invalidos.")
        return

    servico = {
        "id": max([s["id"] for s in servicos], default=0) + 1,
        "nome": nome,
        "preco": preco,
        "duracao": duracao
    }

    servicos.append(servico)
    historico.append(("servico", servico))
    print("Servico cadastrado!")


def listar_servicos():
    for s in servicos:
        print(s)


def alterar_servico():
    id_servico = int(input("ID do servico: "))

    for s in servicos:
        if s["id"] == id_servico:
            s["nome"] = input("Novo nome: ")
            s["preco"] = float(input("Novo preco: "))
            s["duracao"] = int(input("Nova duracao: "))
            print("Servico alterado!")
            return

    print("Servico nao encontrado.")


def remover_servico():
    id_servico = int(input("ID do servico: "))

    for s in servicos:
        if s["id"] == id_servico:
            servicos.remove(s)
            historico.append(("remover_servico", s))
            print("Servico removido!")
            return

    print("Servico nao encontrado.")


# BUSCA LINEAR

def buscar_cliente():
    telefone = input("Telefone para buscar: ")

    for c in clientes:
        if c["telefone"] == telefone:
            print("Encontrado:", c)
            return

    print("Cliente nao encontrado.")


# FILA DE PRIORIDADE

def cadastrar_atendimento():
    if not clientes or not servicos:
        print("Cadastre clientes e servicos primeiro.")
        return

    listar_clientes()
    id_cliente = int(input("ID do cliente: "))

    cliente = None
    for c in clientes:
        if c["id"] == id_cliente:
            cliente = c

    if cliente is None:
        print("Cliente nao encontrado.")
        return

    listar_servicos()
    id_servico = int(input("ID do servico: "))

    servico = None
    for s in servicos:
        if s["id"] == id_servico:
            servico = s

    if servico is None:
        print("Servico nao encontrado.")
        return

    prioridade = int(input("Prioridade (1 baixa, 2 normal, 3 alta): "))

    if prioridade not in [1, 2, 3]:
        print("Prioridade invalida.")
        return

    atendimento = {
        "cliente": cliente["nome"],
        "servico": servico["nome"],
        "prioridade": prioridade
    }

    fila.append(atendimento)
    print("Atendimento adicionado!")


def listar_fila():
    for a in fila:
        print(a)


def atender():
    if not fila:
        print("Fila vazia.")
        return

    maior = 0

    for i in range(1, len(fila)):
        if fila[i]["prioridade"] > fila[maior]["prioridade"]:
            maior = i

    atendimento = fila.pop(maior)
    historico.append(("atendimento", atendimento))
    print("Atendendo:", atendimento)


# PILHA E HISTORICO

def ver_historico():
    for acao in reversed(historico):
        print(acao)


def desfazer():
    if not historico:
        print("Historico vazio.")
        return

    tipo, dado = historico.pop()

    if tipo == "cliente" and dado in clientes:
        clientes.remove(dado)

    elif tipo == "servico" and dado in servicos:
        servicos.remove(dado)

    elif tipo == "remover_cliente":
        clientes.append(dado)

    elif tipo == "remover_servico":
        servicos.append(dado)

    elif tipo == "atendimento":
        fila.append(dado)

    print("Ultima acao desfeita.")


# ORDENACAO MANUAL - SELECTION SORT

def ordenar_servicos():
    lista = servicos.copy()

    for i in range(len(lista)):
        menor = i

        for j in range(i + 1, len(lista)):
            if lista[j]["preco"] < lista[menor]["preco"]:
                menor = j

        lista[i], lista[menor] = lista[menor], lista[i]

    for s in lista:
        print(s["nome"], "- R$", s["preco"])


# RELATORIO COM FILTRO

def filtrar_servicos():
    minimo = float(input("Preco minimo: "))

    for s in servicos:
        if s["preco"] >= minimo:
            print(s)


# MENU PRINCIPAL

while True:
    print("""
===== BARBERERP =====
1 - Cadastrar cliente
2 - Listar clientes
3 - Alterar cliente
4 - Remover cliente
5 - Buscar cliente
6 - Cadastrar servico
7 - Listar servicos
8 - Alterar servico
9 - Remover servico
10 - Cadastrar atendimento
11 - Ver fila
12 - Atender proximo
13 - Ver historico
14 - Desfazer ultima acao
15 - Ordenar servicos por preco
16 - Filtrar servicos por preco
0 - Sair
""")

    opcao = input("Opcao: ")

    if opcao == "1":
        cadastrar_cliente()
    elif opcao == "2":
        listar_clientes()
    elif opcao == "3":
        alterar_cliente()
    elif opcao == "4":
        remover_cliente()
    elif opcao == "5":
        buscar_cliente()
    elif opcao == "6":
        cadastrar_servico()
    elif opcao == "7":
        listar_servicos()
    elif opcao == "8":
        alterar_servico()
    elif opcao == "9":
        remover_servico()
    elif opcao == "10":
        cadastrar_atendimento()
    elif opcao == "11":
        listar_fila()
    elif opcao == "12":
        atender()
    elif opcao == "13":
        ver_historico()
    elif opcao == "14":
        desfazer()
    elif opcao == "15":
        ordenar_servicos()
    elif opcao == "16":
        filtrar_servicos()
    elif opcao == "0":
        break
    else:
        print("Opcao invalida.")