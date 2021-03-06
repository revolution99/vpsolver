"""
This code is part of the Arc-flow Vector Packing Solver (VPSolver).

Copyright (C) 2013-2015, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from .base import CmdBase
from ..vpsolver import VBP
from .. import pymplutils


class CmdLoadVBP(CmdBase):
    """Command for loading VBP instances."""

    def _evalcmd(self, name, fname, i0=0, d0=0):
        """Evalutates CMD[name](*args)."""
        name, index = pymplutils.parse_indexed(name, "{}")
        index_I = "{0}_I".format(name)
        index_D = "{0}_D".format(name)
        if index is not None:
            assert 1 <= len(index) <= 2
            if len(index) == 2:
                index_I, index_D = index
            elif len(index) == 1:
                index_I = index[0]

        instance = VBP.from_file(fname, verbose=False)

        W = {
            i0+i: instance.W[i]
            for i in xrange(instance.ndims)
        }
        w = {
            (i0+i, d0+d): instance.w[i][d]
            for i in xrange(instance.m)
            for d in xrange(instance.ndims)
        }
        b = {
            i0+i: instance.b[i]
            for i in xrange(instance.m)
        }

        assert "_{0}".format(name.lstrip("^")) not in self._pyvars
        self._pyvars["_{0}".format(name.lstrip("^"))] = instance
        sets, params = self._sets, self._params

        self._defs += "#BEGIN_DEFS: Instance[{0}]\n".format(name)
        self._data += "#BEGIN_DATA: Instance[{0}]\n".format(name)
        defs, data = pymplutils.ampl_param(
            "{0}_m".format(name), None, instance.m, sets, params
        )
        self._defs += defs
        self._data += data
        defs, data = pymplutils.ampl_param(
            "{0}_n".format(name), None, sum(instance.b), sets, params
        )
        self._defs += defs
        self._data += data
        defs, data = pymplutils.ampl_param(
            "{0}_p".format(name), None, instance.ndims, sets, params
        )
        self._defs += defs
        self._data += data
        defs, data = pymplutils.ampl_set(
            index_I, range(i0, i0+instance.m), sets, sets
        )
        self._defs += defs
        self._data += data
        defs, data = pymplutils.ampl_set(
            index_D, range(d0, d0+instance.ndims), sets, params
        )
        self._defs += defs
        self._data += data
        defs, data = pymplutils.ampl_param(
            "{0}_W".format(name), index_D, W, sets, params
        )
        self._defs += defs
        self._data += data
        defs, data = pymplutils.ampl_param(
            "{0}_b".format(name), index_I, b, sets, params
        )
        self._defs += defs
        self._data += data
        defs, data = pymplutils.ampl_param(
            "{0}_w".format(name),
            "{0},{1}".format(index_I, index_D),
            w, sets, params
        )
        self._defs += defs
        self._data += data
        self._defs += "#END_DEFS: Instance[{0}]\n".format(name)
        self._data += "#END_DATA: Instance[{0}]\n".format(name)
