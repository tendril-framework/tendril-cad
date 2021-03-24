#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2021 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import inspect
from glob import glob
from jinja2 import Template

from tendril.entities.materials.cad import ManualCADMaterial

from tendril.libraries.materials.base import MaterialLibraryBase
from tendril.libraries.materials.base import MaterialNotFound

from tendril.config import CAD_MANUAL_MATERIALS_LIBRARY_PATH


template_path = os.path.normpath(os.path.join(
    inspect.getfile(inspect.currentframe()),
    os.pardir, os.pardir, os.pardir,
    'schema', 'templates', 'ManualCADMaterial.yaml')
)


class ManualCADMaterialNotFound(MaterialNotFound):
    pass


class ManualCADMaterialAlreadyExists(Exception):
    pass


class ManualCADMaterialLibrary(MaterialLibraryBase):
    _material_class = ManualCADMaterial
    _exc_class = ManualCADMaterialNotFound

    def __init__(self, *args, **kwargs):
        super(ManualCADMaterialLibrary, self).__init__(*args, **kwargs)

    def _load_material(self, path):
        material = ManualCADMaterial(path)
        self.materials.append(material)

    def _load_folder_materials(self, path):
        if not self._recursive:
            files = [f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))
                     and f.endswith('.yaml')]
        else:
            files = []
            for x in os.walk(path):
                for y in glob(os.path.join(x[0], '*.yaml')):
                    files.append(y)

        for f in files:
            self._load_material(os.path.join(path, f))

    def create_manual_entry(self, name, description, status=None):
        template = Template(open(template_path).read())
        stage = {
            'name': name,
            'description': description,
            'status': status or "Active",
            'schema_name': 'ManualCADMaterialFile',
            'schema_version': "1.0",
        }
        path = os.path.join(self.path, "{0}.yaml".format(name))
        if os.path.exists(path):
            raise ManualCADMaterialAlreadyExists(path)
        with open(path, 'w') as f:
            f.write(template.render(stage=stage))

    def _load_library(self):
        self._load_folder_materials(self.path)

    def regenerate(self):
        super(ManualCADMaterialLibrary, self).regenerate()


def load(manager):
    manual_library = ManualCADMaterialLibrary(CAD_MANUAL_MATERIALS_LIBRARY_PATH)
    manager.install_library('manual', manual_library)
    manager.install_exc_class('ManualCADMaterialNotFound', ManualCADMaterialNotFound)
