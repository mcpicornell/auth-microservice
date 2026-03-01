import ast
from pathlib import Path


class TestArchitectureCompliance:
    def test_domain_does_not_import_infra(self):
        domain_path = (
            Path(__file__).parent.parent.parent.parent / "src" / "app" / "domain"
        )

        for py_file in domain_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not alias.name.startswith("src.app.infra"), (
                            f"{py_file} imports from infra: {alias.name}"
                        )
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith("src.app.infra"):
                        assert False, f"{py_file} imports from infra: {node.module}"

    def test_infra_does_not_import_domain(self):
        infra_path = (
            Path(__file__).parent.parent.parent.parent / "src" / "app" / "infra"
        )

        for py_file in infra_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not alias.name.startswith("src.app.domain"), (
                            f"{py_file} imports from domain: {alias.name}"
                        )
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith("src.app.domain"):
                        assert False, f"{py_file} imports from domain: {node.module}"

    def test_adapters_import_domain_and_infra_only(self):
        adapters_path = (
            Path(__file__).parent.parent.parent.parent / "src" / "app" / "adapters"
        )

        for py_file in adapters_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        if node.module.startswith("src.app.domain"):
                            continue
                        elif node.module.startswith("src.app.infra"):
                            continue
                        elif node.module.startswith("src."):
                            assert False, (
                                f"{py_file} imports from invalid layer: {node.module}"
                            )

    def test_schemas_only_in_infra(self):
        schemas_path = (
            Path(__file__).parent.parent.parent.parent
            / "src"
            / "app"
            / "infra"
            / "api"
            / "schemas"
        )
        assert schemas_path.exists(), "Schemas directory should exist in infra/api/"

        for py_file in schemas_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "BaseModel" in content or "pydantic" in content, (
                f"{py_file} should contain Pydantic models"
            )

    def test_domain_entities_are_dataclasses(self):
        entities_path = (
            Path(__file__).parent.parent.parent.parent
            / "src"
            / "app"
            / "domain"
            / "entities"
        )

        for py_file in entities_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if (
                        "Entity" in node.name
                        or "Input" in node.name
                        or "Output" in node.name
                    ):
                        has_dataclass = any(
                            (isinstance(dec, ast.Name) and dec.id == "dataclass")
                            for dec in node.decorator_list
                        )
                        assert has_dataclass, (
                            f"{py_file}: {node.name} should be a dataclass"
                        )

    def test_no_pydantic_in_domain(self):
        domain_path = (
            Path(__file__).parent.parent.parent.parent / "src" / "app" / "domain"
        )

        for py_file in domain_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "pydantic" not in content, f"{py_file} should not import pydantic"
            assert "BaseModel" not in content, f"{py_file} should not use BaseModel"

    def test_mappers_exist_for_decoupling(self):
        # UserAdapter ahora maneja el mapping directamente
        adapters_path = (
            Path(__file__).parent.parent.parent.parent / "src" / "app" / "adapters"
        )
        assert adapters_path.exists(), "Adapters directory should exist"

        user_adapter = adapters_path / "database" / "user_adapter.py"
        assert user_adapter.exists(), "User adapter should exist"

        # Verificar que UserAdapter tiene método entity_to_dict
        with open(user_adapter, "r", encoding="utf-8") as f:
            content = f.read()
        assert "entity_to_dict" in content, (
            "UserAdapter should have entity_to_dict method"
        )

    def test_infra_uses_schemas_not_domain_entities(self):
        handlers_path = (
            Path(__file__).parent.parent.parent.parent
            / "src"
            / "app"
            / "infra"
            / "api"
            / "handlers"
        )

        for py_file in handlers_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith(
                        "src.app.domain.entities"
                    ):
                        assert False, (
                            f"{py_file} should not import domain entities directly: "
                            f"{node.module}"
                        )
