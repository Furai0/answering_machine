import os
from datetime import datetime

def bug_report(filename: str, text: str, time_format: str = "%Y-%m-%d %H:%M:%S") -> None:
    """
    Создаёт/открывает файл в той же папке, где находится этот скрипт (fallback — текущая рабочая папка),
    и добавляет строку вида:
        "<timestamp> <text>\n"
    Гарантируется, что запись будет на новой строке, даже если файл существовал и не заканчивался '\n'.
    """
    # Папка, где расположен скрипт. Если __file__ не доступен (интерактив), используем cwd.
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__)) or os.getcwd()
    except NameError:
        base_dir = os.getcwd()

    file_path = os.path.join(base_dir, filename)

    # Создаём директорию, если по какой-то причине указано вложение (на всякий случай)
    dirpath = os.path.dirname(file_path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    timestamp = datetime.now().strftime(time_format)
    line = f"{timestamp} {text}\n"

    # Проверяем, нужно ли добавить перевод строки перед новой записью
    prefix = ""
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as fb:
                if fb.tell() == 0:
                    # файл пустой
                    pass
                else:
                    fb.seek(-1, os.SEEK_END)
                    last_byte = fb.read(1)
                    if last_byte != b"\n":
                        prefix = "\n"
        except OSError:
            # если не удалось читать в бинарном режиме — игнорируем и просто дописываем
            pass

    with open(file_path, "a", encoding="utf-8") as f:
        if prefix:
            f.write(prefix)
        f.write(line)

