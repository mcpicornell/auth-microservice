from src.app.adapters.security.password_adapter import PasswordAdapter


class TestPasswordAdapter:
    def test_hash_password(self, mocker):
        mock_ctx = mocker.Mock()
        mock_ctx.hash.return_value = "$2b$12$hashedpassword"

        with mocker.patch(
            "src.app.adapters.security.password_adapter.CryptContext",
            return_value=mock_ctx,
        ):
            adapter = PasswordAdapter()
            result = adapter.hash_password("test")

            assert result == "$2b$12$hashedpassword"
            mock_ctx.hash.assert_called_once_with("test")

    def test_verify_password_correct(self, mocker):
        mock_ctx = mocker.Mock()
        mock_ctx.verify.return_value = True

        with mocker.patch(
            "src.app.adapters.security.password_adapter.CryptContext",
            return_value=mock_ctx,
        ):
            adapter = PasswordAdapter()
            result = adapter.verify_password("test", "$2b$12$hashedpassword")

            assert result is True
            mock_ctx.verify.assert_called_once_with("test", "$2b$12$hashedpassword")

    def test_verify_password_incorrect(self, mocker):
        mock_ctx = mocker.Mock()
        mock_ctx.verify.return_value = False

        with mocker.patch(
            "src.app.adapters.security.password_adapter.CryptContext",
            return_value=mock_ctx,
        ):
            adapter = PasswordAdapter()
            result = adapter.verify_password("wrong", "$2b$12$hashedpassword")

            assert result is False
            mock_ctx.verify.assert_called_once_with("wrong", "$2b$12$hashedpassword")

    def test_verify_password_with_invalid_hash(self, mocker):
        mock_ctx = mocker.Mock()
        mock_ctx.verify.return_value = False

        with mocker.patch(
            "src.app.adapters.security.password_adapter.CryptContext",
            return_value=mock_ctx,
        ):
            adapter = PasswordAdapter()
            result = adapter.verify_password("test", "invalid_hash")

            assert result is False
            mock_ctx.verify.assert_called_once_with("test", "invalid_hash")

    def test_hash_different_passwords_produce_different_hashes(self, mocker):
        mock_ctx = mocker.Mock()
        mock_ctx.hash.side_effect = ["$2b$12$hash1", "$2b$12$hash2"]

        with mocker.patch(
            "src.app.adapters.security.password_adapter.CryptContext",
            return_value=mock_ctx,
        ):
            adapter = PasswordAdapter()
            hash1 = adapter.hash_password("pass1")
            hash2 = adapter.hash_password("pass2")

            assert hash1 != hash2
            assert mock_ctx.hash.call_count == 2

    def test_hash_same_password_produces_different_hashes(self, mocker):
        mock_ctx = mocker.Mock()
        mock_ctx.hash.side_effect = ["$2b$12$hash1", "$2b$12$hash2"]

        with mocker.patch(
            "src.app.adapters.security.password_adapter.CryptContext",
            return_value=mock_ctx,
        ):
            adapter = PasswordAdapter()
            hash1 = adapter.hash_password("same")
            hash2 = adapter.hash_password("same")

            # bcrypt uses salt, so same password should produce different hashes
            assert hash1 != hash2
            assert mock_ctx.hash.call_count == 2
