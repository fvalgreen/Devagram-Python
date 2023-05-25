import boto3
from botocore.exceptions import ClientError
from decouple import config


class AWSProvider:

    def upload_arquivo_s3(self, caminho_para_salvar, caminho_do_arquivo, bucket='devagram-python-fvalgreen'):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
        )

        try:
            response = s3_client.upload_file(caminho_do_arquivo, bucket, Key=caminho_para_salvar, ExtraArgs={'ACL': 'public-read'})
            url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': caminho_para_salvar})
            return url
        except ClientError as erro:
            print(erro)
            return False