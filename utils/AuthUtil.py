from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUtils:
    @staticmethod
    def gerar_senha_criptografada(senha):
        return pwd_context.hash(senha)

    @staticmethod
    def verificar_senha(senha, senha_criptografada):
        return pwd_context.verify(senha,
                                  senha_criptografada)
