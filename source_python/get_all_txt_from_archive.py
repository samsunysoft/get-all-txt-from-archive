import os
import sys
import shutil
import subprocess
from time import sleep

import random

from loguru import logger

logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', enqueue=True)

# bundle_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(os.path.dirname(__file__))
#
# if sys.maxsize > 2 ** 32:
#     path_to_winrar = os.path.join(bundle_dir, "winz64\\winrar.exe")
#
# else:
#     path_to_winrar = os.path.join(bundle_dir, "winz32\\winrar.exe")
#
# path_to_unrar = f'"{path_to_winrar}"'


if sys.maxsize > 2**32:
    path_to_unrar = '"winz64\\winrar.exe"'

else:
    path_to_unrar = '"winz32\\winrar.exe"'


def delete_subfolder(path_source: str):
    for _ in range(6):
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
                    destination_item_path = os.path.join(path_source + str(random.randint(1,999)), item)
                    try:
                        shutil.move(source_item_path, destination_item_path)
                    except:
                        pass

        if off: break

    for path in os.listdir(path_source):
        source_folder = f'{path_source}\\{path}'
        if os.path.isdir(source_folder) and os.listdir(source_folder) == []:
            os.rmdir(source_folder)


def delete_structure(path_source: str):
    paths = []
    for root, dirs, files in os.walk(path_source):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                if file_path in paths: continue
                log_name = root.split('\\')[1]
                try:
                    shutil.move(file_path, f"{path_source}\\{log_name}_{file[:-4]}_{random.randint(10000, 99999)}.txt")
                except:
                    pass
                paths.append(file_path)

    for path in os.listdir(path_source):
        if os.path.isdir(f'{path_source}\\{path}'): shutil.rmtree(f'{path_source}\\{path}')


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def unrar_with_struct(archname: str, outfolder: str, path_to_unrar: str, passwords: list):
    try:
        archive_size = os.path.getsize(archname)
        folder_size_start = get_folder_size(outfolder)
        for pwd in ['zkzkzkzkz'] + passwords:
            cmdline = fr'{path_to_unrar} x -p{pwd} -r -ibck -o+ -y "{archname}" *.txt "{outfolder}"'
            x = subprocess.run(cmdline, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               universal_newlines=True, check=False)

            folder_size_new = get_folder_size(outfolder)
            if folder_size_new - folder_size_start >= archive_size * 0.3:
                logger.opt(colors=True).info(
                    f'<green>[{archname}] Успешно извлечён [пароль - {"нет" if pwd == "zkzkzkzkz" else pwd}]</green>')
                break

            #elif folder_size_new - folder_size_start <= archive_size * 0.1:
            else:
                logger.opt(colors=True).info(f'<red>[{archname}] Неверный пароль [{pwd}]</red>')

        else:
            if folder_size_new - folder_size_start > archive_size * 0.1:
                logger.opt(colors=True).info(f'<red>[{archname}] Извлечён не полностью</red>')
            else:
                logger.opt(colors=True).info(f'<red>[{archname}] Не удалось сбрутить</red>')
    except Exception as e:
        logger.exception(e)


def main():
    # получаем путь к архиву
    print("Developer - Samusuny [zelenka.guru/samsuny/, telegram @Toxenskiy]")
    if len(sys.argv) > 1:
        archive = sys.argv[1]
    else:
        archive = input('Путь к папке с архивом(ами): ')
    if not os.path.exists(archive):
        print(f'Путь к папке с архивом(ами): {archive} не найден!')
        input('Программа завершена')
        exit()

    # нужен ли брутфорс
    brute_pass = input('Подбирать пароль? (y/n): ').lower()

    # получаем пароли если они нужны
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
    if brute_pass == 'y':
        pwds = [pwd.strip() for pwd in open(path_pwds, 'r', encoding='utf-8').readlines()]
    else:
        pwds = []
    zxc = input('Вы уверены, что указали параметры правильно? Если да, то нажмите ENTER')
    os.system('cls')
    for archivez in os.listdir(archive):
        logger.info(f'Извлекаем {archivez}...')
        unrar_with_struct(archname=f'{archive}\\{archivez}', outfolder=path_save, path_to_unrar=path_to_unrar,
                          passwords=pwds)
        delete_subfolder(path_save)
        sleep(4)
        if mode == 'n':
            delete_structure(path_save)


if __name__ == "__main__":
    os.system('title ' + 'Developer - Samusuny [zelenka.guru/samsuny/, telegram @Toxenskiy]')
    main()
