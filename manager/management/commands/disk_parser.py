from subprocess import run, PIPE
from django.core.management import BaseCommand
from manager.models import Disk


def disk_parser(disks):
    """
    Парсит диски в системе по названию и сохраняет их в 
    список словарей.
    """
    cmd = ['lsblk -o NAME,SIZE,MOUNTPOINT']
    output = run(cmd, shell=True, stdout=PIPE)
    
    output_string = output.stdout.decode('Utf-8')
    output_list = output_string.split('\n')
    output_list.pop(len(output_list)-1)

    disks_set = set(disks.split(','))
    output_dict = dict([i.split(' ', maxsplit=1) for i in output_list])
    output_dict = {k:v.strip().split() for k,v in output_dict.items() \
            if k in disks_set}

    if len(disks_set) != len(output_dict):
        return f'Пожалуйста введите правильные имена дисков.Вы ввели: {disks}.'

    data_list = []

    for key,value in output_dict.items():
        if len(value) == 1:
            data_list.append({
                'name': key,
                'size': int(value[0][0:-1]),
                'mount_point': None,
                'mount_state': 'umount'})
        else:
            data_list.append({
                'name': key,
                'size': int(value[0][0:-1]),
                'mount_point': value[1],
                'mount_state': 'mount'})

    return data_list


def saved_disks(data_list):
    """Чистит базу и cохраняет список словарей дисков в базу данных"""
    Disk.objects.all().delete()
    obj = [Disk(**data) for data in data_list]
    Disk.objects.bulk_create(obj)
    print('Данные дисков успешно сохранены')


class Command(BaseCommand):
    help = 'Запуск парсера дисков'

    def add_arguments(self, parser):
        parser.add_argument('disks', type=str)

    def handle(self, *args, **options):
        data = disk_parser(options['disks'])
        saved_disks(data)
        
