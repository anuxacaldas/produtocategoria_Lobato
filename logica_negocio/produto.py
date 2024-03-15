from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Produto
from logica_negocio import categoria

def incluir(motor):
    print("Incluir novo produto")
    nome = input("Qual o nome do produto? ")
    preco = float(input("Qual o preço do produto? "))
    estoque = int(input("Qual o estoque inicial do produto? "))
    cat_id = categoria.selecionar(motor)


    with Session(motor) as sessao:
        produto = Produto()
        produto.nome = nome
        produto.preco = preco
        produto.estoque = estoque
        produto.ativo = True
        produto.categoria_id = cat_id
        sessao.add(produto)
        sessao.commit()
        print(f"O Produto {nome} foi adicionado")


def selecionar(motor):
    """
    Retorna o id de um produto selecionado
    :param motor: motor de acesso ao banco
    :return: wid com o id do produto
    """

    nome_parcial = input("Digite uma parte do nome do produto desejado: ")
    stmt = select(Produto).where(Produto.nome.ilike(f"%{nome_parcial}%")).order_by("nome")
    with Session(motor) as sessao:
        rset = sessao.execute(stmt).scalars()
        contador = 1
        ids = list()
        for produto in rset:
            print(f"{contador:3d} - {produto.nome}")
            ids.append(produto.id)
            contador = contador + 1
        cod = int(input("Digite o numero da categoria desejada: "))
        produto = ids[cod - 1]
    return produto


def alterar(motor):
    id_produto = selecionar(motor)
    with Session(motor) as sessao:
        produto = sessao.get(Produto, id_produto)
        print(f"Deixe em branco as respostas abaixo para manter os valores atuais")
        novo_nome = input(f"Qual vai ser o novo nome: ({produto.nome})? ")
        novo_preco = float(input(f"Qual o novo preco: ({produto.preco:.2f})? "))
        situacao_hoje = "Ativo" if produto.ativo else "Inativo"
        novo_ativo = input(f"Muda o status do produto ({situacao_hoje}) (S/N)? ")
        if novo_nome != "":
            produto.nome = novo_nome
        if novo_preco != 0:
            produto.preco = float(novo_preco)
        if novo_ativo[0].lower() == "s":
            produto.ativo = not produto.ativo
        sessao.commit()
        print("Produto alterado")

