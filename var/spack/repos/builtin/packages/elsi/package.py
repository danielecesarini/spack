# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Elsi(CMakePackage):
    """ELSI provides a unified interface for electronic structure
    codes to a variety of eigenvalue solvers."""

    homepage = "https://wordpress.elsi-interchange.org/"
    
    version('2.7.1', sha256='4a70b6047c39f4e0fd5eca1b2543bfa600acb8305a05ccaaf823ca045f8a4e4d',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2021/03/elsi-2.7.1.tar.gz')
    version('2.7.0', sha256='cac19128fe2626313676b37df47580b74c9d0e161513f9de40c052251c9d46ca',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2021/03/elsi-2.7.0.tar.gz')
    version('2.6.4', sha256='e43fc12b4954ecd70813fcb45aaef39779f7d9bb5270bbc7246e88d92c8b1dc4',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2020/11/elsi-2.6.4.tar.gz')
    version('2.6.3', sha256='6de3a9068f1788b096ab7141f7170d4ceac3dabe106dbadbc8e28a6d46ad2d9b',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2020/11/elsi-2.6.3.tar.gz')
    version('2.6.2', sha256='5b4b2e8fa4b3b68131fe02cc1803a884039b89a1b1138af474af66453bec0b4d',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2020/07/elsi-2.6.2.tar.gz')
    version('2.6.1', sha256='f4bf08bd0ebc7739f0eae94aa15243731a1718bf314817c32f649354a3de9ad5',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2020/06/elsi-2.6.1.tar.gz')
    version('2.6.0', sha256='abe147e3cbcf3624236b1439c49e18891fdeb66cfb59755302c67bd9c5755c3e',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2020/06/elsi-2.6.0.tar.gz')
    version('2.5.0', sha256='f4d77c4291341c9708ab8070dc4ec683577b3556e7d9f214370d626dc6a4753f',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2020/02/elsi-2.5.0.tar.gz')
    version('2.4.1', sha256='ba48074dd232f88f68e368c7742d7da53de94655b0c8aa9f8d71f0de1a91d39e',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2019/11/elsi-2.4.1.tar.gz')
    version('2.3.1', sha256='ba48074dd232f88f68e368c7742d7da53de94655b0c8aa9f8d71f0de1a91d39e',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2019/07/elsi-2.3.1.tar.gz')
    version('2.3.0', sha256='f2fad2a16c8e8c7f54f87753b34e2eecea074416251620268a7633272646ce92',
             url = 'http://wordpress.elsi-interchange.org/wp-content/uploads/2019/06/elsi-2.3.0.tar.gz')
    version('2.2.1', sha256='5b4b2e8fa4b3b68131fe02cc1803a884039b89a1b1138af474af66453bec0b4d',
             url = 'https://wordpress.elsi-interchange.org/wp-content/uploads/2019/03/elsi-2.2.1.tar.gz')

    # Variants (translation of cmake options)
    variant(
        'add_underscore', default=True,
        description="Suffix C functions with an underscore"
    )
    variant(
        'elpa2_kernel', default="none", description="ELPA2 Kernel",
        values=('none', 'AVX', 'AVX2', 'AVX512'), multi=False
    )
    variant(
        'enable_pexsi', default=False, description='Enable PEXSI support'
    )
    variant(
        'enable_sips', default=False, description='Enable SLEPc-SIPs support'
    )
    variant(
        'use_external_elpa', default=False,
        description="Build ELPA using SPACK"
    )
    variant(
        'use_external_ntpoly', default=False,
        description="Build NTPoly using SPACK"
    )
    variant(
        'use_external_omm', default=False,
        description="Use external libOMM and MatrixSwitch"
    )
    variant(
        'use_external_superlu', default=False,
        description="Use external SuperLU DIST"
    )
    variant(
        'use_mpi_iallgather', default=True,
        description="Use non-blocking collective MPI functions"
    )

    # Basic dependencies
    depends_on('blas', type="link")
    depends_on('lapack', type="link")
    depends_on('cmake', type="build")
    depends_on('mpi')
    depends_on('scalapack', type="link")

    # Library dependencies
    depends_on('elpa', when='+use_external_elpa')
    depends_on('ntpoly', when='+use_external_ntpoly')
    depends_on('slepc', when='+enable_sips')
    depends_on('petsc', when='+enable_sips')
    depends_on('superlu-dist', when='+use_external_superlu')

    def cmake_args(self):
        from os.path import dirname

        spec = self.spec
        args = []

        # Compiler Information
        # (ELSI wants these explicitly set)
        args += ["-DCMAKE_Fortran_COMPILER=" + self.spec["mpi"].mpifc]
        args += ["-DCMAKE_C_COMPILER=" + self.spec["mpi"].mpicc]
        args += ["-DCMAKE_CXX_COMPILER=" + self.spec["mpi"].mpicxx]

        # Handle the various variants
        if "-add_underscore" in self.spec:
            args += ["-DADD_UNDERSCORE=OFF"]
        if "elpa2_kernel" in self.spec.variants and \
                self.spec.variants["elpa2_kernel"].value != "none":
            kernel = self.spec.variants["elpa2_kernel"].value
            args += ["-DELPA2_KERNEL=" + kernel]
        if '+enable_pexsi' in self.spec:
            args += ["-DENABLE_PEXSI=ON"]
        if '+enable_sips' in self.spec:
            args += ["-DENABLE_SIPS=ON"]
        if '+use_external_elpa' in self.spec:
            args += ["-DUSE_EXTERNAL_ELPA=ON"]
            # Setup the searchpath for elpa
            elpa = self.spec['elpa']
            elpa_module = find(elpa.prefix, 'elpa.mod')
            args += ["-DINC_PATHS=" + dirname(elpa_module[0])]
        if '+use_external_ntpoly' in self.spec:
            args += ["-DUSE_EXTERNAL_NTPOLY=ON"]
        if '+use_external_omm' in self.spec:
            args += ["-DUSE_EXTERNAL_OMM=ON"]
        if '+use_external_superlu' in self.spec:
            args += ["-DUSE_EXTERNAL_SUPERLU=ON"]
        if '-use_mpi_iallgather' in self.spec:
            args += ["-DUSE_MPI_IALLGATHER=OFF"]

        # Only when using fujitsu compiler
        if spec.satisfies('%fj'):
            args += ["-DCMAKE_Fortran_MODDIR_FLAG=-M"]

        return args
