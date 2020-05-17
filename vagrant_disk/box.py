import os
import tarfile
from .boxovf import BoxOVF


class VagrantBoxReader:
    def __init__(self, name):
        """
        :param str name: vagrant box ファイルのパス
        """
        self.name = name


    def iter_disk(self):
        with tarfile.open(name=self.name, mode='r') as boxtar:
            boxitem = next((it for it in boxtar if os.path.basename(it.name) == 'box.ovf'), None)

            with boxtar.extractfile(boxitem) as fp:
                boxovf = BoxOVF(fp.read())

            for diskinfo in boxovf.iter_disk():
                yield VagrantBoxDisk(boxtar, **diskinfo)


class VagrantBoxDisk(dict):
    def __repr__(self):
        return '<{cls.__module__}.{cls.__name__} id="{self[disk_id]} href="{self[href]}">'.format(
            cls=self.__class__,
            self=self,
        )

    def __init__(self, boxtar, **kwargs):
        self._boxtar = boxtar
        self.update(**kwargs)

    def get_tarinfo(self):
        return next((it for it in self._boxtar if os.path.basename(it.name) == self['href']), None)

    def extractfile(self):
        tarinfo = self.get_tarinfo()
        return self._boxtar.extractfile(tarinfo)
