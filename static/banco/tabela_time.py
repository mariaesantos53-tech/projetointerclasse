import time
from os import times

from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Time, Jogador
from sqlalchemy import select, func, outerjoin


def select_todos():
    #  - busca todos os times no banco
    # 1 - montar o select
    times_sql = (
        select(Time, func.count(Jogador.id).label("jogadores'"))
        .outerjoin(Jogador,Jogador.time_id == Time.id)
        .group_by(Time.id)
    )



    # 2-executar o select
    times = db_session.execute(times_sql).all()
    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    qtd_total = db_session.execute(times_sql).scalar()
    return qtd_total

print(select_quantidade_total())



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