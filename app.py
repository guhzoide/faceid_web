import os
import mysql.connector
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
data = str((datetime.now().strftime("%Y-%m-%d_%H_%M_%S")))

database = 'databae'
user = 'user'
host = 'host'
password = 'password'

#janelas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/camera')
def camera():
    return render_template ('camera.html')

@app.route('/identificacao')
def identificacao():
    return render_template ('identificacao.html')

@app.route('/tentativas')
def lista_tentativas():
    try:
        con = mysql.connector.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        cursor.execute("SELECT id, colaborador_nome, chapa, cpf, data, acesso_autorizado FROM acessos")
        data = cursor.fetchall()
        cursor.close()
        con.close()

        quantidade = len(data)
        nomes_arquivos_imagem = os.listdir('static/tentativas')
        dados_e_imagens = list(zip(data, nomes_arquivos_imagem))
        
        return render_template('lista_tentativas.html', dados_e_imagens=dados_e_imagens, quantidade=quantidade)
    except Exception as error:
        return str(error)

@app.route('/salvar', methods=['POST'])
def salvarCad():
    nome = request.form.get('nome')
    chapa = request.form.get('matricula')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    nivel = request.form.get('nivel')
    foto = 'N'

    if nome == '' or chapa == '' or cpf == '' or email == '':
        mensagem = 'Preencha todos os campos'

        return jsonify({'mensagem': mensagem})     

    nome = nome.upper()
    chars = "''()[],. "
    nome = nome.translate(str.maketrans('', '', chars))

    try:
        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute(f"select * from cadastros where cpf='{cpf}';")
        result = str(cursor.fetchall())
        chars = "''()[],"
        consulta = result.translate(str.maketrans('', '', chars))
        cursor.close()

        if consulta != '':
            mensagem = 'Já existe um cadastro com esse CPF'
            return jsonify({'mensagem': mensagem})

        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute('INSERT INTO cadastros (nome, chapa, email, cpf, nivel, foto) VALUES (%s,%s,%s,%s,%s,%s);', (nome, chapa, email, cpf, nivel, foto))
        con.commit()
        cursor.close()

        mensagem = 'Cadastro realizado com sucesso'
        return jsonify({'mensagem': mensagem})
    
    except Exception as error:
        mensagem = f"Erro ao realizar o cadastro: '{error}'"
        with open('log/log.dat', 'a') as file:
            file.write(f'{data} \n log de salvarCad\n {error} \n\n------------------------------------------------------------------------------\n\n')
        return jsonify({'mensagem': mensagem})   

@app.route('/excluir/<matricula>', methods=['DELETE'])
def excluir_cadastro(matricula):
    try:
        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute(f"select * from cadastros where chapa='{matricula}';")
        result = str(cursor.fetchall())
        chars = "''()[],"
        consulta = result.translate(str.maketrans('', '', chars))
        cursor.close()

        if consulta == '':
            return jsonify({'mensagem': f'Não existe cadastro com essa matricula - {matricula}'})
        
        else:
            con = mysql.connector.connect(host=host,database=database,user=user,password=password)
            cursor = con.cursor()
            cursor.execute(f"delete from cadastros where chapa='{matricula}';")
            cursor.close()

            try:
                os.remove(f'banco/{matricula}.png')
            except FileNotFoundError:
                return jsonify({'mensagem': 'Cadastro excluído com sucesso'})
        
        return jsonify({'mensagem': 'Cadastro excluído com sucesso'})
    except Exception as error:
        return jsonify({'mensagem': f'Erro ao excluir matricula{matricula}:{error}'})

