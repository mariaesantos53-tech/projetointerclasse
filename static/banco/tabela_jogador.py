from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session, Time


def select_todos_jogadores():
    # 1- montar o select
    # join(tabela que eu quero juntar,condição= chave estrangeira = chave primaria)
    jogadores_sql = select(Jogador,Time).join(Time,Jogador.time_id== Time.id)

    # 2- executar o select
    # scalars só usa quando tem uma tabela,se não usa all
    jogadores = db_session.execute(jogadores_sql).all()
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    quantidade_total = db_session.execute(jogadores_sql).scalar()
    return quantidade_total
print(select_quantidade_total())

def salvar_jogadores(nome,posicao,numero_camisa,time_id):
    try:
        novo_jogador = Jogador(nome=nome, posicao=posicao, numero_camisa=int(numero_camisa), time_id=int(time_id))
        db_session.add(novo_jogador)
        db_session.commit()
        flash('jogador adicinado com sucesso', 'success')

    except SQLAlchemyError as e:
        db_session.rollback()
        print('erro inesperado: {e}')
        flash('erro inesperado', 'error')

