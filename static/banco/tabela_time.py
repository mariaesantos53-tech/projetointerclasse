from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Time
from sqlalchemy import select

def select_todos():
    #  - busca todos os times no banco
    # 1 - montar o select
    times_sql = select(Time)
    # 2-executar o select
    times = db_session.execute(times_sql).scalars().all()
    return times
def salvar(nome,responsavel,turma):
    try:
        novo_times = Time(nome=nome, responsavel=responsavel, turma=turma)
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