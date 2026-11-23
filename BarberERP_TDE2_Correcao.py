# BARBERERP (TDE2)

# FUNCOES AUXILIARES

def ler_int(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        print("Digite um numero inteiro valido.")
        return None


def ler_float(mensagem):
    try:
        return float(input(mensagem).replace(",", "."))
    except ValueError:
        print("Digite um numero valido.")
        return None


def dados_publicos(atendimento):
    return {
        "cliente": atendimento["cliente"],
        "servico": atendimento["servico"],
        "prioridade": atendimento["prioridade"]
    }


# ARVORE AVL 

class NoAVL:
    def __init__(self, dado):
        self.chave = dado["id"]
        self.dado = dado
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.quantidade = 0

    def altura(self, no):
        if no is None:
            return 0
        return no.altura

    def atualizar_altura(self, no):
        altura_esquerda = self.altura(no.esquerda)
        altura_direita = self.altura(no.direita)
        if altura_esquerda > altura_direita:
            no.altura = altura_esquerda + 1
        else:
            no.altura = altura_direita + 1

    def fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotacao_direita(self, y):
        x = y.esquerda
        auxiliar = x.direita

        x.direita = y
        y.esquerda = auxiliar

        self.atualizar_altura(y)
        self.atualizar_altura(x)
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        auxiliar = y.esquerda

        y.esquerda = x
        x.direita = auxiliar

        self.atualizar_altura(x)
        self.atualizar_altura(y)
        return y

    def balancear(self, no):
        if no is None:
            return None

        self.atualizar_altura(no)
        fator = self.fator_balanceamento(no)

        # esquerda-esquerda ou esquerda-direita.
        if fator > 1:
            if self.fator_balanceamento(no.esquerda) < 0:
                no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)

        # direita-direita ou direita-esquerda.
        if fator < -1:
            if self.fator_balanceamento(no.direita) > 0:
                no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)

        return no

    def _inserir(self, no, dado):
        if no is None:
            return NoAVL(dado)

        if dado["id"] < no.chave:
            no.esquerda = self._inserir(no.esquerda, dado)
        elif dado["id"] > no.chave:
            no.direita = self._inserir(no.direita, dado)
        else:
            no.dado = dado
            return no

        return self.balancear(no)

    def inserir(self, dado):
        existente = self.buscar(dado["id"])
        self.raiz = self._inserir(self.raiz, dado)
        if existente is None:
            self.quantidade += 1

    def buscar(self, chave):
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return atual.dado
            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def buscar_por_campo(self, campo, valor):
        return self._buscar_por_campo(self.raiz, campo, valor)

    def _buscar_por_campo(self, no, campo, valor):
        if no is None:
            return None
        if no.dado.get(campo) == valor:
            return no.dado

        encontrado = self._buscar_por_campo(no.esquerda, campo, valor)
        if encontrado is not None:
            return encontrado
        return self._buscar_por_campo(no.direita, campo, valor)

    def _menor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _remover(self, no, chave):
        if no is None:
            return None

        if chave < no.chave:
            no.esquerda = self._remover(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remover(no.direita, chave)
        else:
            if no.esquerda is None:
                return no.direita
            if no.direita is None:
                return no.esquerda

            sucessor = self._menor_no(no.direita)
            no.chave = sucessor.chave
            no.dado = sucessor.dado
            no.direita = self._remover(no.direita, sucessor.chave)

        return self.balancear(no)

    def remover(self, chave):
        dado = self.buscar(chave)
        if dado is None:
            return None
        self.raiz = self._remover(self.raiz, chave)
        self.quantidade -= 1
        return dado

    def maior_chave(self):
        """Retorna a maior chave sem percorrer todos os registros."""
        atual = self.raiz
        if atual is None:
            return 0
        while atual.direita is not None:
            atual = atual.direita
        return atual.chave

    # Travessias
    def percorrer(self, tipo="in"):
        resultado = []

        def visitar(no):
            if no is None:
                return

            if tipo == "pre":
                resultado.append(no.dado)

            visitar(no.esquerda)

            if tipo == "in":
                resultado.append(no.dado)

            visitar(no.direita)

            if tipo == "pos":
                resultado.append(no.dado)

        visitar(self.raiz)
        return resultado

    def __len__(self):
        return self.quantidade

    def __bool__(self):
        return self.raiz is not None


# FILA DE PRIORIDADE - HEAP MAXIMO 

class FilaPrioridade:
    def __init__(self):
        self.itens = []
        self.proxima_ordem = 0

    def __len__(self):
        return len(self.itens)

    def __bool__(self):
        return len(self.itens) > 0

    def _tem_prioridade(self, a, b):
        if a["prioridade"] != b["prioridade"]:
            return a["prioridade"] > b["prioridade"]
        return a["_ordem"] < b["_ordem"]

    def inserir(self, atendimento):
        novo = atendimento.copy()

        if "_ordem" not in novo:
            novo["_ordem"] = self.proxima_ordem
            self.proxima_ordem += 1
        elif novo["_ordem"] >= self.proxima_ordem:
            self.proxima_ordem = novo["_ordem"] + 1

        self.itens.append(novo)
        indice = len(self.itens) - 1

        while indice > 0:
            pai = (indice - 1) // 2
            if self._tem_prioridade(self.itens[indice], self.itens[pai]):
                self.itens[indice], self.itens[pai] = self.itens[pai], self.itens[indice]
                indice = pai
            else:
                break

    def remover_proximo(self):
        if not self.itens:
            return None

        primeiro = self.itens[0]
        ultimo = self.itens.pop()

        if self.itens:
            self.itens[0] = ultimo
            indice = 0

            while True:
                melhor = indice
                esquerdo = 2 * indice + 1
                direito = 2 * indice + 2

                if esquerdo < len(self.itens):
                    if self._tem_prioridade(self.itens[esquerdo], self.itens[melhor]):
                        melhor = esquerdo

                if direito < len(self.itens):
                    if self._tem_prioridade(self.itens[direito], self.itens[melhor]):
                        melhor = direito

                if melhor == indice:
                    break

                self.itens[indice], self.itens[melhor] = self.itens[melhor], self.itens[indice]
                indice = melhor

        return primeiro

    def listar(self):
        copia = FilaPrioridade()
        copia.itens = [item.copy() for item in self.itens]
        copia.proxima_ordem = self.proxima_ordem

        resultado = []
        while copia:
            resultado.append(dados_publicos(copia.remover_proximo()))
        return resultado


# ESTRUTURAS DO SISTEMA

clientes = ArvoreAVL()
servicos = ArvoreAVL()
fila = FilaPrioridade()
historico = []  

# CLIENTES - CRUD

def cadastrar_cliente():
    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()

    if nome == "" or telefone == "":
        print("Preencha todos os campos.")
        return

    cliente = {
        "id": clientes.maior_chave() + 1,
        "nome": nome,
        "telefone": telefone
    }

    clientes.inserir(cliente)
    historico.append(("cliente", cliente))
    print("Cliente cadastrado!")


def listar_clientes():
    for cliente in clientes.percorrer("in"):
        print(cliente)


def mostrar_travessia_clientes():
    print("1 - Em ordem")
    print("2 - Pre-ordem")
    print("3 - Pos-ordem")
    opcao = input("Travessia: ")

    tipos = {"1": "in", "2": "pre", "3": "pos"}
    if opcao not in tipos:
        print("Opcao invalida.")
        return

    for cliente in clientes.percorrer(tipos[opcao]):
        print(cliente)


def alterar_cliente():
    id_cliente = ler_int("ID do cliente: ")
    if id_cliente is None:
        return

    cliente = clientes.buscar(id_cliente)
    if cliente is None:
        print("Cliente nao encontrado.")
        return

    nome = input("Novo nome: ").strip()
    telefone = input("Novo telefone: ").strip()
    if nome == "" or telefone == "":
        print("Preencha todos os campos.")
        return

    cliente["nome"] = nome
    cliente["telefone"] = telefone
    print("Cliente alterado!")


def remover_cliente():
    id_cliente = ler_int("ID do cliente: ")
    if id_cliente is None:
        return

    cliente = clientes.remover(id_cliente)
    if cliente is None:
        print("Cliente nao encontrado.")
        return

    historico.append(("remover_cliente", cliente))
    print("Cliente removido!")


# SERVICOS - CRUD

def cadastrar_servico():
    nome = input("Nome do servico: ").strip()
    preco = ler_float("Preco: ")
    duracao = ler_int("Duracao em minutos: ")

    if nome == "" or preco is None or duracao is None or preco <= 0 or duracao <= 0:
        print("Dados invalidos.")
        return

    servico = {
        "id": servicos.maior_chave() + 1,
        "nome": nome,
        "preco": preco,
        "duracao": duracao
    }

    servicos.inserir(servico)
    historico.append(("servico", servico))
    print("Servico cadastrado!")


def listar_servicos():
    for servico in servicos.percorrer("in"):
        print(servico)


def mostrar_travessia_servicos():
    print("1 - Em ordem")
    print("2 - Pre-ordem")
    print("3 - Pos-ordem")
    opcao = input("Travessia: ")

    tipos = {"1": "in", "2": "pre", "3": "pos"}
    if opcao not in tipos:
        print("Opcao invalida.")
        return

    for servico in servicos.percorrer(tipos[opcao]):
        print(servico)


def alterar_servico():
    id_servico = ler_int("ID do servico: ")
    if id_servico is None:
        return

    servico = servicos.buscar(id_servico)
    if servico is None:
        print("Servico nao encontrado.")
        return

    nome = input("Novo nome: ").strip()
    preco = ler_float("Novo preco: ")
    duracao = ler_int("Nova duracao: ")

    if nome == "" or preco is None or duracao is None or preco <= 0 or duracao <= 0:
        print("Dados invalidos.")
        return

    servico["nome"] = nome
    servico["preco"] = preco
    servico["duracao"] = duracao
    print("Servico alterado!")


def remover_servico():
    id_servico = ler_int("ID do servico: ")
    if id_servico is None:
        return

    servico = servicos.remover(id_servico)
    if servico is None:
        print("Servico nao encontrado.")
        return

    historico.append(("remover_servico", servico))
    print("Servico removido!")


# BUSCA NA ARVORE

def buscar_cliente():
    telefone = input("Telefone para buscar: ").strip()
    cliente = clientes.buscar_por_campo("telefone", telefone)

    if cliente is not None:
        print("Encontrado:", cliente)
    else:
        print("Cliente nao encontrado.")


def buscar_cliente_por_id():
    id_cliente = ler_int("ID do cliente para buscar na AVL: ")
    if id_cliente is None:
        return

    cliente = clientes.buscar(id_cliente)
    if cliente is not None:
        print("Encontrado:", cliente)
    else:
        print("Cliente nao encontrado.")


# FILA DE PRIORIDADE

def cadastrar_atendimento():
    if not clientes or not servicos:
        print("Cadastre clientes e servicos primeiro.")
        return

    listar_clientes()
    id_cliente = ler_int("ID do cliente: ")
    if id_cliente is None:
        return

    cliente = clientes.buscar(id_cliente)
    if cliente is None:
        print("Cliente nao encontrado.")
        return

    listar_servicos()
    id_servico = ler_int("ID do servico: ")
    if id_servico is None:
        return

    servico = servicos.buscar(id_servico)
    if servico is None:
        print("Servico nao encontrado.")
        return

    prioridade = ler_int("Prioridade (1 baixa, 2 normal, 3 alta): ")
    if prioridade not in (1, 2, 3):
        print("Prioridade invalida.")
        return

    atendimento = {
        "cliente": cliente["nome"],
        "servico": servico["nome"],
        "prioridade": prioridade
    }

    fila.inserir(atendimento)
    print("Atendimento adicionado!")


def listar_fila():
    for atendimento in fila.listar():
        print(atendimento)


def atender():
    if not fila:
        print("Fila vazia.")
        return

    atendimento = fila.remover_proximo()
    historico.append(("atendimento", atendimento))
    print("Atendendo:", dados_publicos(atendimento))


# PILHA E HISTORICO REVERSIVEL

def ver_historico():
    for tipo, dado in reversed(historico):
        if tipo == "atendimento":
            print((tipo, dados_publicos(dado)))
        else:
            print((tipo, dado))


def desfazer():
    if not historico:
        print("Historico vazio.")
        return

    tipo, dado = historico.pop()

    if tipo == "cliente":
        clientes.remover(dado["id"])
    elif tipo == "servico":
        servicos.remover(dado["id"])
    elif tipo == "remover_cliente":
        clientes.inserir(dado)
    elif tipo == "remover_servico":
        servicos.inserir(dado)
    elif tipo == "atendimento":
        fila.inserir(dado)

    print("Ultima acao desfeita.")


# MERGE SORT 

def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    return intercalar(esquerda, direita)


def intercalar(esquerda, direita):
    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i]["preco"] <= direita[j]["preco"]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado


