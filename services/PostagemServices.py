import os
from datetime import datetime
from bson import ObjectId
from dtos.ReturnDto import ReturnDto
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
            return ReturnDto("Postagem criada com sucesso", nova_postagem, 201)

        except Exception as error:
            return ReturnDto("Erro interno no servidor", str(error), 500)

    @staticmethod
    async def listar_postagens():
        try:
            postagens = await postagemRepository.listar_postagens()

            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])
                p["total_comentarios"] = len(p["comentarios"])

            return ReturnDto("Postagens listadas com sucesso", postagens, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)

    @staticmethod
    async def listar_postagens_seguidos(usuario_id):
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
            return ReturnDto("Postagens listadas com sucesso", postagens_seguidos, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)

    @staticmethod
    async def listar_postagens_usuario_especifico(usuario_id):
        try:
            postagens = await postagemRepository.listar_postagens_usuario(usuario_id)

            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])
                p["total_comentarios"] = len(p["comentarios"])

            return ReturnDto("Postagens listadas com sucesso", postagens, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)

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
            return ReturnDto("Postagem curtida/descurtida com sucesso", postagem_atualizada, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)

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
            return ReturnDto("Comentário realizado com sucesso", postagem_atualizada, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)

    @staticmethod
    async def deletar_comentario(postagem_id, comentario_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            for comentario in postagem_encontrada["comentarios"]:
                if comentario["comentario_id"] == comentario_id:
                    if comentario["usuario_id"] == usuario_id or postagem_encontrada["usuario_id"] == usuario_id:
                        postagem_encontrada["comentarios"].remove(comentario)
                    else:
                        return ReturnDto("Operação inválida", "", 401)

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_id,
                                                                              {"comentarios": postagem_encontrada[
                                                                                  "comentarios"]})
            return ReturnDto("Comentário deletado com sucesso", postagem_atualizada, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)

    @staticmethod
    async def atualizar_comentario(postagem_id, comentario_id, usuario_id, comentario_novo):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            for comentario in postagem_encontrada["comentarios"]:
                if comentario["comentario_id"] == comentario_id:
                    if comentario["usuario_id"] == usuario_id:
                        comentario["comentario"] = comentario_novo
                    else:
                        return ReturnDto("Operação inválida", "", 401)

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_id,
                                                                              {"comentarios": postagem_encontrada[
                                                                                  "comentarios"]})
            return ReturnDto("Comentário atualizado com sucesso", postagem_atualizada, 200)

        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)

    @staticmethod
    async def deletar_postagem(postagem_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem_pelo_id(postagem_id)

            if postagem_encontrada["usuario_id"] != usuario_id:
                return ReturnDto("Operação inválida", "", 401)

            await postagemRepository.deletar_postagem(postagem_id)
            return ReturnDto("Postagem deletada com sucesso", "", 200)
        except Exception as error:
            print(error)
            return ReturnDto("Erro interno no servidor", str(error), 500)
