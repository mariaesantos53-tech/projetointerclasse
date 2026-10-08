from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Time, Partida
from sqlalchemy import select, func


def select_todas_partidas():

    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)
    partidas_sql = (select(Partida,TimeCasa,TimeVisitante)
                    .join(TimeVisitante,Partida.time_visitante_id == TimeVisitante.id)
                    .join(TimeCasa,Partida.time_casa_id == TimeCasa.id)
    )


    partidas_casa = db_session.execute(partidas_sql).all()

    return partidas_casa

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_session.execute(partidas_sql).scalar()
    return qtd_total
print(select_quantidade_total())

def salvar():
    try:
        novo_times = Partida(nome=nome, responsavel=responsavel, turma=turma)
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