def ordenar_servicos():
    lista = merge_sort(servicos.percorrer("in"))

    for servico in lista:
        print(servico["nome"], "- R$", f'{servico["preco"]:.2f}')


# RELATORIO COM FILTRO

def filtrar_servicos():
    minimo = ler_float("Preco minimo: ")
    if minimo is None or minimo < 0:
        print("Preco minimo invalido.")
        return

    for servico in servicos.percorrer("in"):
        if servico["preco"] >= minimo:
            print(servico)


# MENU PRINCIPAL

while True:
    print("""
===== BARBERERP - VERSAO OTIMIZADA =====
1 - Cadastrar cliente
2 - Listar clientes (em ordem)
3 - Alterar cliente
4 - Remover cliente
5 - Buscar cliente por telefone
6 - Cadastrar servico
7 - Listar servicos (em ordem)
8 - Alterar servico
9 - Remover servico
10 - Cadastrar atendimento
11 - Ver fila
12 - Atender proximo
13 - Ver historico
14 - Desfazer ultima acao
15 - Ordenar servicos por preco (Merge Sort)
16 - Filtrar servicos por preco
17 - Travessias da arvore de clientes
18 - Travessias da arvore de servicos
19 - Buscar cliente por ID (AVL)
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
    elif opcao == "17":
        mostrar_travessia_clientes()
    elif opcao == "18":
        mostrar_travessia_servicos()
    elif opcao == "19":
        buscar_cliente_por_id()
    elif opcao == "0":
        break
    else:
        print("Opcao invalida.")
