import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

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

def menu():
    print("="*40)
    print(f"{'Senai':^40}")
    print("="*40)
    print("""
    1 - Adicionar dados
    2 - Consultar livros
    3 - Atualizar os dados 
    4 - Adicionar ao carrinho 
    5 - Finalizar compra
    0 - Sair do sistema.     
    """)

def solicitando_dados():
    inserir_matricula = int(input("Digite sua matricula: "))
    inserir_nome = input("Digite seu nome: ")
    inserir_email = input("Digite seu email: ")
    inserir_senha = input("Digite sua senha: ")

    cliente = Cliente(matricula=inserir_matricula, nome=inserir_nome, email=inserir_email, senha=inserir_senha)
    session.add(cliente)
    session.commit()
    print("Cliente adicionado com sucesso!")
    limpar_tela()

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

def adicionar_livros_iniciais():
    livros_iniciais = [
        {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "codigo": 1, "preco": 30},
        {"titulo": "O Alquimista", "autor": "Paulo Coelho", "codigo": 2, "preco": 45},
        {"titulo": "1984", "autor": "George Orwell", "codigo": 3, "preco": 25},
        {"titulo": "A Moreninha", "autor": "Joaquim Manuel de Macedo", "codigo": 4, "preco": 35},
        {"titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "codigo": 5, "preco": 40},
        {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "codigo": 6, "preco": 55},
        {"titulo": "A Revolução dos Bichos", "autor": "George Orwell", "codigo": 7, "preco": 20},
        {"titulo": "Cem Anos de Solidão", "autor": "Gabriel García Márquez", "codigo": 8, "preco": 50},
        {"titulo": "Orgulho e Preconceito", "autor": "Jane Austen", "codigo": 9, "preco": 30},
        {"titulo": "A Metamorfose", "autor": "Franz Kafka", "codigo": 10, "preco": 25},
    ]
    
    for livro in livros_iniciais:
        novo_livro = Livros(titulo=livro["titulo"], autor=livro["autor"], codigo=livro["codigo"], preco=livro["preco"])
        session.add(novo_livro)

    session.commit()
    print("Livros iniciais adicionados com sucesso!")

def consultando_livros():
    livros = session.query(Livros).all()
    for livro in livros:
        print(f"Código: {livro.codigo}, Título: {livro.titulo}, Autor: {livro.autor}, Preço: R${livro.preco}")
    input("Pressione Enter para continuar...")

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

def limpar_tela():
    os.system("cls || clear")

# Inicializa os livros
adicionar_livros_iniciais()

while True:
    menu()
    opcao = input("Resposta: ")
    match opcao:
        case "1":
            solicitando_dados()
        case "2":
            consultando_livros()
        case "3":
            atualizando_dados()
        case "4":
            adicionar_ao_carrinho()
        case "5":
            finalizar_compra()
        case "0":
            print("Saindo do sistema...")
            break
        case _:
            print("Opção inválida.")
            continue
