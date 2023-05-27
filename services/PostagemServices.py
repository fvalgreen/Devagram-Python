import os
from datetime import datetime
from providers.AWSProvider import AWSProvider
from repositories.PostagemRepository import PostagemRepository

awsProvider = AWSProvider()

postagemRepository = PostagemRepository()


class PostagemServices:

    async def criar_postagem(self, postagem, usuario_id):

        try:
            nova_postagem = await postagemRepository.criar_postagem(postagem.legenda, usuario_id)

            try:
                caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}'

                with open(caminho_foto, 'wb+') as arquivo:
                    arquivo.write(postagem.foto.file.read())
                url_foto = awsProvider.upload_arquivo_s3(f'fotos-postagens/{nova_postagem["id"]}.png',
                                                         caminho_foto).split('?')[0]

                nova_postagem = await postagemRepository.atualizar_postagem(nova_postagem["id"], {"foto": url_foto})
                os.remove(caminho_foto)
            except Exception as erro:
                print(erro)

            return{
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


    async def listar_postagens(self):
        try:
            postagens = await postagemRepository.listar_postagens()

            return{
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