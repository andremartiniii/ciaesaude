#################################################################################################
############################################ IMPORTS ############################################
#################################################################################################
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt

###################################################################################################
############################################ FLASK APP ############################################
###################################################################################################
app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

##################################################################################################
############################################ DATABASE ############################################
##################################################################################################
bd_user = "gpelai"
bd_password = "4e129757"
client = MongoClient(f'mongodb+srv://{bd_user}:{bd_password}@cluster0.v1wbgmq.mongodb.net/?retryWrites=true&w=majority')
db = client.clinica
users_collection = db.login_system

################################################################################################
############################################ ROUTES ############################################
################################################################################################

# Rota inicial
@app.route('/')
def index():
    return render_template('landing_page.html')

######################################
############## REGISTER ##############
######################################

# Registro Page OKOKOKOK
@app.route('/register')
def register_page():
    return render_template("register_page.html")

# Rota de registro OKOKOKOK
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Verificar se o usuário já existe
    if users_collection.find_one({'username': username}):
        return render_template('index.html', message='Nome de usuário já está em uso!')

    # Criptografar a senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Inserir o novo usuário no banco de dados
    users_collection.insert_one({'username': username, 'password': hashed_password})

    return render_template('index.html', message='Registro realizado com sucesso!')

###################################
############## LOGIN ##############
###################################

# Home
@app.route('/home')
def home():
    return render_template('home.html')

# Login Page OKOKOKOK
@app.route('/login')
def login_page():
    return render_template('login_page.html')

# Rota de login OKOKOKOK
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Buscar o usuário no banco de dados
    user = users_collection.find_one({'username': username})

    # Verificar se o usuário existe e a senha está correta
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        return redirect('/home')
    else:
        return render_template('login_page.html')

####################################
############## LOGOUT ##############
####################################

# Rota de logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return render_template('landing_page.html', message='Logout realizado com sucesso!')

###################################
############## ROTAS ##############
###################################

@app.route('/colaborador-novo')
def novo_colaborador():
    return render_template('novos_colaboradores.html')

@app.route('/usuario-novo')
def novo_usuario():
    return render_template('novos_usuarios.html')

@app.route('/paciente-novo')
def paciente_novo():
    return render_template('paciente_novo.html')

@app.route('/paciente-consulta')
def paciente_consulta():
    return render_template('paciente_consulta.html')

#################################
############## RUN ##############
#################################

if __name__ == '__main__':
    app.run(debug=True)