from models.categoria import Categoria
from sqlalchemy import select
from sqlalchemy.orm import Session


def incluir(motor):
    print("Incluindo categoria")
    nome = input("Qual o nome da categoria que você quer adicionar? ")
    with Session(motor) as sessao:
        categoria = Categoria()
        categoria.nome = nome
        sessao.add(categoria)
        sessao.commit()
    print(f"Categoria {nome} adicionada.")


def listar(motor):
    print("Categorias cadastradas")
    print(f"Nome                                      # Produtos")
    print(f"----------------------------------------- ----------")
    stmt = select(Categoria)
    stmt = stmt.order_by("nome")
    with Session(motor) as sessao:
        rset = sessao.execute(stmt).scalars()
        for categoria in rset:
            print(f"{categoria.nome:40s}  {len(categoria.lista_de_produtos):10d}")
    print(f"----------------------------------------- ----------")


def selecionar(motor):

    nome_parcial = input("Digite uma parte do nome da categoria desejada: ")
    stmt = select(Categoria).where(Categoria.nome.ilike(f"%{nome_parcial}%")).order_by("nome")
    with Session(motor) as sessao:
        rset = sessao.execute(stmt).scalars()
        contador = 1
        ids = list()
        for categoria in rset:
            print(f"{contador:3d} - {categoria.nome}")
            ids.append(categoria.id)
            contador = contador + 1
        cod = int(input("Digite o numero da categoria desejada: "))
        categoria = ids[cod - 1]
    return categoria

def alterar(motor):
    id_categoria = selecionar(motor)
    with Session(motor) as sessao:
        categoria = sessao.get(Categoria, id_categoria)
        print(f"Nome atual da categoria: {categoria.nome}")
        novo_nome = input("Qual vai ser o novo nome: ")
        categoria.nome = novo_nome
        sessao.commit()
    return


def remover(motor):
    id_categoria = selecionar(motor)
    with Session(motor) as sessao:
        categoria = sessao.get(Categoria, id_categoria)
        print(f"ATENCAO!  Ao remover a categoria '{categoria.nome}' você vai "
              f"remover, também, {len(categoria.lista_de_produtos)} produtos vinculados")
        for produto in categoria.lista_de_produtos:
            print(f"   - {produto.nome}")
        resposta = input("Remove mesmo assim (S/N)?")
        if resposta.upper() == "S":
            sessao.delete(categoria)
            sessao.commit()
        else:
            print("Mantendo a categoria no banco...")
    return
