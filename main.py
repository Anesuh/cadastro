'''
    Programa criado na versão 3.11.2 do Python.
    Data a ultima atualização: 26/03/2023
    Versão: 1.2
'''

#Importa o metódo de geração de números aleátorios em um determinado intervalo.
from random import randint

#Importa o metódo sleep para dar pausas no programa.
from time import sleep

#Importa a biblioteca para se conectar ao banco de dados
import psycopg2, psycopg2.errors

from getpass import getpass

#Lista com caracteres especiais e senhas comuns
caracteres_especiais = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '`', '~', '|', '{', '}', '[', ']', ';', ':', '"', "'", '<', '>', '?', '/','.']

comuns_senhas = ['1234', 'senha', '123456', 'password', '123456789', '12345678', '12345', '111111', '1234567', 'sunshine',
'qwerty', 'letmein', 'monkey', 'dragon', 'baseball', 'football', 'superman', 'batman',
'trustno1', 'iloveyou', 'welcome', 'admin', 'hello', 'password1', '123123', 'shadow',
'monkey1', 'letmein1', 'mustang', 'shadow1', 'football1', 'qwerty1']

#Função para validar senhas
def password_validation(senha):
    validation = 0
    #Lista que guarda as vulnerabilidades
    vulnerabilidades = []

    #Verifica se a senha é maior que 8 caracteres
    if len(senha) <= 8:
        vulnerabilidades.append('Sua senha deve ter mais que 8 caracteres.')

    #Verifica se a senha contem caracteres especiais
    validation = 0
    for i in range(30):
        if caracteres_especiais[i] in senha:
            validation = 1
            break
    if validation == 0:
        vulnerabilidades.append('Sua senha deve conter caracteres especiais.')

    #Verifica se a senha contem sequencias de caracteres comuns
    for i in range(len(comuns_senhas)):
        if comuns_senhas[i] in senha or comuns_senhas[i].lower() in senha or comuns_senhas[i].upper() in senha:
            vulnerabilidades.append('Sua senha contem elementos frequentimente usados.')
            break

    #Verifica se contem números e letras na senha
    if senha.isalnum() == True:
        vulnerabilidades.append('Sua senha deve conter números e letras.')

    #Verifica se a senha contem caracteres minúsculos e maiúsculos
    if senha.lower() == senha or senha.upper() == senha:
        vulnerabilidades.append('Sua senha deve misturar letras minúsculas e maiúsuclas.')

    #Caso não tenha vulnerabilidades, diz que a senha é segura
    if len(vulnerabilidades) == 0:
        return 1

    #Trás possiveis vulnerabilidades
    else:
        for i in range(len(vulnerabilidades)):
            print(f'\033[31;1m{vulnerabilidades[i]}\033[0m')

#Função para cadastrar o usuário.
def cadastro(name, lastname):

    #Cria um username e um ID aleátorio e não existente para o usuário
    username = name.lower().strip()+'_@'+lastname.lower().title().strip()+str(len(name))
    id = randint(1000, 9999)
    while id in ids:
        id = randint(1000,9999)
    if len(username) <= 80:
        #Trata excessões caso o usuário ou o ID já esteja no banco de dados
        while True:
            try:
                #Insere o usuário no banco de dados
                add_query = f"""INSERT INTO usuario (nome, id) VALUES ('{username}', {id})"""
                cursor.execute(add_query)
                conn.commit()

                #Insere o usuário em uma lista de usuários.
                users.append((username, id))
                ids.append(id)

                #Mostra o ID do usuário.
                print(f'\033[32;1mUsuário cadastrado com sucesso. O código é \033[0m\033[34;1m{id}\033[0m')
                break

            #Caso o id já esteja no banco de dados, cria outro id
            except psycopg2.errors.UniqueViolation as erro:
                id = randint(1000,9999)

            #Exibe uma mensagem de erro caso o nome de usuário ja esteja no sistema
            except psycopg2.errors.InFailedSqlTransaction as erro:
                print(f'\033[31;1mERRO! Esse nome de usuário já está cadastrado no sistema. Por favor, tente novamente.\033[0m {erro}')
                cursor.execute("ROLLBACK")
                break

    #Exibe uma mensagem de erro caso o nome de usuário seja maior que 80 caracteres
    else:
        print('\033[31;1mERRO! O nome de usuário ficou grande demais.')

def adm_cadastro(username, password):
    senha = password_validation(password)
    if senha == 1:
        senha = password
        if len(username) <= 80:
            admin = (username, password)
            adm.append(admin)
        else:
            print('\033[31;1mO nome de usuário é grande demais.\033[0m')

