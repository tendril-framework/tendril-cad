

from tendril.schema import ManualCADMaterialFileSchema
from .base import MaterialsBase


class ManualCADMaterial(MaterialsBase):
    def __init__(self, path, vctx=None):
        super(ManualCADMaterial, self).__init__(vctx=vctx)
        self._load_definition(path)

    def _load_definition(self, path):
        data = ManualCADMaterialFileSchema(path)
        self.validation_errors.add(data.validation_errors)
        self._base_name = data.name
        self._description = data.description
        if data.status:
            self.status = data.status
        else:
            self.status = "Active"

    def _ident_constructor(self, generic=False):
        return self._base_name
