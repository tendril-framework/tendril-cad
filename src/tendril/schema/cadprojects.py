#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
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
EDA Project Configuration Schema Stub
-------------------------------------
"""

from decimal import Decimal

from tendril.validation.base import ValidationError
from tendril.validation.configs import ConfigOptionPolicy
from tendril.conventions.status import Status

from tendril.schema.base import NakedSchemaObject
from tendril.schema.projects.config import ProjectConfig


class CADProjectConfig(ProjectConfig):
    supports_schema_name = 'CADProjectConfig'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')

    def elements(self):
        e = super(CADProjectConfig, self).elements()
        e.update({
        })
        return e

    def validate(self):
        super(CADProjectConfig, self).validate()


def load(manager):
    manager.load_schema('CADProjectCOnfig', CADProjectConfig,
                        doc="Schema for Tendril CAD Project Definitions")
