import ast
from pathlib import Path


class TestArchitectureRules:
    def test_domain_never_imports_from_infra(self):
        domain_path = Path("src/app/domain")
        infra_imports = []

        for py_file in domain_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            with open(py_file, "r") as f:
                content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name.startswith("src.app.infra"):
                                infra_imports.append(f"{py_file}: {alias.name}")
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and node.module.startswith("src.app.infra"):
                            infra_imports.append(f"{py_file}: from {node.module}")

        assert not infra_imports, f"Domain imports from infra found: {infra_imports}"

    def test_infra_never_imports_from_domain(self):
        infra_path = Path("src/app/infra")
        domain_imports = []

        for py_file in infra_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            with open(py_file, "r") as f:
                content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name.startswith("src.app.domain"):
                                domain_imports.append(f"{py_file}: {alias.name}")
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and node.module.startswith("src.app.domain"):
                            domain_imports.append(f"{py_file}: from {node.module}")

        assert not domain_imports, f"Infra imports from domain found: {domain_imports}"

    def test_adapters_only_import_from_domain_and_infra(self):
        adapters_path = Path("src/app/adapters")
        forbidden_imports = []

        for py_file in adapters_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            with open(py_file, "r") as f:
                content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if (
                                alias.name.startswith("src.app")
                                and not alias.name.startswith("src.app.domain")
                                and not alias.name.startswith("src.app.infra")
                                and not alias.name.startswith("src.app.adapters")
                            ):
                                forbidden_imports.append(f"{py_file}: {alias.name}")
                    elif isinstance(node, ast.ImportFrom):
                        if (
                            node.module
                            and node.module.startswith("src.app")
                            and not node.module.startswith("src.app.domain")
                            and not node.module.startswith("src.app.infra")
                            and not node.module.startswith("src.app.adapters")
                        ):
                            forbidden_imports.append(f"{py_file}: from {node.module}")

        assert not forbidden_imports, (
            f"Adapters import forbidden modules: {forbidden_imports}"
        )

    def test_infra_managers_have_port_protocols(self):
        infra_path = Path("src/app/infra")
        missing_ports = []

        for py_file in infra_path.rglob("*manager.py"):
            with open(py_file, "r") as f:
                content = f.read()

                if "Manager" in content and "Protocol" not in content:
                    missing_ports.append(str(py_file))

        assert not missing_ports, f"Managers without port protocols: {missing_ports}"

    def test_adapters_use_protocols_not_concrete_classes(self):
        adapters_path = Path("src/app/adapters")
        concrete_type_usage = []

        for py_file in adapters_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            with open(py_file, "r") as f:
                content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                        for arg in node.args.args:
                            if arg.annotation:
                                annotation_str = (
                                    ast.unparse(arg.annotation)
                                    if hasattr(ast, "unparse")
                                    else str(arg.annotation)
                                )
                                if (
                                    "Manager" in annotation_str
                                    and "Protocol" not in annotation_str
                                    and "Port" not in annotation_str
                                ):
                                    concrete_type_usage.append(
                                        f"{py_file}: {arg.arg} - {annotation_str}"
                                    )

        assert not concrete_type_usage, (
            f"Adapters using concrete types: {concrete_type_usage}"
        )

    def test_no_full_settings_passed_to_managers(self):
        infra_path = Path("src/app/infra")
        settings_usage = []

        for py_file in infra_path.rglob("*manager.py"):
            with open(py_file, "r") as f:
                content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                        for arg in node.args.args:
                            if arg.annotation:
                                annotation_str = (
                                    ast.unparse(arg.annotation)
                                    if hasattr(ast, "unparse")
                                    else str(arg.annotation)
                                )
                                if "Settings" in annotation_str:
                                    settings_usage.append(
                                        f"{py_file}: {arg.arg} - {annotation_str}"
                                    )

        assert not settings_usage, f"Managers receiving full settings: {settings_usage}"
