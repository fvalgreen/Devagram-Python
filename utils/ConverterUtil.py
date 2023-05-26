class ConverterUtil:
    @staticmethod
    def usuario_converter(usuario):  # define uma função helper que pega o usuário e transforma numa dict

        return {
            "id": str(usuario["_id"]),
            "nome": usuario['nome'],
            "email": usuario['email'],
            "senha": usuario['senha'],
            "avatar": usuario['avatar'] if 'avatar' in usuario else '',
            "seguidores": usuario['seguidores'],
            "seguindo": usuario['seguindo'],
            "publicacoes": usuario['publicacoes']
        }

    @staticmethod
    def postagem_converter(postagem):
        return {
            "id": str(postagem["_id"]),
            "usuario_id": str(postagem["usuario_id"]),
            "foto": postagem["foto"],
            "legenda": postagem["legenda"],
            "data": postagem["data"],
            "curtidas": postagem["curtidas"],
            "comentarios": postagem["comentarios"]
        }
