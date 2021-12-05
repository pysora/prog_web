import locale
import bd
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def menu():
   return render_template('menu.html')

@app.route('/formIncluir')
def formIncluir():
   return render_template('formIncluir.html')

@app.route('/incluir', methods=['POST'])
def incluir():

   nome = request.form['nome']
   data = request.form['data']
   linguagens = request.form['linguagens']
   instituicao = request.form['instituicao']
   curso = request.form['curso']
   semestre = int(request.form['semestre'])
   celular = request.form['celular']
   email = request.form['email']

   mysql = bd.SQL("root", "", "test")
   comando = "INSERT INTO curriculo(nome, dta_nasc, ling_prog, inst_ensino, curso, semestre, celular, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
   if mysql.executar(comando, [nome, data, linguagens, semestre, instituicao, curso, celular, email]):
       msg=f"Currículo de {nome} cadastrado com sucesso!"
   else:
       msg="Falha na inclusão de curriculo."

   return render_template('incluir.html', msg=msg)

@app.route('/parConsultar')
def parConsultar():

   mysql = bd.SQL("root", "", "test")

   comando = "SELECT nome from curriculo;"
   cs = mysql.consultar(comando, ())

   sel = "<SELECT NAME='curriculo'>"
   sel += "<OPTION>Todos</OPTION>"
   for [curriculo] in cs:
       sel += "<OPTION>" + curriculo + "</OPTION>"
   sel += "</SELECT>"
   cs.close()

   return render_template('parConsultar.html', curriculo=sel)

@app.route('/consultar', methods=['POST'])
def consultar():
   nome = request.form['curriculo']

   mysql = bd.SQL("root", "", "test")
   comando = "SELECT * from curriculo where nome=%s;"

   locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

   cs = mysql.consultar(comando, [nome, ])
   curriculos = ""
   for [nome, dta_nasc, ling_prog, inst_ensino, curso, semestre, celular, email] in cs:
       curriculos += "<TR>"
       curriculos += "<TD>" + nome + "</TD>"
       curriculos += "<TD>" + ling_prog + "</TD>"
       curriculos += "<TD>" + inst_ensino + "</TD>"
       curriculos += "<TD>" + curso + "</TD>"
       curriculos += "<TD>" + str(dta_nasc) + "</TD>"
       curriculos += "<TD>" + str(semestre) + "</TD>"
       curriculos += "<TD>" + celular + "</TD>"
       curriculos += "<TD>" + email + "</TD>"
       curriculos += "</TR>"
   cs.close()

   return render_template('consultar.html', curriculos=curriculos)

@app.route('/parAlterar')
def parAlterar():
   return render_template('parAlterar.html')

@app.route('/formAlterar', methods=['POST'])
def formAlterar():

   nome = request.form['nome']


   mysql = bd.SQL("root", "", "test")
   comando = "SELECT * FROM curriculo WHERE nome=%s;"

   cs = mysql.consultar(comando, [nome])
   dados = cs.fetchone()
   cs.close()

   if dados == None:
      return render_template('naoEncontrado.html')
   else:
      return render_template('formAlterar.html', nome=dados[0], dta_nasc=dados[1], ling_prog=dados[2], inst_ensino=dados[3],
                             curso=dados[4], semestre=dados[5], celular=dados[6], email=[7])


@app.route('/alterar', methods=['POST'])
def alterar():

   idt_curriculo = int(request.form['idt_curriculo'])
   nome = request.form['nome']
   dta_nasc = request.form['dta']
   ling_prog = request.form['ling']
   inst_ensino = request.form['inst']
   curso = request.form['curso']
   semestre = int(request.form['sem'])
   celular = request.form['cel']
   email = request.form['email']


   mysql = bd.SQL("root", "", "test")
   comando = "UPDATE curriculo SET nome=%s, dta_nasc=%s, ling_prog=%s, inst_ensino=%s, curso=%s, semestre=%s, celular=%s, email=%s WHERE idt_curriculo=%s;"

   if mysql.executar(comando, [nome, dta_nasc, ling_prog, inst_ensino, curso, semestre, celular, email]):
      msg = "Curriculo de " + nome + " alterado com sucesso!"
   else:
      msg = "Falha na alteração de curriculo."

   return render_template('alterar.html', msg=msg)

@app.route('/parExcluir')
def parExcluir():
   mysql = bd.SQL("root", "", "test")
   comando = "SELECT idt_curriculo, nome, curso FROM curriculo ORDER BY nome;"

   cs = mysql.consultar(comando, ())
   curriculos = ""
   for [idt, nme, curso] in cs:
       curriculos += "<TR>"
       curriculos += "<TD>" + nme + "</TD>"
       curriculos += "<TD>" + curso + "</TD>"
       curriculos += "<TD><BUTTON ONCLICK=\"jsExcluir('" + nme + " (" + curso + ")" + "', " + str(idt) + ")\">Excluir" + "</BUTTON></TD>"
       curriculos += "</TR>"
   cs.close()

   return render_template('parExcluir.html', curriculos=curriculos)

@app.route('/excluir', methods=['POST'])
def excluir():
   idt = int(request.form['idt'])

   mysql = bd.SQL("root", "", "test")
   comando = "DELETE FROM curriculo WHERE idt_curriculo=%s;"

   if mysql.executar(comando, [idt]):
       msg="Currículo excluído com sucesso!"
   else:
       msg="Falha na exclusão de currículo."

   return render_template('excluir.html', msg=msg)

app.run()