

from tendril.conventions.status import get_status
from tendril.conventions.status import Status

from tendril.validation.base import ValidatableBase


class MaterialsBase(ValidatableBase):
    def __init__(self, vctx=None):
        super(MaterialsBase, self).__init__(vctx)
        self._base_name = None
        self._status = None
        self._description = None

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, Status):
            self._status = get_status(value)
        else:
            self._status = value

    @property
    def ident(self):
        return self._ident_constructor(generic=False)

    @property
    def ident_generic(self):
        return self._ident_constructor(generic=True)

    def _ident_constructor(self, generic=False):
        raise NotImplementedError

    def _validate(self):
        pass

    # Status
    @property
    def is_virtual(self):
        if self.status == 'Virtual':
            return True
        return False

    @property
    def is_deprecated(self):
        if self.status == 'Deprecated':
            return True
        return False

    @property
    def is_experimental(self):
        if self.status == 'Experimental':
            return True
        return False

    @is_virtual.setter
    def is_virtual(self, value):
        if self.status == 'Generator':
            if value is True:
                self.status = 'Virtual'
        else:
            raise AttributeError

    def __repr__(self):
        return '{0:40}'.format(self.ident)
