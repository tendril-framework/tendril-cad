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

"""
Manual CAD Material Schema
---------------------------
"""

from decimal import Decimal
from tendril.schema.base import SchemaControlledYamlFile


class ManualCADMaterialFileSchema(SchemaControlledYamlFile):
    supports_schema_name = 'ManualCADMaterialFile'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')

    def __init__(self, path, *args, **kwargs):
        super(ManualCADMaterialFileSchema, self).__init__(path, *args, **kwargs)

    def _stub_content(self):
        c = super(ManualCADMaterialFileSchema, self)._stub_content()
        c.update({
            'names': [],
            'description': '',
            'status': ''
        })
        return c

    def elements(self):
        e = super(ManualCADMaterialFileSchema, self).elements()
        e.update({
            'name':              self._p('name',        required=False),
            'description':       self._p('description', required=False),
            'status':            self._p('status',      required=False),
        })
        return e


def load(manager):
    manager.load_schema('ManualCADMaterialFileSchema', ManualCADMaterialFileSchema,
                        doc="Schema for Tendril Manual CAD Material Files")
