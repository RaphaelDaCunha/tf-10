
from collections import deque


class MiniGit:
    # Controla os commits, branches e o histórico.

    __slots__ = (
        "__pais",
        "__mensagens",
        "__branches",
        "__branch_atual",
        "__contador",
        "__passos"
    )

    def __init__(self):
        # Inicializa o repositório vazio: 0 passos.
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__contador = 0
        self.__passos = 0

    @property
    def passos(self):
        # Consulta os passos da última operação.
        return self.__passos

    @property
    def branch_atual(self):
        # Consulta a branch atual.
        return self.__branch_atual

    # Cria um commit e move o ponteiro: 2 passos.
    def commitar(self, mensagem):
        if not mensagem:
            self.__passos = 0
            raise ValueError("Mensagem vazia")

        self.__contador += 1
        identificador = "c" + str(self.__contador)

        commit_anterior = self.__branches[self.__branch_atual]
        lista_pais = []

        if commit_anterior is not None:
            lista_pais.append(commit_anterior)

        self.__pais[identificador] = lista_pais
        self.__mensagens[identificador] = mensagem
        self.__branches[self.__branch_atual] = identificador

        self.__passos = 2
        return identificador

    # Consulta a mensagem pelo dicionário: 1 passo.
    def mensagem(self, commit):
        if commit not in self.__mensagens:
            self.__passos = 0
            raise ValueError("Commit não existe")

        self.__passos = 1
        return self.__mensagens[commit]

    # Retorna os pais em uma tupla: 1 passo.
    def pais(self, commit):
        if commit not in self.__pais:
            self.__passos = 0
            raise ValueError("Commit não existe")

        self.__passos = 1
        return tuple(self.__pais[commit])

    # Cria uma branch: 1 passo.
    def criar_branch(self, nome):
        if nome in self.__branches:
            self.__passos = 0
            raise ValueError("Branch já existe")

        commit_atual = self.__branches[self.__branch_atual]

        if commit_atual is None:
            self.__passos = 0
            raise ValueError("Não existem commits")

        self.__branches[nome] = commit_atual
        self.__passos = 1

    # Troca a branch atual: 1 passo.
    def trocar_branch(self, nome):
        if nome not in self.__branches:
            self.__passos = 0
            raise ValueError("Branch não existe")

        self.__branch_atual = nome
        self.__passos = 1

    # Cria um commit com dois pais: 2 passos.
    def mesclar(self, nome):
        if nome not in self.__branches:
            self.__passos = 0
            raise ValueError("Branch não existe")

        if nome == self.__branch_atual:
            self.__passos = 0
            raise ValueError("Não pode mesclar a própria branch")

        primeiro_pai = self.__branches[self.__branch_atual]
        segundo_pai = self.__branches[nome]

        if primeiro_pai is None or segundo_pai is None:
            self.__passos = 0
            raise ValueError("Não existem commits para mesclar")

        self.__contador += 1
        identificador = "c" + str(self.__contador)

        self.__pais[identificador] = [primeiro_pai, segundo_pai]
        self.__mensagens[identificador] = "merge de " + nome
        self.__branches[self.__branch_atual] = identificador

        self.__passos = 2
        return identificador

    # Percorre o histórico com uma fila: 1 passo por commit visitado.
    def log(self):
        fila = deque()
        commit_atual = self.__branches[self.__branch_atual]

        if commit_atual is not None:
            fila.append(commit_atual)

        visitados = set()
        resultado = []

        while fila:
            commit = fila.popleft()

            if commit in visitados:
                continue

            visitados.add(commit)
            resultado.append(commit)

            for pai in self.__pais[commit]:
                fila.append(pai)

        self.__passos = len(resultado)
        return tuple(resultado)

    # Procura texto nas mensagens: 1 passo por commit olhado.
    def buscar(self, texto):
        self.__passos = 0

        for identificador in self.__mensagens:
            self.__passos += 1

            if texto in self.__mensagens[identificador]:
                return identificador

        return None

    # Procura commits com mais de um pai: 1 passo por commit.
    def merges(self):
        resultado = []
        self.__passos = 0

        for identificador in self.__pais:
            self.__passos += 1

            if len(self.__pais[identificador]) > 1:
                resultado.append(identificador)

        return tuple(resultado)


# Executa uma ação e apresenta erros.
def tentar(acao):
    try:
        acao()
    except ValueError as erro:
        print("erro:", erro)


# Testes principais.

git = MiniGit()
git.commitar("primeiro commit")
print(git.passos)

git.commitar("segundo commit")
git.criar_branch("feature")
print(git.passos)

git.commitar("terceiro commit")
git.trocar_branch("feature")
git.commitar("quarto commit")
git.trocar_branch("main")
git.mesclar("feature")

print(git.pais("c5"))
print(git.log(), git.passos)
print(git.mensagem("c3"), git.passos)
print(git.buscar("quarto"), git.passos)
print(git.merges())

git.trocar_branch("feature")
print(git.log(), git.passos)
git.trocar_branch("main")


# Testes de erros.

tentar(lambda: git.trocar_branch("inexistente"))
tentar(lambda: git.criar_branch("main"))
tentar(lambda: git.mesclar("main"))
tentar(lambda: git.pais("c99"))


# Mede os passos de escrita e leitura.
def medir(quantidade):
    git_teste = MiniGit()

    for numero in range(quantidade):
        git_teste.commitar("commit " + str(numero))

    passos_commitar = git_teste.passos

    git_teste.log()
    passos_log = git_teste.passos

    return passos_commitar, passos_log


# Apresenta a tabela de medição.

print("\nTabela de medição")
print("commits   passos do commitar   passos do log")

for quantidade in (10, 100, 1000):
    passos_commitar, passos_log = medir(quantidade)
    print(quantidade, passos_commitar, passos_log)
