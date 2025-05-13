import os
from mcp.server.fastmcp import FastMCP
from core.cfg import CFG

mcp = FastMCP("FileTools")

BASE_DIR = CFG.BASE_DIR

os.makedirs(BASE_DIR, exist_ok=True)

@mcp.tool()
def create_folder(folder_name: str) -> str:
    """Создаёт папку с указанным именем в базовой директории."""
    folder_path = os.path.join(BASE_DIR, folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        return f"Папка '{folder_name}' успешно создана."
    except Exception as e:
        return f"Ошибка при создании папки: {e}"

@mcp.tool()
def create_text_file(file_name: str, content: str) -> str:
    """Создаёт текстовый файл с указанным именем и содержимым в базовой директории."""
    file_path = os.path.join(BASE_DIR, file_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Файл '{file_name}' успешно создан."
    except Exception as e:
        return f"Ошибка при создании файла: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
