import psycopg2


# CONEXAO COM BANCO DE DADOS LOCAL
def conexao():
    dbonline = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'database': 'wave_financas',
        'password': 'Excluiragora1.'
    }

    try:
        conn = psycopg2.connect(**dbonline)
        cursor = conn.cursor()
        print('Conectado')

        return conn, cursor

    except (Exception, psycopg2.Error) as error:
        print('Erro ao conectar', error)


# FUNÇÃO QUE REALIZA CADASTRO DOS USUÁRIOS NO BANCO
def insere_usuario(cursor, conn, nome, email, telefone, senha, foto):
    try:
        with open(foto, 'rb') as arquivo:
            foto_bin = arquivo.read()

        cursor.execute("INSERT INTO public.usuario (nome, email, telefone, senha, foto) VALUES (%s, %s, %s, %s, %s)",
                       (nome, email, telefone, senha, foto_bin))
        conn.commit()

        print('Novo usuário inserido')

    except (Exception, psycopg2.Error) as error:
        print("Erro ao inserir", error)


# INICIA CONEXÃO COM BANCO DE DADOS
banco = conexao()
conn, cursor = banco

# PASSAR CAMINHO DA FOTO E DADOS DO USUÁRIO
foto = r"C:\Users\yurym\OneDrive\Imagens\WhatsApp Image 2024-07-29 at 17.17.38.jpeg"
#insere_usuario(cursor, conn, 'yury', 'yurymiguelc1@gmail.com', '(34) 984104848', 'Excluiragora1.', foto)