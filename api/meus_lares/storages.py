import mimetypes
import os
import zipfile

import boto3
import rarfile
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".txt",
    ".xlsx",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".csv",
    ".json",
    ".xml",
    ".yaml",
    ".zip",
    ".rar",
]
ALLOWED_MIME_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/zip",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/x-rar-compressed",
    "image/jpeg",
    "image/png",
    "text/csv",
    "application/json",
]


def validate_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Extension not allowed: {ext}.")

    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValidationError(f"Invalid MIME-Type: {mime_type}.")

    if ".." in file.name or "/" in file.name:
        raise ValidationError("Invalid file name!")

    max_size = 20 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError("The maximum size allowed is 20 MB.")

    validate_compressed_contents(file)


def validate_compressed_contents(file):
    if zipfile.is_zipfile(file):
        with zipfile.ZipFile(file, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith((".exe", ".bat", ".sh", ".php", ".js")):
                    raise ValidationError(
                        f"Arquivo malicioso detectado no ZIP: {file_name}"
                    )

    if rarfile.is_rarfile(file):
        with rarfile.RarFile(file, "r") as rar_ref:
            for file_name in rar_ref.namelist():
                if file_name.endswith((".exe", ".bat", ".sh", ".php", ".js")):
                    raise ValidationError(
                        f"Arquivo malicioso detectado no RAR: {file_name}"
                    )


if settings.DEBUG:

    class PublicMediaStorage(FileSystemStorage):
        location = os.path.join(settings.BASE_DIR, "media", "public")
        base_url = "/media/public/"

    class PrivateMediaStorage(FileSystemStorage):
        location = os.path.join(settings.BASE_DIR, "media", "private")
        base_url = "/media/private/"

else:

    class PublicMediaStorage(S3Boto3Storage):
        location = settings.AWS_MEDIA_LOCATION
        default_acl = "public-read"

    class PrivateMediaStorage(S3Boto3Storage):
        location = settings.AWS_PRIVATE_MEDIA_LOCATION
        default_acl = "private"
        custom_domain = False

        def url(self, name):
            s3_client = boto3.client(
                "s3",
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            return s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": self._normalize_name(name)},
                ExpiresIn=120,
            )