@app.route('/salvarimg', methods=['POST'])
def salvarimg():
    matricula = request.form.get('matricula')
    uploaded_file = request.files['imagem']
    try:
        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute(f"select * from cadastros where chapa='{matricula}';")
        result = str(cursor.fetchall())
        chars = "''()[],"
        consulta = result.translate(str.maketrans('', '', chars))
        cursor.close()

        if consulta == '':
            mensagem = 'Essa matricula não existe em nosso sistema'
            return jsonify({'mensagem': mensagem})

        if uploaded_file:
            uploaded_file.save(f'banco/{matricula}.png')
            con = mysql.connector.connect(host=host,database=database,user=user,password=password)
            cursor = con.cursor()
            cursor.execute(f"update cadastros set foto='S' where chapa='{matricula}';")
            con.commit()
            cursor.close()
            mensagem = 'Imagem salva com sucesso'
            return jsonify({'mensagem': mensagem})
    
        mensagem = 'Erro ao salvar a imagem.'
        return jsonify({'mensagem': mensagem})
    
    except Exception as error:
        mensagem = f'Erro ao salvar a imagem: {error}'
        with open('log/log.dat', 'a') as file:
            file.write(f'{data} \n log de salvarimg\n {error} \n\n------------------------------------------------------------------------------\n\n')
        return jsonify({'mensagem': mensagem})   

@app.route('/identificar', methods=['POST'])
def identificar():
    data = str((datetime.now().strftime("%Y-%m-%d_%H_%M_%S")))
    matricula = request.form.get('matricula')
    uploaded_file = request.files['imagem']
    uploaded_file.save(f'static/tentativas/{data}_{matricula}.png')

    with open('banco/nomes.dat', 'w') as file:
        file.write(f'{data}_{matricula}.png')

    with open('banco/matricula.dat', 'w') as file:
        file.write(f'{matricula}.png')

    try:
        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute(f"select * from cadastros where chapa='{matricula}';")
        result = str(cursor.fetchall())
        chars = "''()[],"
        consulta = result.translate(str.maketrans('', '', chars))
        cursor.close()

        if consulta == '':
            con = mysql.connector.connect(host=host,database=database,user=user,password=password)
            cursor = con.cursor()
            cursor.execute(f"select nivel, nome, cpf, foto from cadastros where chapa='{matricula}';")
            consulta = cursor.fetchone()
            nivel = consulta[0]
            nome = consulta[1]
            cpf = consulta[2]
            foto = consulta[3]
            cursor.close()
            mensagem = 'Essa matricula não existe em nosso sistema'
            return jsonify({'mensagem': mensagem})

        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute(f"select nivel, nome, cpf, foto from cadastros where chapa='{matricula}';")
        consulta = cursor.fetchone()
        nivel = consulta[0]
        nome = consulta[1]
        cpf = consulta[2]
        foto = consulta[3]
        cursor.close()

        with open('banco/nivel.dat', 'r') as file:
            for line in file:
                pass
            last_nivel = line        

        if nivel <= last_nivel or foto == 'N':
            result = False
            con = mysql.connector.connect(host=host,database=database,user=user,password=password)
            cursor = con.cursor()
            cursor.execute('INSERT INTO acessos (colaborador_nome, chapa, cpf, data, acesso_autorizado) VALUES (%s,%s,%s,%s,%s);', (nome, matricula, cpf, data, result))
            con.commit()
            cursor.close()
            if foto == 'N':
                return jsonify({'mensagem': 'Não possui foto cadastrada'})
            
            return jsonify({'mensagem': 'Nível de acesso não autorizado'})
        
        os.system('python identificacao.py')
        
    except Exception as error:
        return error

    with open('banco/result.dat', 'r') as file:
        for line in file:
            pass
        last_result = line

    os.remove('banco/result.dat')

    if last_result == 'True':
        result = True
        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute('INSERT INTO acessos (colaborador_nome, chapa, cpf, data, acesso_autorizado) VALUES (%s,%s,%s,%s,%s);', (nome, matricula, cpf, data, result))
        con.commit()
        cursor.close()
        return jsonify({'mensagem': 'Acesso autorizado'})
    else:
        result = False
        con = mysql.connector.connect(host=host,database=database,user=user,password=password)
        cursor = con.cursor()
        cursor.execute('INSERT INTO acessos (colaborador_nome, chapa, cpf, data, acesso_autorizado) VALUES (%s,%s,%s,%s,%s);', (nome, matricula, cpf, data, result))
        con.commit()
        cursor.close()
        return jsonify({'mensagem': 'Acesso negado'})

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
