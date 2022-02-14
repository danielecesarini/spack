# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FoxF(AutotoolsPackage):
    """A Fortran XML library"""

    homepage = "https://github.com/pietrodelugas/fox"
    url      = "https://github.com/pietrodelugas/fox/archive/refs/tags/4.1.2.tar.gz"

    version('4.1.2-QE', sha256='e27e721ac5ce4d6dcfa47c62ed14c35731d211f04f6d9215e86b1c73ab6b9dab')
    version('4.1.2',    sha256='dea0adc9cc035238fa9cdba42f2bf56481e3a64ac8aa0aece9119f127f71d4e7')
    version('4.0.4',    sha256='1d917690d3a655fb320b14b10bd6408bf5ab80aa14dfbf1f600173c3469f5a1e')
