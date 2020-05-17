import xml.etree.ElementTree as ET


class BoxOVF:
    namespaces = {
        'ovf': 'http://schemas.dmtf.org/ovf/envelope/1',
        'vbox': "http://www.virtualbox.org/ovf/machine",
    }

    def __init__(self, content):
        """
        :param str content: OVF ファイルの内容
        """
        self.content = content

    @property
    def xmlroot(self):
        try:
            return self._xmlroot
        except AttributeError:
            self._xmlroot = ET.fromstring(self.content)
            return self._xmlroot

    # ovf:File の attr names
    attr_id = '{{{ovf}}}id'.format(**namespaces)
    attr_href = '{{{ovf}}}href'.format(**namespaces)

    def get_filemap(self):
        refs = self.xmlroot.findall('./ovf:References/ovf:File', self.namespaces)
        return {item.get(self.attr_id): item.get(self.attr_href) for item in refs}

    # ovf:Disk の attr names
    attr_disk_file_ref = '{{{ovf}}}fileRef'.format(**namespaces)
    attr_disk_id = '{{{ovf}}}diskId'.format(**namespaces)
    attr_disk_capacity = '{{{ovf}}}capacity'.format(**namespaces)
    attr_disk_uuid = '{{{vbox}}}uuid'.format(**namespaces)

    def iter_disk(self):
        filemap = self.get_filemap()
        disks = self.xmlroot.findall('./ovf:DiskSection/ovf:Disk', self.namespaces)
        for disk in disks:
            file_ref = disk.attrib.get(self.attr_disk_file_ref)
            yield {
                'disk_id': disk.attrib.get(self.attr_disk_id),
                'file_ref': file_ref,
                'href': filemap.get(file_ref),
            }
