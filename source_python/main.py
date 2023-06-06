import os
import sys
import shutil
import subprocess

import random

from loguru import logger

logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', enqueue=True)

bundle_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(os.path.dirname(__file__))
path_to_unrar = os.path.join(bundle_dir, 'unrar.exe')
#path_to_unrar = r'"unrar.exe"'


def get_struct(archname: str, path_to_unrar: str) -> list:
    get_struct_command = fr'{path_to_unrar} lt {archname}'
    x = set([file for file in os.popen(get_struct_command).read().split('\n') if file.endswith('.txt')])
    return list(x)


def delete_subfolder(path_source: str):
    while True:
        off = True
        paths = os.listdir(path_source)
        for path in paths:
            source_folder = f'{path_source}\\{path}'
            list_dir = os.listdir(source_folder)

            if list_dir == []: continue

            for pathz in list_dir:
                if pathz.endswith('.txt'): break
            else:
                off = False
                items = list_dir
                for item in items:
                    source_item_path = os.path.join(source_folder, item)
                    destination_item_path = os.path.join(path_source, item)
                    shutil.move(source_item_path, destination_item_path)

        if off: break

    for path in os.listdir(path_source):
        source_folder = f'{path_source}\\{path}'
        if os.path.isdir(source_folder) and os.listdir(source_folder) == []:
            os.rmdir(source_folder)


def delete_structure(path_source: str):
    paths = []
    for root, dirs, files in os.walk(path_source):
        for file in files:
            if file.endswith('.txt'):  # Проверяем расширение файла
                file_path = os.path.join(root, file)
                if file_path in paths: continue
                log_name = root.split('\\')[1]
                shutil.move(file_path, f"{path_source}\\{log_name}_{file[:-4]}_{random.randint(10000, 99999)}.txt")
                paths.append(file_path)

    for path in os.listdir(path_source):
        if os.path.isdir(f'{path_source}\\{path}'): shutil.rmtree(f'{path_source}\\{path}')


def unrar_with_struct(archname:str, outfolder:str, path_to_unrar: str, passwords: list):
    files = len(get_struct(archname, path_to_unrar))
    files_unrar = 0
    true_passwords = []
    for pwd in passwords:
        cmdline = fr'{path_to_unrar} x -p{pwd} -r -ibck -o+ -y "{archname}" *.txt "{outfolder}"' #first_command full work

        #print(cmdline)
        x = subprocess.run(cmdline, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, universal_newlines=True, check=False)

        if 'Total errors: ' in x.stdout:
            total_unrar = files - int(x.stdout.split('Total errors: ')[-1].strip())
            files_unrar += total_unrar
            if files > files_unrar:
                if total_unrar < 1:
                    logger.opt(colors=True).info(f'<red>[{archname}] Неверный пароль [{pwd}]</red>')
                    continue
                logger.opt(colors=True).info(f'<green>[{archname}] Извлечено {files_unrar} из {files} файлов [password - {pwd}]</green>')
                true_passwords.append(pwd)
                continue

            else:
                true_passwords.append(pwd)
                logger.opt(colors=True).info(f'<green>[{archname}] Извлечено {files} из {files} файлов с паролями:</green>')
                logger.opt(colors=True).info(f'<green>[{archname}] passwords - {true_passwords}</green>')
                return

        logger.opt(colors=True).info(f'<green>[{archname}] Извлечено {files} из {files} файлов [password - {pwd}]</green>')
        break
    else:
        logger.info(f'[{archname}] Извлечено {files_unrar} из {files}')
        if len(true_passwords) > 0:
            logger.info(f'[{archname}] Валидные пароли: {true_passwords}')


def main():
    # получаем путь к архиву
    if len(sys.argv) > 1:
        archive = sys.argv[1]
    else:
        archive = input('Путь к папке с архивом(ами): ')
    if not os.path.exists(archive):
        print(f'Путь к папке с архивом(ами): {archive} не найден!')
        input('Программа завершена')
        exit()

    # получаем пароли если они нужны
    brute_pass = input('Подбирать пароль? (y/n): ').lower()

    if brute_pass == 'y':
        path_pwds = input('Введите путь до текстовика с паролями (можно без .txt): ')
        if path_pwds[-4:] != '.txt': path_pwds += '.txt'
        if not os.path.exists(path_pwds):
            print(f'Текстовик с паролями по пути: {archive} не найден!')
            input('Программа завершена')
            exit()

    # нужна ли нам струтура папок
    mode = input('Оставлять структуру папок? (y/n): ').lower()

    # куда сохраним наши логи
    path_save = input('Введите название папки куда сохранять результат(по умолчанию all_txt): ')
    if path_save == '': path_save = 'all_txt'

    # проверка содержимого и если есть удалить его
    if os.path.exists(path_save):
        if len(os.listdir(path_save)) > 0:
            del_dir = input(f'Удалить содержимое папки {path_save}? (y/n): ').lower()
            if del_dir == 'y':
                print('Удаляю содержимое папки')
                while os.path.exists(path_save):
                    try:
                        shutil.rmtree(path_save)
                    except:
                        pass
                os.mkdir(path_save)
                print('Удаление завершено')
    else:
        os.mkdir(path_save)

    # извлекам архив
    if brute_pass == 'y': pwds = [pwd.strip() for pwd in open(path_pwds, 'r', encoding='utf-8').readlines()]
    else: pwds = ['0']

    for archivez in os.listdir(archive):
        unrar_with_struct(archname=f'{archive}\\{archivez}', outfolder=path_save, path_to_unrar=path_to_unrar, passwords=pwds)
    delete_subfolder(path_save) # удаляет лишние подпапки
    if mode == 'n':
        delete_structure(path_save)


if __name__ == "__main__":
    main()