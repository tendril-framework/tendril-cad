

import os
import csv

from tendril.validation.base import ValidatableBase
from tendril.entities.materials.base import MaterialsBase
from tendril.utils.fsutils import VersionedOutputFile

from tendril.config import AUDIT_PATH


class MaterialNotFound(Exception):
    pass


class MaterialLibraryBase(ValidatableBase):
    _material_class = MaterialsBase
    _exc_class = MaterialNotFound

    def __init__(self, path, recursive=True, **kwargs):
        super(MaterialLibraryBase, self).__init__(**kwargs)
        self.path = path
        self._recursive = recursive

        self.materials = []
        self.index = {}
        self.regenerate()

    def get_folder_materials(self, path=None, **kwargs):
        return self.__class__(path, **kwargs)

    def _load_library(self):
        raise NotImplementedError

    def _generate_index(self):
        self.index = {}
        for material in self.materials:
            ident = material.ident_generic
            if ident in self.index.keys():
                self.index[ident].append(material)
            else:
                self.index[ident] = [material]

    def regenerate(self):
        self.materials = []
        self.index = {}

        self._load_library()
        self._generate_index()

    @property
    def idents(self):
        return self.index.keys()

    def is_recognized(self, ident):
        if ident in self.idents:
            return True
        return False

    def get_material(self, ident, get_all=False):
        if not ident.strip():
            raise self._exc_class("Ident cannot be left blank")

        if self.is_recognized(ident):
            if not get_all:
                return self.index[ident][0]
            else:
                return self.index[ident]

        raise self._exc_class('Material {0} not found in {1}'
                              ''.format(ident, self.name))

    def get_material_folder(self, ident):
        symfolder = os.path.split(self.get_material(ident).gpath)[0]
        return os.path.relpath(symfolder, self.path)

    def get_latest_materials(self, n=10, include_virtual=False):
        if include_virtual is False:
            tlib = (x for x in self.symbols if x.is_virtual is False)
        else:
            tlib = self.symbols
        return sorted(tlib, key=lambda y: y.last_updated, reverse=True)[:n]

    def export_audit(self, name):
        auditfname = os.path.join(
            AUDIT_PATH, 'materialslib-{0}.audit.csv'.format(name)
        )
        outf = VersionedOutputFile(auditfname)
        outw = csv.writer(outf)
        outw.writerow(['filename', 'status', 'ident', 'description', 'path'])
        for material in self.materials:
            outw.writerow(
                [material.gname, material.status, material.ident,
                 material.description, material.gpath]
            )
        outf.close()

    def _validate(self):
        pass


def load(manager):
    manager.install_exc_class('MaterialNotFound', MaterialNotFound)
