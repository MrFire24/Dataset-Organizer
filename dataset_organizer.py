import os
import pandas as pd
from pathlib import Path

SYS_TIME = 'sys_time'
GROUPS = ['coordinate', 'io', 'control', 'weld', 'scanner', 'termo', 'set', 'positioner']


def _strip_prefixes(df, group):
    return df.rename(columns=lambda col: col.removeprefix(group + '_') if col != SYS_TIME else col)


def _get_jbi_name(df, custom_name=""):
    if custom_name.strip():
        return custom_name.strip()
    if 'control_jbi_name' in df.columns:
        name = df['control_jbi_name'].iloc[0]
        if not pd.isna(name) and str(name).strip() != '':
            return str(name).strip()
    return 'UNNAMED'


def process_csv(
    file,
    output_path="processed_data",
    custom_name="",
    strip_prefixes=True,
    #additional_files=None
):
    """
    Парсит CSV датасет и раскладывает по файловой структуре.

    Параметры:
        file            - путь к входному CSV файлу
        output_path     - папка для результата
        custom_name     - кастомное имя сессии (по умолчанию берётся из control_jbi_name)
        strip_prefixes  - убирать ли префиксы из названий колонок
        additional_files - список путей к доп. файлам, которые будут скопированы в папку сессии (не реализовано)

    Возвращает:
        Path сессии если успешно, None если отменено
    """
    import shutil

    df = pd.read_csv(file)

    jbi_name = _get_jbi_name(df, custom_name)
    start_time = pd.to_datetime(df[SYS_TIME].iloc[0]).strftime('%Y-%m-%d_%H-%M-%S')

    session_path = Path(output_path) / jbi_name / start_time

    if session_path.exists():
        answer = input(f"Папка {session_path} уже существует. Перезаписать? (y/n): ")
        if answer.lower() != 'y':
            print("Парсинг отменён.")
            return None

    session_path.mkdir(parents=True, exist_ok=True)

    for group in GROUPS:
        cols = [SYS_TIME] + [col for col in df.columns if col.startswith(group + '_')]
        if len(cols) > 1:
            result = df[cols]
            if strip_prefixes:
                result = _strip_prefixes(result, group)
            result.to_csv(session_path / f'{group}.csv', index=False)

    # if additional_files:
    #     pass

    return session_path