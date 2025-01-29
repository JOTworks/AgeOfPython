import ast


class Aoe2Tree:
    def __init__(
        self,
        main_tree=ast.Module(body=[]),
        func_tree=ast.Module(body=[]),
        const_tree=ast.Module(body=[]),
    ):
        self.main_tree = main_tree
        self.func_tree = func_tree
        self.const_tree = const_tree

    def __itter__(self):
        return self.main_tree, self.func_tree, self.const_tree


class Parser:
    def __init__(self, file_name, ai_folder):
        self.trees = Aoe2Tree()
        self.file_name = file_name
        self.ai_folder = ai_folder

    def parse(self):
        asts = self.parse_multiple_files(self.file_name, self.ai_folder)
        assert isinstance(self.trees, Aoe2Tree)
        self.trees.main_tree = asts[self.file_name]
        asts.pop(self.file_name)

        # remove all functions and constants from main tree to their respective trees
        for node in list(self.trees.main_tree.body):
            if isinstance(node, ast.FunctionDef):
                self.trees.func_tree.body.append(node)
                self.trees.main_tree.body.remove(node)
            elif isinstance(node, ast.ImportFrom):
                self.trees.main_tree.body.remove(node)
            elif isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call) and node.value.func.id == "Const":
                    self.trees.const_tree.body.append(node)
                    self.trees.main_tree.body.remove(node)

        # add functions and constants from imports to their respective trees
        for tree_filename, tree in asts.items():
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    self.trees.func_tree.body.append(node)
                elif isinstance(node, ast.Assign):
                    self.trees.const_tree.body.append(node)
                else:
                    raise Exception(
                        f"Only FunctionDefs and Assigns allowed in imports, not {type(node)}"
                    )

        return self.trees

    def parse_multiple_files(self, base_file, ai_folder) -> Aoe2Tree:
        """Parses the given file and all its imports.
        the imports will only have functdef, assign in their tree.
        they will have edited names if imported with the as keyword
        """
        parsed_files = set()  # Keep track of parsed files to avoid cycles
        asts = {}

        def parse_file(file_name, ai_folder, names, base_file=False):
            import_all = False
            alias_names = [alias.name for alias in names]
            alias_asnames = dict(
                [
                    (alias.name, alias.asname)
                    if hasattr(alias, "asname")
                    else (alias.name, alias.name)
                    for alias in names
                ]
            )
            if alias_names == ["*"]:
                alias_names = []
                import_all = True

            file_path = get_file_path(file_name, ai_folder)
            if file_path in parsed_files:
                return
            parsed_files.add(file_path)

            with open(file_path, "r") as f:
                tree = ast.parse(f.read(), filename=file_path)

                for node in ast.walk(
                    tree
                ):  # needed for printer to find sourcecode for comments
                    node.file_path = file_path

                module = ast.Module(body=[])
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef) and (
                        node.name in alias_names or import_all
                    ):
                        if not import_all:
                            alias_names.remove(node.name)
                            node.name = alias_asnames[node.name]
                        module.body.append(node)
                    elif isinstance(node, ast.Assign):
                        if len(node.targets) != 1:
                            raise Exception("Only one target allowed in assignment")
                        if isinstance(node.targets[0], ast.Name) and (
                            node.targets[0].id in alias_names or import_all
                        ):
                            if not import_all:
                                alias_names.remove(node.targets[0].id)
                                node.targets[0].id = alias_asnames[node.targets[0].id]
                            module.body.append(node)
                    elif isinstance(node, ast.ImportFrom):
                        if not (
                            "aoe2scriptEnums" in node.module
                            or "aoe2scriptFunctions" in node.module
                            or "scraper" in node.module
                        ):
                            parse_file(node.module, ai_folder, node.names)
                if len(alias_names) > 0 and "*" not in alias_names:
                    raise Exception(f"{alias_names} not found in {file_name}")

                if base_file:
                    asts[file_name] = tree
                else:
                    asts[file_name] = module

        parse_file(base_file, ai_folder, [ast.alias("*")], base_file=True)
        return asts


def get_file_path(file_name, ai_folder):  # TODO: issue if 2 files have same name
    # OPEN FILE
    fullPath = "FILE NOT FOUND"
    file_name = file_name.replace("/", "\\")
    for file in list(ai_folder.glob("**/*.per")):
        if file_name + ".per" in str(file) or file_name in str(file):
            fullPath = file
    for file in list(
        ai_folder.glob("**/*.aop")
    ):  # prioritizes aop files because it is last
        if file_name + ".aop" in str(file) or file_name in str(file):
            fullPath = file
    for file in list(
        ai_folder.glob("**/*.py")
    ):  # prioritizes aop files because it is last
        if file_name + ".aop" in str(file) or file_name in str(file):
            fullPath = file
    if fullPath == "FILE NOT FOUND":
        raise Exception(file_name + " is not found")
    # infile = open(os.path.join(os.path.dirname(sys.argv[0]), "folder2/test.txt"), "r+")
    return fullPath