#Função para remover um usuário.
def remover_usuario(id):
    confirmacao = 0

    #Para cada usuário em users, me dê o índice (i) e o usuário (user)
    for i, user in enumerate(users):

        #Se o ID do usuário for igual ao passado, remove o usuário do sistema.
        if user[1] == id:
            users.pop(i)
            print(f'\033[32;1mUsuário {user[0]} removido com sucesso!\033[0m')

            #Remove o usuário do banco de dados
            delete_query = f'''DELETE FROM usuario WHERE id = {id}'''
            cursor.execute(delete_query)
            conn.commit()
            confirmacao = 1

    #Exibe uma mensagem de erro caso o usuário não exista no sistema.
    if confirmacao != 1:
        print('\033[31;1mNão foi possivel encontrar o usuário no sistema\033[0m')

#Função para mostrar um determinado usuário.
def buscar_usuario(id):
    confirmacao = 0

    #Para cada usuário em users:
    for user in users:

        #Se o ID do usuário for igual ao passado, mostra o nome de usuário correspondente.
        if user[1] == id:
            confirmacao = 1
            user2 = user[0]
            user2 = user2.replace("'",'')
            print(f'\033[32;1mO usuário correspondente ao id\033[0m \033[34;1m{id}\033[32;1m é \033[0m\033[34;1m{user2}\033[0m')

        #Exibe uma mensagem de erro caso o usuário não exista no sistema.
    if confirmacao != 1:
        print('\033[31;1mNão foi possivel encontrar o usuário no sistema\033[0m')

#Função para sair do programa.
def sair():

    #Pede a confirmação do usuário.
    choice = input('Você tem certeza que deseja encerrar o programa? [Y/N]\n').lower().strip()
    if choice == 'y':

        #Fecha o programa e te desconecta do banco de dados.
        cursor.close()
        conn.close()
        print(f'\033[31;1mVocê foi desconectado de {database}')
        sleep(0.5)
        print('Fechando programa, aguarde...\033[0m')
        sleep(3)
        exit()
    elif choice == 'n':
        return 0
    else:
        print('\033[31;1mERRO! Opção inválida\033[0m')

#Função para mostrar todos os usuários.
def mostrar_todos(choice):

    #Verifica se existem usuários.
    if choice == 1:
        if len(users) == 0:
            print('\033[31;1mVocê não tem usuários cadastrados.\033[0')
        else:
            #Mostra todos os usuários em ordem de cadastro.
            print('\033[32;1mAqui estão todos os usuarios em ordem de cadastro!\033[0m')
            linha(30)
            for user in users:

                #Retira as aspas do nome de usuário.
                user2 = user[0]
                user2 = user2.replace("'",'')
                print(f'Usuário: \033[34;1m{user[0]}\033[0m | ID: \033[34;1m{user[1]}\033[0m')
            linha(30)
    #Mostra os usuários em ordem alfabética
    elif choice == 2:
        print('Aqui estão todos os usuários em ordem alfabética')
        user_alfa = sorted(users, key=lambda users: users[0])
        for user in user_alfa:
            print(f'Usuário: \033[34;1m{user[0]}\033[0m | ID: \033[34;1m{user[1]}\033[0m')

    #Mostra os usuários em ordem de ID (Crescente)
    elif choice == 3:
            user_num = sorted(users, key=lambda users: users[1])
            print('Aqui estão todos os usuários em ordem de ID (Crescente)')
            for user in user_num:
                print(f'Usuário: \033[34;1m{user[0]}\033[0m | ID: \033[34;1m{user[1]}\033[0m')
#Função para criar linhas de separação.
def linha(qnt):
    print('\033[33;1m\n'+'='*qnt+'\n\033[0m')

#Função para mostrar o menu.
def menu():
    return '''\033[35;1m[1] Cadastrar usuário
[2] Remover usuário
[3] Limpar lista de usuários
[4] Buscar usuário
[5] Mostrar todos os usuários
[6] Sair do programa
[7] Mostrar menu\033[0m
'''

#Pede uma escolha do banco de dados para o usuário
escolha2 = input('\033[34;1mAntes de tudo, por favor insira essas informações\nVocê deseja usar o banco de dados padrão ou inserir um novo?\033[0m\n\033[33;1m[1] Novo\n[2] Padrão\n\033[0m')

if escolha2 == '1':
    database = input('Banco de dados: ')
    password = input('Senha: ')

else:
    database = 'cadastro'
    password = '5511'

try:
    conn = psycopg2.connect(host='localhost', database=f'{database}', user='postgres', password=f'{password}')
    cursor = conn.cursor()
    print(f'\033[32;1mVocê se conectou a {database}\033[0m')

except (UnboundLocalError, psycopg2.OperationalError) as e:
    print(f'\033[31;1mNão foi possivel se conectar ao banco de dados. Verifique se escreveu o as informações corretamente ou se o banco de dados existe. O erro foi: {e}\033[0m')
    exit()

