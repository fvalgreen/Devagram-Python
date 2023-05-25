import time
import jwt
from decouple import config
from models.UsuarioModel import UsuarioLoginModel
from repositories.UsuarioRepository import buscar_usuario_por_email
from utils.AuthUtil import verificar_senha

JWT_SECRET = config('JWT_SECRET') # Pega as chave JWT na ENV

def gerar_token_jwt(usuario_id: str) -> str: # Define uma função que irá gerar o token JWT

    payload = { # Criando um payload para o token que passa o id do usuário e um tempo de expiração
        "usuario_id": usuario_id,
        "expires": time.time() + 600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256") # Criando o token passando o payload criado e
    # guardando na variável token

    return token # Retornando o token criado

def decodificar_token_jwt(token: str): # Define uma função que irá desencriptografar o token
    try:
        token_decodificado = jwt.decode(token, JWT_SECRET, algorithms="HS256") # Decodifica o token passado de acordo
        # com a chave

        if token_decodificado["expires"] >= time.time(): # Se o tempo de expiração for maior que o horário atual
            # significa que o token ainda é válido e então retorna o token decodificado
            return token_decodificado
        else: return None # Se o tempo for menor ao horário atual retorna None indicando que o token é inválido

    except Exception as erro:
        return None



async def login_service(usuario: UsuarioLoginModel): # define a função login service recebendo como parametro um
    # usuário seguindo o modelo UsuarioLoginModel
    usuario_encontrado = await buscar_usuario_por_email(usuario.email) # busca por email o usupário

    if not usuario_encontrado: # Caso não exista o email cadastrado volta um erro de email ou senha incorretos
        return {
            "mensagem": "Email ou Senha incorreto",
            "status": 401
        }
    else: # Caso retorne um usuário com o email
        if verificar_senha(usuario.senha, usuario_encontrado['senha']): # Caso a senha informada e a senha que
            # retornou do banco de dados sejam iguais
            usuario_encontrado['senha'] = '' #Definimos a senha que retornou do banco de dados como uma string vazia
            # para não trafegar a senha do usuário
            token = gerar_token_jwt(usuario_encontrado["id"]) # Geramos um token para o usuário passando o ID do msm
            usuario_encontrado["token"] = token # Criamos a propriedade token na dict retornada da DB e colocamos o
            # token gerado nela
            return { # Retornamos o sucesso e os dados do usuário
                "mensagem": "Login realizado com sucesso",
                "dados": usuario_encontrado,
                "status": 200
            }
        else: # Caso a senha não seja igual retorna um erro de email ou senha incorretos
            return {
                "mensagem": "Email ou Senha incorreto",
                "status": 401
            }