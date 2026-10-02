from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session


def select_todos_jogadores():
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores


def salvar_jogadores():
    try:
        novo_jogador = Jogador(nome=nome, posicao=posicao, numero_camisa=int(numero_camisa), time_id=int(time_id))
        db_session.add(novo_jogador)
        db_session.commit()
        flash('jogador adicinado com sucesso', 'success')

    except SQLAlchemyError as e:
        db_session.rollback()
        print('erro inesperado: {e}')
        flash('erro inesperado', 'error')