#Cria a lista de usuários, de IDs e define um contador.
users = []
adm = [('anesuh', '1234')]
ids = []
RESET = "\033[0m"
cont = 0

while True:
    #Exibe o menu na primeira vez que o código for rodado.
    if cont <= 0:
        print(menu())
    
    while True:
        #Validação de entrada do usuário.
        try:
            sleep(0.5)
            choice = int(input('\033[36;1m\nQual opção você deseja escolher?\033[0m'))     
            break
        
        except ValueError as erro:
            print('\033[31;1mERRO! Você deve inserir um número.\033[0m')
    
    #Chama a função de cadastro e pede nome e sobrenome para dar como paramêtros.
    if choice == 1:
        #Verficia se o nome contem apenas letras.
        name = str(input('Nome: '))
        while name.isalpha() == False:
            name = str(input('Digite apenas letras: '))
        lastname = str(input('Sobrenome: '))
        while lastname.isalpha() == False:
            lastname = str(input('Digite apenas letras: '))
        cadastro(name, lastname)
    
    #Chama a função de remover usuário e pede ID para passar como paramêtro.
    elif choice == 2:
        #Valida a entrada do usuário.
        while True:
            try:
                id = int(input('Qual o id que deseja remover? '))
                break
            except ValueError as erro:
                print('\033[31;1mERRO! Você deve inserir um número.\033[0m')
        remover_usuario(id)

    #Limpa a lista de usuários.  
    elif choice == 3:
        #Pede a escolha do usuário.
        choice2 = input('Você tem certeza? [Y/N] ').lower().strip()
        if choice2 == 'y':
            #if len(users) == 0:
                #print('\033[31;1mA lista já está vazia\033[0m')
            #Limpa a lista de usuários.
            clear_query = f'''TRUNCATE TABLE usuario'''
            cursor.execute(clear_query)
            conn.commit()
            users.clear()
            print('\033[32;1mLista limpa com sucesso.\033[0m')
            #Verifica o status atual da lista e mostra uma mensagem de sucesso ou erro.
        #Exibe uma mensagem de erro caso o usuário não escolha nenhuma das duas opções.
        elif choice2 != 'n':
            print('\033[31;1mERRO! Opção inválida. \033[0m')
        else:
            print('\033[31;1mHouve um erro ao tentar limpar a lista.\033[0m')
    
    #Chama a função para buscar um usuário em especifico.
    elif choice == 4:
        #Valida a entrada do usuário.
        while True:
            try:
                #Pede o ID do usuário.
                id = int(input('Qual o id que deseja remover? '))
                break
            except ValueError as erro:
                print('\033[31;1mERRO! Você deve inserir um número.\033[0m')
        buscar_usuario(id)
    
    #Chama a função para mostrar todos os usuários.
    elif choice == 5:
        validation = 0
        while True:
            #Pede a escolha do usuário e trata possiveis erros.
            adm_senha = getpass('Qual a senha do ADM? ')
            for i in adm:
                if adm_senha in i[1]:
                    validation = 1
                    try:     
                        choice2 = int(input('[1] Mostrar por ordem de cadastro\n[2] Mostrar por ordem alfabetica\n[3] Mostrar por ordem de ID\n'))
                        if choice2 == 1 or choice2 == 2 or choice2 == 3:
                            mostrar_todos(choice2)
                            break
                        else:
                            print('\033[31;1mERRO! Opção inválida\033[0m')
                    except ValueError as error:
                        print('\033[31;1mERRO! Opção inválida, escolha um número. \033[0m')
            break
        if validation == 0:
            print('\033[31;1mSenha do ADM incorreta\033[0m')
            
    #Chama a função sair.
    elif choice == 6:
        sair()
    
    #Chama a função menu.
    elif choice == 7:
        print(menu())
    
    elif choice == -1:
        print('\033[1;45;37mVocê selecionou a opção de adicionar um novo administrador no sistema. Por favor, nos de essas informações: ')
        nomeadm_base = input('Usuário adm padrão: ')
        senhaadm_base = getpass('Senha adm padrão: ')
        for c in adm:
            if c[0] == nomeadm_base and c[1] == senhaadm_base:
                before = len(adm)
                name = input('Qual a username que você deseja cadastrar?')
                senha = getpass(f'Qual a senha que você deseja vincular a {name}? ')
                adm_cadastro(name, senha)
                if len(adm) != before:
                    print('ADM CADASTRADO COM SUCESSO')
                print(RESET)
            else:
                print(RESET)
    
    #Exibe uma mensagem de erro caso o usuário não escolha nenhuma das opções apresentadas.
    else:
        print('\033[31;1mEscolha invalida.\033[0m')
    
    #Aumenta o contador.
    cont += 1

#Fim do programa