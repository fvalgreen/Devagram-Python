from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # importa um criptografador para criptografar a


# senha do usuário e evitar que ela trafegue sem estar protegida

class AuthUtils:
    @staticmethod
    def gerar_senha_criptografada(senha):
        return pwd_context.hash(senha)  # Criptografa a senha do usuário

    @staticmethod
    def verificar_senha(senha, senha_criptografada):
        return pwd_context.verify(senha,
                                  senha_criptografada)  # Verifica se a senha informada é a mesma senha do usuário
