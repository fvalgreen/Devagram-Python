from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AWSProvider import AWSProvider
from repositories.UsuarioRepository import UsuarioRepository
from repositories.PostagemRepository import PostagemRepository
from dtos.ReturnDto import ReturnDto

awsProvider = AWSProvider()

usuarioRepository = UsuarioRepository()
postagemRepository = PostagemRepository()

class UsuarioServices:

    async def registrar_usuario(self, usuario: UsuarioCriarModel, caminho_foto: str):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email)

            if usuario_encontrado:
                return ReturnDto(f'E-mail  {usuario.email} já está cadastrado no sistema', "", 400)

            else:
                novo_usuario = await usuarioRepository.criar_usuario(usuario)
                try:
                    url_foto = awsProvider.upload_arquivo_s3(f'fotos-perfil/{novo_usuario["id"]}.png',
                                                             caminho_foto).split('?')[0]

                    await usuarioRepository.atualizar_usuario(novo_usuario['id'], {'avatar': url_foto})
                except Exception as erro:
                    print(erro)

                novo_usuario["avatar"] = url_foto
                return ReturnDto("Usuário cadastrado com sucesso", novo_usuario, 201)

        except Exception as error:
            return ReturnDto("Erro interno no servidor", str(error), 500)

    async def buscar_usuario(self, id: str):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_id(id)
            postagens = await postagemRepository.listar_postagens_usuario(id)

            if usuario_encontrado:
                usuario_encontrado["senha"]=""
                usuario_encontrado["total_seguindo"] = len(usuario_encontrado["seguindo"])
                usuario_encontrado["total_seguidores"] = len(usuario_encontrado["seguidores"])
                usuario_encontrado["postagens"] = postagens
                return ReturnDto("Usuário encontrado", usuario_encontrado, 200)

            else:
                return ReturnDto(f"Usuário com o {id} não foi encontrado", "", 404)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)
    async def buscar_todos_usuario(self):
        try:
            usuarios_encontrados = await usuarioRepository.listar_usuarios()

            for usuario in usuarios_encontrados:
                usuario["total_seguindo"] = len(usuario["seguindo"])
                usuario["total_seguidores"] = len(usuario["seguidores"])
                usuario["senha"] = ""
            return ReturnDto("Usuários listados com sucesso", usuarios_encontrados, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)
    async def buscar_usuario_filtro(self, nome):
        try:
            usuarios_encontrados = await usuarioRepository.buscar_usuario_por_filtro(nome)

            for usuario in usuarios_encontrados:
                usuario["total_seguindo"] = len(usuario["seguindo"])
                usuario["total_seguidores"] = len(usuario["seguidores"])
                usuario["senha"] = ""
            return ReturnDto("Usuários listados com sucesso", usuarios_encontrados, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)
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

                return ReturnDto("Usuário atualizado com sucesso", usuario_atualizado, 200)

            else:
                return ReturnDto(f"Usuário com o {id} não foi encontrado", "", 404)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)
    async def seguir_usuario(seldf, usuario_logado_id, usuario_seguir_id):
        try:
            usuario_logado = await usuarioRepository.buscar_usuario_por_id(usuario_logado_id)
            usuario_seguir = await usuarioRepository.buscar_usuario_por_id(usuario_seguir_id)

            if usuario_seguir["seguidores"].count(usuario_logado_id) > 0:
                usuario_seguir["seguidores"].remove(usuario_logado_id)
                usuario_logado["seguindo"].remove(usuario_seguir_id)
            else:
                usuario_seguir["seguidores"].append(usuario_logado_id)
                usuario_logado["seguindo"].append(usuario_seguir_id)

            await usuarioRepository.atualizar_usuario(usuario_seguir_id, {
                "seguidores": usuario_seguir["seguidores"]
            })
            await usuarioRepository.atualizar_usuario(usuario_logado_id, {
                "seguindo": usuario_logado["seguindo"]
            })

            return ReturnDto("Seguir / deixar de seguir realizado com sucesso", "", 200)
            return {
                "mensagens": "Seguir / deixar de seguir realizado com sucesso",
                "dados": "",
                "status": 200
            }
        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)