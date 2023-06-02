import os
import sys
import zipfile
import random
import shutil


def first_func(archive, path_save):
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if not os.path.isdir(info.filename):
                if info.filename[-4:] != '.txt': continue
                z.extract(info.filename, path=path_save)


def second_func(archive, path_save):
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():

            if not os.path.isdir(info.filename):
                if info.filename[-4:] != '.txt': continue
                file_name = info.orig_filename.split('/')
                file_name = f'{file_name[0]}_{file_name[-1][:-4]}_{random.randint(0, 99999)}.txt'

                open(f'{path_save}\\' + file_name, 'wb').write(z.read(info.filename))
                #z.extract(info.filename, path='all_txt')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        archive = sys.argv[1]
    else:
        archive = input('Введите путь до архива: ')
    if archive[-4:] != '.zip': archive += '.zip'
    if not os.path.exists(archive):
        print(f'Архив по пути: {archive} не найден!')
        input()
        exit()

    mode = input('Оставлять струтуру папок? (y/n): ').lower()

    path_save = input('Введите название папки куда сохранять результат(по умолчанию all_txt): ')
    if path_save == '': path_save = 'all_txt'

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

    if mode == 'y':
        first_func(archive, path_save)
    else:
        second_func(archive, path_save)

