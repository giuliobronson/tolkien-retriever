import pytest

from core.ports.storage.file_storage import IFileStorage


class TestMinIOStorageIntegration:
    """Testes de integração da classe MinIOStorage"""

    def test_upload_pdf_creates_file(self, minio_storage: IFileStorage):
        """Upload de arquivo PDF e verifica se foi criado no storage"""
        # Arrange
        filename = "document.pdf"
        content = b"%PDF-1.4 mock PDF content"
        content_type = "application/pdf"

        # Act
        minio_storage.upload(filename, content, content_type)

        # Assert
        assert minio_storage.exists(
            filename
        ), f"Arquivo {filename} deveria existir após upload"

    def test_upload_empty_file(self, minio_storage: IFileStorage):
        """Upload vazio: cria arquivo mesmo com 0 bytes"""
        # Arrange
        filename = "empty.txt"
        content = b""  # Arquivo vazio
        content_type = "text/plain"

        # Act
        minio_storage.upload(filename, content, content_type)

        # Assert
        assert minio_storage.exists(
            filename
        ), f"Arquivo vazio {filename} deveria existir após upload"

    def test_upload_with_none_content_type(self, minio_storage: IFileStorage):
        """Upload sem content_type: usa content-type padrão"""
        # Arrange
        filename = "binary.bin"
        content = b"\x00\x01\x02\x03"
        content_type = None

        # Act
        minio_storage.upload(filename, content, content_type)

        # Assert
        assert minio_storage.exists(
            filename
        ), f"Arquivo {filename} deveria existir com content_type default"

    def test_exists_returns_true_for_existing_file(self, minio_storage: IFileStorage):
        """exists: retorna True para arquivo existente"""
        # Arrange
        filename = "existing_file.txt"
        content = b"Some content"
        minio_storage.upload(filename, content, "text/plain")

        # Act
        result = minio_storage.exists(filename)

        # Assert
        assert result is True, f"exists() deveria retornar True para arquivo que existe"

    def test_exists_returns_false_for_nonexistent_file(
        self, minio_storage: IFileStorage
    ):
        """exists: retorna False para arquivo inexistente"""
        # Arrange
        filename = "nonexistent_file_xyz_123.txt"

        # Act
        result = minio_storage.exists(filename)

        # Assert
        assert (
            result is False
        ), f"exists() deveria retornar False para arquivo inexistente"

    def test_download_retrieves_uploaded_content(self, minio_storage: IFileStorage):
        """Download: retorna o mesmo conteúdo que foi upado"""
        # Arrange
        filename = "content_test.txt"
        original_content = b"This is the original content that was uploaded"
        minio_storage.upload(filename, original_content, "text/plain")

        # Act
        downloaded_content = minio_storage.download(filename)

        # Assert
        assert (
            downloaded_content == original_content
        ), "Conteúdo baixado deveria ser idêntico ao upado"

    def test_download_empty_file(self, minio_storage: IFileStorage):
        """Download vazio: retorna bytes vazios"""
        # Arrange
        filename = "empty_download.txt"
        original_content = b""
        minio_storage.upload(filename, original_content, "text/plain")

        # Act
        downloaded_content = minio_storage.download(filename)

        # Assert
        assert (
            downloaded_content == b""
        ), "Download de arquivo vazio deveria retornar b''"

    def test_download_nonexistent_file_raises_error(self, minio_storage: IFileStorage):
        """Download inexistente: lança exceção"""
        # Arrange
        filename = "does_not_exist_xyz_123.txt"

        # Act & Assert
        with pytest.raises(Exception):
            minio_storage.download(filename)

    def test_multiple_uploads_same_path_overwrites(self, minio_storage: IFileStorage):
        """Upload no mesmo path: novo upload sobrescreve o anterior"""
        # Arrange
        filename = "overwrite_test.txt"
        content_v1 = b"Version 1"
        content_v2 = b"Version 2 - Overwritten"

        # Act - Upload versão 1
        minio_storage.upload(filename, content_v1, "text/plain")
        assert minio_storage.download(filename) == content_v1

        # Act - Upload versão 2 (sobrescreve)
        minio_storage.upload(filename, content_v2, "text/plain")

        # Assert - Versão 2 está lá
        assert (
            minio_storage.download(filename) == content_v2
        ), "Novo upload deveria sobrescrever o anterior"
