from sqlalchemy import create_engine

import seed_func
from logica_negocio import categoria
from logica_negocio import produto

"""
alembic init migrations
Editar o alembic.ini com a string de conexao do banco
Editar o migrations/env.py linha 18 e 19 para
    from models import base
    target_metadata = base.Base.metadata
alembic revision --autogenerate -m "Migracao inicial"
alembic upgrade head
"""

if __name__ == "__main__":
    motor = create_engine("sqlite+pysqlite:///banco_de_dados.sqlite", echo=False)

    seed_func.seed_database(motor)
    while True:
        print("Menu de opcoes")
        print(" 1. Incluir categoria")
        print(" 2. Listar categorias")
        print(" 3. Alterar categoria")
        print(" 4. Remover categoria")
        print(" 5. Incluir produto")
        print(" 6. Listar produtos")
        print(" 7. Alterar produto")
        print(" 8. Remover produto")
        print(" 9. Comprar produto")
        print("10. Vender produto")
        print("11. Listar produtos sem estoque")

        print("0. Sair")
        opcao = int(input("Qual opcao? "))
        if opcao == 1:
            categoria.incluir(motor)
        elif opcao == 2:
            categoria.listar(motor)
        elif opcao == 3:
            categoria.alterar(motor)
        elif opcao == 4:
            categoria.remover(motor)
        elif opcao == 5:
            produto.incluir(motor)
        elif opcao == 6:
            pass
        elif opcao == 7:
            produto.alterar(motor)
        elif opcao == 8:
            pass
        elif opcao == 0:
            exit(0)
        else:
            print("Opcao invalida...")
