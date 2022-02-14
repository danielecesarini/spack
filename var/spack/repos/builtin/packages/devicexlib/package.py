# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Devicexlib(AutotoolsPackage, CudaPackage):
    """Library wrapping device-oriented routines and utilities"""

    homepage = "https://gitlab.com/max-centre/components/devicexlib"
    url      = "https://gitlab.com/max-centre/components/devicexlib/-/archive/0.2.0/devicexlib-0.2.0.tar.gz"
    git      = "https://gitlab.com/max-centre/components/devicexlib.git"

    # Current
    version('0.2.0', sha256='286ed38871f9b6766b7fa42f79220b5b8840a928db91faf11d9d2ae5e089b000')
    version('0.1.0', sha256='5b2beab4cf3a863751a14eca8bfccc0cb4bf4bb36e7758ea57e8986064841240')

    depends_on('blas')
    depends_on('lapack')

    phases = ['configure', 'build', 'install']

    def build(self, spec, prefix):
        make('core')

#    def build(self, spec, prefix):
#        make('install')