from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AWSProvider import AWSProvider
from repositories.UsuarioRepository import UsuarioRepository

awsProvider = AWSProvider()

usuarioRepository = UsuarioRepository()


class UsuarioServices:

    async def registrar_usuario(self, usuario: UsuarioCriarModel, caminho_foto: str): # Cria a função de registrar o
        # usuário
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email) # busca o usuário na
            # DB pelo email

            if usuario_encontrado: # Caso retorne algum usuário com esse e-amil dá um erro informando que o e-mail já
                # está cadastrado no sistema
                return {
                    "mensagem": f'E-mail  {usuario.email} já está cadastrado no sistema',
                    "dados": "",
                    "status": 400
                }
            else: # Caso não retorne nenhum usuário com esse e-mail cria o usuário passando os dados
                novo_usuario = await usuarioRepository.criar_usuario(usuario)
                try:
                    url_foto = awsProvider.upload_arquivo_s3(f'fotos-perfil/{novo_usuario["id"]}.png',
                                                             caminho_foto).split('?')[0]

                    await usuarioRepository.atualizar_usuario(novo_usuario['id'], {'avatar': url_foto})
                except Exception as erro:
                    print(erro)

                novo_usuario["avatar"] = url_foto
                return{ # Retorna uma mensagem de sucesso e os dados do usuário
                    "mensagem": "Usuário cadastrado com sucesso",
                    "dados": novo_usuario,
                    "status": 201
                }
        except Exception as error:
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500

            }

    async def buscar_usuario(self, id: str):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_id(id)

            if usuario_encontrado:
                usuario_encontrado["senha"]=""
                return { # Retorna uma mensagem de sucesso e os dados do usuário
                    "mensagem": "Usuário encontrado",
                    "dados": usuario_encontrado,
                    "status": 200
                }

            else:
                return {
                    "mensagem": f"Usuário com o {id} não foi encontrado",
                    "status": 404
                }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }
    async def atualizar_usuario_logado(self, id, usuarioAtualizar: UsuarioAtualizarModel, caminho_foto: str):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_id(id)

            if usuario_encontrado:
                try:
                    url_foto = awsProvider.upload_arquivo_s3(f'fotos-perfil/{id}.png',
                                                             caminho_foto).split('?')[0]

                    await usuarioRepository.atualizar_usuario(id, {'avatar': url_foto})
                except Exception as erro:
                    print(erro)
                usuario_atualizado = await usuarioRepository.atualizar_usuario(id, usuarioAtualizar.__dict__)
                usuario_atualizado['senha'] = ''
                return {
                    "mensagem": "Usuário atualizado com sucesso",
                    "dados": usuario_atualizado,
                    "status": 200
                }

            else:
                return {
                    "mensagem": f"Usuário com o {id} não foi encontrado",
                    "status": 404
                }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }