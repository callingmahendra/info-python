

class FileHandler:
    @staticmethod
    def save_file(file_path: str, content: str):
        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def read_file(file_path: str) -> str:
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception:
            # if file is not found, return empty string
            return ""