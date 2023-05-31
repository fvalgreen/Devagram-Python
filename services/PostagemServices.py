import os
from datetime import datetime

from bson import ObjectId

from providers.AWSProvider import AWSProvider
from repositories.PostagemRepository import PostagemRepository
from repositories.UsuarioRepository import UsuarioRepository

awsProvider = AWSProvider()

postagemRepository = PostagemRepository()
usuarioRepository = UsuarioRepository()


class PostagemServices:

    @staticmethod
    async def criar_postagem(postagem, usuario_id):

        try:
            nova_postagem = await postagemRepository.criar_postagem(postagem.legenda, usuario_id)
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_id(usuario_id)

            try:
                caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}'

                with open(caminho_foto, 'wb+') as arquivo:
                    arquivo.write(postagem.foto.file.read())
                url_foto = awsProvider.upload_arquivo_s3(f'fotos-postagens/{nova_postagem["id"]}.png',
                                                         caminho_foto).split('?')[0]

                nova_postagem = await postagemRepository.atualizar_postagem(nova_postagem["id"], {"foto": url_foto})
                if nova_postagem:
                    publicacoes_totais = usuario_encontrado["publicacoes"] + 1
                    await usuarioRepository.atualizar_usuario(usuario_id, {"publicacoes": publicacoes_totais})
                os.remove(caminho_foto)
            except Exception as erro:
                print(erro)

            return {
                "mensagem": "Postagem criada com sucesso",
                "dados": nova_postagem,
                "status": 201
            }
        except Exception as error:
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500

            }

    @staticmethod
    async def listar_postagens():
        try:
            postagens = await postagemRepository.listar_postagens()

            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])
                p["total_comentarios"] = len(p["comentarios"])

            return {
                "mensagens": "Postagens listadas com sucesso",
                "dados": postagens,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }

    async def listar_postagens_seguidos(self, usuario_id):
        try:
            postagens = await postagemRepository.listar_postagens()
            usuario_logado = await usuarioRepository.buscar_usuario_por_id(usuario_id)
            postagens_seguidos = []
            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])
                p["total_comentarios"] = len(p["comentarios"])
                for seguindo in usuario_logado["seguindo"]:
                    if p["usuario_id"] == seguindo or p["usuario_id"] == usuario_id:
                        postagens_seguidos.append(p)

            return {
                "mensagens": "Postagens listadas com sucesso",
                "dados": postagens_seguidos,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }

    @staticmethod
    async def listar_postagens_usuario_especifico(usuario_id):
        try:
            postagens = await postagemRepository.listar_postagens_usuario(usuario_id)

            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])
                p["total_comentarios"] = len(p["comentarios"])

            return {
                "mensagens": "Postagens listadas com sucesso",
                "dados": postagens,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }

    @staticmethod
    async def curtir_postagem(postagem_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            if postagem_encontrada["curtidas"].count(usuario_id):
                postagem_encontrada["curtidas"].remove(usuario_id)
            else:
                postagem_encontrada["curtidas"].append(usuario_id)

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_id, {
                "curtidas": postagem_encontrada["curtidas"]})
            return {
                "mensagens": "Postagem curtida/descurtida com sucesso",
                "dados": postagem_atualizada,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }

    @staticmethod
    async def comentar_publicacao(postagem_id, usuario_id, comentario):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            postagem_encontrada["comentarios"].append(
                {
                    "comentario_id": ObjectId(),
                    "usuario_id": usuario_id,
                    "comentario": comentario
                }
            )

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_id,
                                                                              {"comentarios": postagem_encontrada[
                                                                                  "comentarios"]})
            return {
                "mensagem": "Comentário realizado com sucesso",
                "dados": postagem_atualizada,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }

    @staticmethod
    async def deletar_comentario(postagem_id, comentario_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            for comentario in postagem_encontrada["comentarios"]:
                if comentario["comentario_id"] == comentario_id:
                    if comentario["usuario_id"] == usuario_id or postagem_encontrada["usuario_id"] == usuario_id:
                        postagem_encontrada["comentarios"].remove(comentario)
                    else:
                        return {
                            "mensagem": "Operação inválida",
                            "dados": "",
                            "status": 401
                        }

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_id,
                                                                              {"comentarios": postagem_encontrada[
                                                                                  "comentarios"]})
            return {
                "mensagem": "Comentário realizado com sucesso",
                "dados": postagem_atualizada,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }

    @staticmethod
    async def atualizar_comentario(postagem_id, comentario_id, usuario_id, comentario_novo):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            for comentario in postagem_encontrada["comentarios"]:
                if comentario["comentario_id"] == comentario_id:
                    if comentario["usuario_id"] == usuario_id:
                        comentario["comentario"] = comentario_novo
                    else:
                        return {
                            "mensagem": "Operação inválida",
                            "dados": "",
                            "status": 401
                        }

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_id,
                                                                              {"comentarios": postagem_encontrada[
                                                                                  "comentarios"]})
            return {
                "mensagem": "Comentário atualizado com sucesso",
                "dados": postagem_atualizada,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }

    @staticmethod
    async def deletar_postagem(postagem_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            if postagem_encontrada["usuario_id"] != usuario_id:
                return {
                    "mensagem": "Não é possível realizar essa ação",
                    "dados": "",
                    "status": 401
                }

            await postagemRepository.deletar_postagem(postagem_id)
            return {
                "mensagem": "Postagem deletada com sucesso",
                "dados": "",
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }
