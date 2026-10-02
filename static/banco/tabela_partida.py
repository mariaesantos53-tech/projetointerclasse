from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Time, Partida
from sqlalchemy import select

def select_todas_partida():
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return partidas

def salvar():
    try:
        novo_times = partida(nome=nome, responsavel=responsavel, turma=turma)
        db_session.add(novo_times)
        db_session.commit()
        flash("Times adicionado com sucesso", "success")

    except SQLAlchemyError as e:
        db_session.rollback()
        flash("ocorreu um erro ao adicionar time", "error")
        print(f"erro: {e}")

    except Exception as e:
        db_session.rollback()
        flash("ocorreu um erro ao adicionar time", "error")
        print(f"erro: {e}")
