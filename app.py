from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import *
from static.banco import tabela_time, tabela_jogador, tabela_partida

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times = tabela_time.select_quantidade_total()

    jogadores = tabela_jogador.select_quantidade_total()

    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores= jogadores,
        total_times= times,
        total_partidas= partidas,

    )


@app.route("/jogadores")
def listar_jogadores():

    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos_jogadores()
    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    # quando clicar no botão cadastrar ele entra no if
    if request.method == "POST":
        # pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        numero_camisa = request.form.get("numero_camisa") or None
        # 2- verificar se foi digitado
        if not nome:
            flash('Preencha o nome', 'erro')
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash('Preencha o posicao do jogador', 'erro')
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash('Preencha o numero_camisa', 'erro')
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash('Preencha o time', 'erro')

        #     3 - salvar no banco
        tabela_jogador.salvar_jogadores(nome=nome,numero_camisa=numero_camisa,posicao=posicao,time_id= time_id)


    #     select times para escolher no formulario

    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos_jogadores()

    return render_template("jogadores.html", times=times, jogadores=jogadores)


@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # pegar os valores do form
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        turma = request.form.get("turma", "").strip()


        # verificar se foi digitado
        if not nome:
            flash("Preencha o nome", "error")
            return redirect(url_for("novo_time"))

        if not responsavel:
            flash("Preencha com o responsável", "error")
            return redirect(url_for("novo_time"))


        if not turma:
            flash("Preencha com a turma", "error")
            return redirect(url_for("novo_time"))

        tabela_time.salvar(nome = nome, responsavel = responsavel, turma = turma)

    times = tabela_time.select_todos()
    print(times)
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():

    partidas = tabela_partida.select_todas_partidas()
    return render_template("partidas.html", partidas=partidas)



@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        if not time_casa_id:
            flash('Preencha o nome do time casa', 'erro')
            return redirect(url_for('nova_partida'))
        if not time_visitante_id:
            flash('selecine um time diferente', 'erro')
            return redirect(url_for('nova_partida'))
        if not gols_casa:
            flash('Preencha o nome do placar casa', 'erro')
            return redirect(url_for('nova_partida'))
        if not gols_visitante:
            flash('preencha o nome do placar visitante, erro.')

        # verificar se os times são iguais
        if time_casa_id == time_visitante_id:
            flash('selecione times diferentes', 'error')

        try:
            partidanova = Partida( time_casa_id= int(time_casa_id), time_visitante_id=int(time_visitante_id),gols_casa=gols_casa, gols_visitante=gols_visitante,data_partida=data_partida)
            db_session.add(partidanova)
            db_session.commit()
            flash("Partida adicionada com sucesso", "success")

        except SQLAlchemyError as e:
            db_session.rollback()
            print(e)
            flash('erro ao adicionar partida', 'error')

        except exception as e:
            db_session.rollback()
            flash('erro insperado', 'error')
    times = tabela_time.select_todos()
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).all()

    return render_template('partidas.html', partidas=partidas, times=times)




if __name__ == "__main__":
    app.run(debug=True)
