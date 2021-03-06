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

from .utils import linear_constraint
from .modelutils import write_lp
from .modelutils import write_mps
from .modelutils import write_mod

inf = float("inf")


class Model(object):
    """Class for creating models."""

    def __init__(self):
        self.vars = {}
        self.cons = {}
        self.vars_list = []
        self.cons_list = []
        self.obj = []
        self.objdir = "min"

    def set_obj(self, objdir, lincomb):
        """Set model objective."""
        assert objdir in ["min", "max"]
        self.objdir = objdir
        for var, coef in lincomb:
            assert var in self.vars
            assert coef != inf and coef != -inf
        self.obj = lincomb

    def new_con_name(self):
        """Generate a new constraint name."""
        name = "RC{0:x}".format(len(self.cons))
        assert name not in self.cons
        return name

    def new_var_name(self):
        """Generate a new variable name."""
        name = "RV{0:x}".format(len(self.vars))
        assert name not in self.vars
        return name

    def add_var(self, lb=None, ub=None, name=None, vtype="C"):
        """Add a new variable to the model."""
        if name is None:
            name = self.new_var_name()
        if lb == -inf:
            lb = None
        if ub == inf:
            ub = None
        assert name not in self.vars
        assert vtype in ["C", "I"]
        self.vars_list.append(name)
        self.vars[name] = {}
        self.vars[name]["lb"] = lb
        self.vars[name]["ub"] = ub
        self.vars[name]["vtype"] = vtype
        return name

    def add_con(self, left, sign, right, name=None):
        """Add a new constraint to the model."""
        sign = sign[:1]
        assert sign in ("<", "=", ">")
        lincomb, sign, rhs = linear_constraint(left, sign, right)
        assert rhs != inf and rhs != -inf
        if lincomb == []:
            return
        if name is None:
            name = self.new_con_name()
        for var, coef in lincomb:
            assert var in self.vars
            assert coef != inf and coef != -inf
        assert name not in self.cons
        self.cons_list.append(name)
        self.cons[name] = (lincomb, sign, rhs)

    def write_lp(self, lp_file):
        """Write the model to a file in LP format."""
        write_lp(self, lp_file)

    def write_mps(self, mps_file):
        """Write the model to a file in MPS format."""
        write_mps(self, mps_file)

    def write_mod(self, mod_file):
        """Write the model to a file in AMPL format."""
        write_mod(self, mod_file)

    def write(self, model_file):
        """Write the model to a file."""
        if model_file.endswith(".lp"):
            self.write_lp(model_file)
        elif model_file.endswith(".mps"):
            self.write_mps(model_file)
        elif model_file.endswith(".mod"):
            self.write_mod(model_file)
        else:
            raise Exception("Invalid file extension!")
