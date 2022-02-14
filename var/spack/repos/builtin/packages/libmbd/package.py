# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libmbd(CMakePackage):
    """Libmbd is a libraty that implements the many-body dispersion (MBD) 
       method in several programming languages and frameworks"""

    homepage = "https://github.com/libmbd/libmbd"
    url      = "https://github.com/libmbd/libmbd/archive/refs/tags/0.12.5.tar.gz"

    version('0.12.5', sha256='bd8ae8e388984171cc65275533ad25695db303248435237a9ed5f08dd6802ba3')

    variant('scalapack', default=False, description='Enable SCALAPACK')
    variant('elsi',      default=False, description='Enable ELSI')
    variant('c-api',     default=True,  description='Enable C API')

    depends_on('lapack')
    depends_on('elsi+shared', when='+elsi')
    depends_on('scalapack',   when='+elsi')
    depends_on('mpi',         when='+elsi')
    depends_on('scalapack',   when='+scalapack')
    depends_on('mpi',         when='+scalapack')

    patch('version.patch')

    def cmake_args(self):
        args = [
            "-DVERSION_TAG={0}".format(self.version),
            self.define_from_variant('ENABLE_C_API', 'c-api')
        ]

        if '+elsi' in self.spec:
            args.append("-DENABLE_SCALAPACK_MPI=ON")
            args.append("-DENABLE_ELSI=ON")
        elif '+scalapack' in self.spec:
            args.append("-DENABLE_SCALAPACK_MPI=ON")
        
        return args
