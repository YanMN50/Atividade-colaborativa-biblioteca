"""
Alunos: Maria Luiza, Henrique Santos e Yan Mendes

"""


import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import time

db = create_engine("sqlite:///meubanco.db")

Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"

    matricula = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)

    def __init__(self, matricula:int, nome:str, email:str, senha:str):
        self.matricula = matricula
        self.nome = nome
        self.email = email
        self.senha = senha

class Funcionario(Base):
    __tablename__ = "funcionario"
    
    cpf = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)

    
    def __init__(self, cpf:int, nome:str, email:str, senha:str):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.senha = senha     

class Livros(Base):
    __tablename__ = "livro"

    titulo = Column(String)
    autor = Column(String)
    codigo = Column(Integer, primary_key=True)
    preco = Column(Integer)

    def __init__(self, titulo:str, autor:str, codigo:int, preco:int):
        self.titulo = titulo
        self.autor = autor
        self.codigo = codigo
        self.preco = preco

Base.metadata.create_all(bind=db)

class Carrinho:
    def __init__(self):
        self.itens = []  # Atributo para armazenar os livros no carrinho

carrinho = Carrinho()

def limpar_tela():
    os.system("cls || clear")

def menu():
    print("="*40)
    print(f"{'Senai':^40}")
    print("="*40)
    print("""
    1 - Adicionar dados
    2 - Fazer login 
    3 - Atualizar os dados  
    4 - Adicionar funcionario
    5 - Deletar Funcionario
    6 - Consultar Funcionario
    0 - Sair do sistema.     
    """)

def menu_2():
    print("="*40)
    print(f"{'Senai':^40}")
    print("="*40)
    print("""
    1 - Adicionar ao carrinho 
    2 - Consultar livro
    3 - Finalizar compra
    0 - Sair do sistema.     
    """)


def login():
    while True:
        matricula_cliente = int(input("Digite sua matricula: "))
        senha_cliente = input("Digte sua senha: ")
        cliente = session.query(Cliente).filter_by(matricula = matricula_cliente, senha = senha_cliente).first()
        if cliente:
            print(f"Login efetuado {cliente.nome}")
            while True:
                limpar_tela()
                menu_2()
                opcao2 = input("Resposta: ")
                match opcao2:
                    case "1":
                        adicionar_ao_carrinho()
                    case "2":
                        consultando_livros()           
                    case "3":
                        finalizar_compra()

                    case "0":
                        print("Sistema encerrado.")
                        return
                    case _:
                        print("Opção invalida.")
                        continue
        else:
            print("Login não encontrado.")
    



def cadastrando_usuario():

    inserir_matricula = int(input("Digite sua matrícula: "))
    if session.query(Cliente).filter_by(matricula=inserir_matricula).first():
        print("Matrícula já cadastrada.")
        return
    inserir_nome = input("Digite seu nome: ")
    inserir_email = input("Digite seu email: ")
    inserir_senha = input("Digite sua senha: ")

    cliente = Cliente(matricula=inserir_matricula, nome=inserir_nome, email=inserir_email, senha=inserir_senha)
    session.add(cliente)
    session.commit()
    print("Cliente adicionado com sucesso!")
    


def adicionando_funcionario():

    inserir_cpf = int(input("Digite seu cpf: "))
    if session.query(Funcionario).filter_by(cpf=inserir_cpf).first():
        print("CPF já cadastrado.")
        return

    inserir_nome = input("Digite seu nome: ")
    inserir_email = input("Digite seu email: ")
    inserir_senha = input("Digite sua senha: ")

    funcionario= Funcionario (cpf=inserir_cpf, nome=inserir_nome, email=inserir_email, senha=inserir_senha)
    session.add(funcionario)
    session.commit()
    print("Funcionário adicionado com sucesso!")
   

def deletando_funcionario():
    
    cpf_funcionario = int(input("Informe o cpf do funcionario: "))
    funcionario = session.query(Funcionario).filter_by(cpf=cpf_funcionario).first()

    if funcionario:
        session.delete(funcionario)
        session.commit()
        print("Funcionario deletado")
    else:
        print("Funcionario não encontrado")    


def atualizando_dados():
    matricula_cliente = int(input("Digite sua matricula: "))
    senha_cliente = input("Digite sua senha: ")
    cliente = session.query(Cliente).filter_by(matricula=matricula_cliente, senha=senha_cliente).first()
   
    if cliente:
        cliente.nome = input("Digite seu nome: ")
        cliente.email = input("Digite seu email: ")
        cliente.senha = input("Digite sua senha: ")

        session.commit()
        print("Usuário atualizado.")
    else:
        print("Usuário não encontrado")

def livros():
    livros = [
        {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "codigo": 1, "preco": 30},
        {"titulo": "O Alquimista", "autor": "Paulo Coelho", "codigo": 2, "preco": 45},
        {"titulo": "1984", "autor": "George Orwell", "codigo": 3, "preco": 25},
        {"titulo": "A Moreninha", "autor": "Joaquim Manuel de Macedo", "codigo": 4, "preco": 35},
        {"titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "codigo": 5, "preco": 40},
        {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "codigo": 6, "preco": 55},
    ]
    
    for livro in livros:
        if not session.query(Livros).filter_by(codigo=livro["codigo"]).first():
            novos_livros = Livros(titulo=livro["titulo"], autor=livro["autor"], codigo=livro["codigo"], preco=livro["preco"])
            session.add(novos_livros)
    session.commit()

def consultando_livros():
    livros = session.query(Livros).all()
    for livro in livros:
        print(f"Código: {livro.codigo}, Título: {livro.titulo}, Autor: {livro.autor}, Preço: R${livro.preco}")
    input("Pressione Enter para voltar ao menu...")

def adicionar_ao_carrinho():
    codigo_livro = int(input("Digite o código do livro que deseja adicionar ao carrinho: "))
    livro = session.query(Livros).filter_by(codigo=codigo_livro).first()

    if livro:
        carrinho.itens.append(livro)
        print(f"{livro.titulo} adicionado ao carrinho.")
    else:
        print("Livro não encontrado.")

def calcular_total():
    total = sum(livro.preco for livro in carrinho.itens)
    if len(carrinho.itens) >= 2:  # Aplica 20% de desconto se houver 2 ou mais livros
        total *= 0.8
    return total

def finalizar_compra():
    total = calcular_total()
    print(f"Total da compra: R${total:.2f}")
    carrinho.itens.clear()  # Limpa o carrinho após a compra
    print("Compra finalizada com sucesso!")
    time.sleep(10)

def lista_funcionarios():
    lista_funcionarios = session.query(Funcionario).all()
    if lista_funcionarios:
        for funcionario in lista_funcionarios:
            print(f"{funcionario.nome},{funcionario.email},{funcionario.cpf}")
    else:
        print("Nenhum funcionário cadastrado.")



# Inicializa os livros
livros()

while True:
    limpar_tela()
    menu()
    opcao = input("Resposta: ")
    match opcao:
        case "1":
            cadastrando_usuario()
        case "2":
            login()
        case "3":
            atualizando_dados()
        case "4":
            adicionando_funcionario()
        case "5":
            deletando_funcionario()
        case "6":
            print("Listando funcionários...")
            lista_funcionarios()    
        case "0":
            print("Saindo do sistema...")
            break
        case _:
            print("Opção inválida.")
            continue

