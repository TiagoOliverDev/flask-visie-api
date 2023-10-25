from flask import Flask, jsonify, request
from flask_cors import CORS
import MySQLdb
from aux import Aux
from decouple import config


DEBUG = True
 

app = Flask(__name__)
app.config.from_object(__name__)
     
   
DB_USER = config('DB_USER', default='tiagooliveira')
DB_PASSWORD = config('DB_PASSWORD', default='dGlhZ29vbGl2')
DB_HOST = config('DB_HOST', default='jobs.visie.com.br')
DB_PORT = config('DB_PORT', default=3306, cast=int)
DB_DATABASE = config('DB_DATABASE', default='tiagooliveira')

db_config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT,
    'database': DB_DATABASE,
}
 
# CORS
CORS(app, resources={r'/*': {'origins': '*'}})
 
 
@app.route('/')
def home():
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * from pessoas order by id_pessoa")
        peopleLists = cursor.fetchall()

        result = []
        for peopleList in peopleLists:
            pessoa_dict = {
                'id': peopleList[0],
                'nome': peopleList[1],
                'rg': peopleList[2],
                'cpf': peopleList[3],
                'data_nascimento': peopleList[4],
                'data_admissao': peopleList[5],
                'funcao': peopleList[6],
            }
            result.append(pessoa_dict)


        return jsonify({
            'status': 'success',
            'peoples': result
        })
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
 
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        nome = post_data.get('nome')
        rg = post_data.get('rg')
        cpf = post_data.get('cpf')
        data_nascimento = post_data.get('data_nascimento')
        data_admissao = post_data.get('data_admissao')
        funcao = post_data.get('funcao')

        data_nascimento_formatada = Aux.formatar_data(data_nascimento)
        data_admissao_formatada = Aux.formatar_data(data_admissao)

        sql = f"INSERT INTO pessoas(nome,rg,cpf,data_nascimento,data_admissao,funcao) VALUES(%s, %s, %s, %s, %s, %s)"
        data = (nome, rg, cpf, data_nascimento_formatada, data_admissao_formatada, funcao)

        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(sql, data)
        conn.commit()
 
        response_object['message'] = "Successfully Added"
    return jsonify(response_object)
 
@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas WHERE id_pessoa = %s", [id])
    row = cursor.fetchone() 
    
    return jsonify({
        'status': 'success',
        'editpeople': row
    })

@app.route('/all_data_by_id/<string:id>', methods=['GET', 'POST'])
def all_data_by_id(id):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas WHERE id_pessoa = %s", [id])
    row = cursor.fetchone() 
    
    return jsonify({
        'status': 'success',
        'editpeople': row
    })
 
@app.route('/update', methods=['GET', 'POST'])
def update():    
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        edit_id = post_data.get('edit_id')
        edit_nome = post_data.get('edit_nome')
        edit_rg = post_data.get('edit_rg')
        edit_cpf = post_data.get('edit_cpf')
        edit_data_nascimento = post_data.get('edit_data_nascimento')
        edit_data_admissao = post_data.get('edit_data_admissao')
        edit_funcao = post_data.get('edit_funcao')

        data_nascimento_formatada = Aux.formatar_data(edit_data_nascimento)
        data_admissao_formatada = Aux.formatar_data(edit_data_admissao)

        cursor.execute (f"UPDATE pessoas SET nome=%s, rg=%s, cpf=%s, data_nascimento=%s, data_admissao=%s, funcao=%s WHERE id_pessoa={edit_id}",(edit_nome, edit_rg, edit_cpf, data_nascimento_formatada, data_admissao_formatada, edit_funcao))
        conn.commit()
        cursor.close()
 
        response_object['message'] = "Successfully Updated"
    return jsonify(response_object)
 
@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
   
    response_object = {'status': 'success'}
 
    cursor.execute("DELETE FROM pessoas WHERE id_pessoa = %s", [id])
    conn.commit()
    cursor.close()
    response_object['message'] = "Successfully Deleted"
    return jsonify(response_object)
 
if __name__ == '__main__':
    app.run()