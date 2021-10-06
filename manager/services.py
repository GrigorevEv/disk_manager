from subprocess import run
from conf.settings import SUDO_STR
from .models import Disk


class DiskManager:
    """
    Класс для выполнения операций форматирования, монтирования
    и отмонтирования дисков.
    """

    def __init__(self, instance):
        self.instance = instance
        

    def formats_disk(self):
        """Метод форматирования диска."""
        cmd = SUDO_STR + f'mkfs -t ext4 /dev/{self.instance.name}'
        if self.instance.format:
            if self.instance.mount_state == 'mount':
                DiskManager.__disk_umount(self.instance)
                run(cmd, shell=True)
                DiskManager.__disk_mount(self.instance)
            else:
                run(cmd, shell=True)
            print(f'Диск {self.instance.name} успешно отформатирован')


    def mounts_or_umounts_disk(self):
        """Метод монтирования и отмонтирования диска."""
        if self.instance.mount_state == 'mount':
            DiskManager.__disk_mount(self.instance)
        else:
            DiskManager.__disk_umount(self.instance)


    def __disk_mount(inst):
        previous_mounted = Disk.objects.get(id=inst.id)
        DiskManager.__disk_umount(previous_mounted)

        cmd = SUDO_STR + f'mkdir -p {inst.mount_point} && ' + \
              SUDO_STR + f'mount /dev/{inst.name} {inst.mount_point}'

        run(cmd, shell=True)
        print(f'Диск {inst.name} успешно монтирован на {inst.mount_point}')
                

    def __disk_umount(inst):
        cmd = SUDO_STR + f'umount {inst.mount_point}'
        run(cmd, shell=True)
        print(f'Диск {inst.name} успешно отмонтирован от {inst.mount_point}')


