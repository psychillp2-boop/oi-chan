from pathlib import Path


class EmptyFolderScanner:

    def __init__(self, root: Path):
        self.root = root

    def scan(self):

        empty_folders = []

        for folder in self.root.rglob("*"):

            if folder.is_dir():

                # フォルダ内にファイルがあるか確認
                has_files = any(folder.rglob("*"))

                # ただし自身しかない場合は空扱い
                if not any(folder.iterdir()):
                    empty_folders.append(str(folder))

        return empty_folders