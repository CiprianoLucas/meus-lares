from storages.backends.s3boto3 import S3Boto3Storage
import boto3
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

if False:
    class PublicMediaStorage(FileSystemStorage):
        location = os.path.join(settings.BASE_DIR, 'media', 'public')
        base_url = '/media/public/'

    class PrivateMediaStorage(FileSystemStorage):
        location = os.path.join(settings.BASE_DIR, 'media', 'private')
        base_url = '/media/private/'

else:
    class PublicMediaStorage(S3Boto3Storage):
        location = settings.AWS_MEDIA_LOCATION
        default_acl = 'public-read'

    class PrivateMediaStorage(S3Boto3Storage):
        location = settings.AWS_PRIVATE_MEDIA_LOCATION
        default_acl = 'private'
        custom_domain = False

        def url(self, name):
            s3_client = boto3.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        
            return s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': self._normalize_name(name)},
                ExpiresIn=120
            )
