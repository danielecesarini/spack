# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# Author: Daniele Cesarini <d.cesarini AT cineca.it>
# Date: May 12, 2020
# ----------------------------------------------------------------------------

from spack import *
import os

class Nemo(MakefilePackage):
    """NEMO (Nucleus for European Modelling of the Ocean) is a state-of-the-art
    modelling framework of ocean related engines for oceanographic research,
    operational oceanography, seasonal forecast and [paleo]climate studies."""

    nemo_arch_file = './arch/arch-SPACK.fcm'
    nemo_options = []

    homepage = 'http://forge.ipsl.jussieu.fr/nemo/wiki/Users'
    maintainers = ['danielecesarini']

    version('4.0',
            svn='https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/releases/release-4.0')
    version('4.0.1',
            svn='https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/releases/release-4.0.1')
    version('4.0.2',
            svn='https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/releases/r4.0/r4.0.2')
    version('4.0.3',
            svn='https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/releases/r4.0/r4.0.3')
    version('4.0.4',
            svn='https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/releases/r4.0/r4.0.4')

    ref_conf = ('AGRIF_DEMO', 
                'AMM12', 
                'C1D_PAPA',
                'GYRE_BFM',
                'GYRE_PISCES',
                'ORCA2_ICE_PISCES',
                'ORCA2_OFF_PISCES',
                'ORCA2_OFF_TRC',
                'ORCA2_SAS_ICE',
                'SPITZ12')

    keys = ('key_agrif',
            'key_asminc',
            'key_c1d',
            'key_cice',
            'key_cice4',
            'key_cyclone',
            'key_diahth',
            'key_diainstant',
            'key_iomput',
            'key_mpi2',
            'key_mpp_mpi',
            'key_nemocice_decomp',
            'key_netcdf4',
            'key_nosignedzero',
            'key_oa3mct_v1v2',
            'key_oasis3',
            'key_sed_off',
            'key_si3',
            'key_top',
            'key_trdmxl_trc',
            'key_trdtrc',
            'key_vectopt_loop')

    variant('ref_conf', 
        default='none',
        description=' Reference configurations',
        values=ref_conf,
        multi=False)

    variant('add_key', 
        default='none',
        description='Add CPP keys',
        values=keys,
        multi=True)

    variant('del_key', 
        default='none',
        description='Remove CPP keys',
        values=keys,
        multi=True)

    variant('debug', 
        default=False, 
        description='Enable debug build')

    conflicts('ref_conf=none', 
        msg='A value for reference configuration must be specified.')

    # Build dependencies
    depends_on('mpi')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    depends_on('hdf5+hl')
    depends_on('xios')

    def nemo_fcm(self):
        spec = self.spec
        param = dict()
        param['NETCDF_C_INC_DIR'] = spec['netcdf-c'].prefix.include
        param['NETCDF_C_LIB_DIR'] = spec['netcdf-c'].prefix.lib
        param['NETCDF_FORTRAN_INC_DIR'] = spec['netcdf-fortran'].prefix.include
        param['NETCDF_FORTRAN_LIB_DIR'] = spec['netcdf-fortran'].prefix.lib
        param['HDF5_INC'] = spec['hdf5'].prefix.include
        param['HDF5_LIB'] = spec['hdf5'].prefix.lib
        param['XIOS_INC_DIR'] = spec['xios'].prefix.include
        param['XIOS_LIB_DIR'] = spec['xios'].prefix.lib
        param['MPIFC'] = spec['mpi'].mpifc
        param['MPICC'] = spec['mpi'].mpicc

        libs = r"""
%NCDF_INC       -I{NETCDF_C_INC_DIR} -I{NETCDF_FORTRAN_INC_DIR}
%NCDF_LIB       -L{NETCDF_C_LIB_DIR} -L{NETCDF_FORTRAN_LIB_DIR} -lnetcdff -lnetcdf
%HDF5_INC       -I{HDF5_INC}
%HDF5_LIB       -L{HDF5_LIB} -lhdf5_hl -lhdf5
%XIOS_INC       -I{XIOS_INC_DIR}
%XIOS_LIB       -L{XIOS_LIB_DIR} -lxios -lstdc++
%OASIS_INC      
%OASIS_LIB  
%USER_INC       %XIOS_INC %OASIS_INC %NCDF_INC
%USER_LIB       %XIOS_LIB %OASIS_LIB %NCDF_LIB

%CPP	        cpp -Dkey_nosignedzero
%FC             {MPIFC} -c -cpp
%FPPFLAGS       -P -C -traditional -std=c11
%CC             {MPICC}
%LD             {MPIFC}

%AR             ar
%ARFLAGS        rs
%MK             make
""".format(**param)

        param = dict()
        param['FFLAGS'] = []
        param['CFLAGS'] = []
        param['LDFLAGS'] = []

        if spec.satisfies('%gcc'):
            if '+debug' in spec:
                param['FFLAGS'].extend([
                    '-g', '-O0',
                    '-fdefault-real-8',
                    '-fcray-pointer',
                    '-ffree-line-length-none'])
                param['CFLAGS'].extend([
                    '-g', '-O0'])
            else:
                param['FFLAGS'].extend([
                    '-g', '-O3',
                    '-fdefault-real-8', 
                    '-fcray-pointer', 
                    '-ffree-line-length-none',
                    '-funroll-all-loops'])
                param['CFLAGS'].extend([
                    '-g', '-O3', 
                    '-funroll-all-loops'])
        elif spec.satisfies('%intel'):
            if '+debug' in spec:
                param['FFLAGS'].extend([
                    '-g', '-O0',
                    '-r8',
                    '-fp-model source', 
                    '-traceback'])
                param['CFLAGS'].extend([
                    '-g', '-O0'])
            else:
                param['FFLAGS'].extend([
                    '-g', '-O3',
                    '-r8',
                    '-fp-model source', 
                    '-traceback',
                    '-qopt-zmm-usage=high'])
                param['CFLAGS'].extend([
                    '-g', '-O3'])
        elif spec.satisfies('%pgi'):
            if '+debug' in spec:
                param['FFLAGS'].extend([
                    '-g', '-O0',
                    '-i4', 
                    '-r8'])
                param['CFLAGS'].extend([
                    '-g', '-O0'])
            else:
                param['FFLAGS'].extend([
                    '-g', '-O3',
                    '-fast',
                    '-i4', 
                    '-r8'])
                param['CFLAGS'].extend([
                    '-g', '-O3',
                    '-fast'])
        elif spec.satisfies('%cce'):
            if '+debug' in spec:
                param['FFLAGS'].extend([
                    '-g', '-O0',
                    '-em',
                    '-s integer32',
                    '-s real64'])
                param['CFLAGS'].extend([
                    '-g', '-O0',
                    '-em',
                    '-s integer32',
                    '-s real64'])
            else:
                param['FFLAGS'].extend([
                    '-g', '-O3',
                    '-em',
                    '-s integer32',
                    '-s real64'])
                param['CFLAGS'].extend([
                    '-g', '-O3',
                    '-em',
                    '-s integer32',
                    '-s real64'])
        elif spec.satisfies('%xl'):
            if '+debug' in spec:
                param['FFLAGS'].extend([
                    '-g', '-O0',
                    '-qrealsize=8',
                    '-qextname',
                    '-qsuffix=f=f90',
                    '-qsuffix=cpp=F90',
                    '-qstrict',
                    '-qfree=f90'])
                param['CFLAGS'].extend([
                    '-g', '-O0',
                    '-qcpluscmt'])
            else:
                param['FFLAGS'].extend([
                    '-g', '-O3',
                    '-qrealsize=8',
                    '-qextname',
                    '-qsuffix=f=f90',
                    '-qsuffix=cpp=F90',
                    '-qstrict',
                    '-qfree=f90'])
                param['CFLAGS'].extend([
                    '-g', '-O3',
                    '-qcpluscmt'])

        param['FFLAGS'] = ' '.join(param['FFLAGS'])
        param['CFLAGS'] = ' '.join(param['CFLAGS'])
        param['LDFLAGS'] = ' '.join(param['LDFLAGS'])

        compilers = r"""
%FCFLAGS        {FFLAGS}
%FFLAGS         %FCFLAGS
%CFLAGS         {CFLAGS}
%LDFLAGS        {LDFLAGS}
                    """.format(**param)

        with open(self.nemo_arch_file, 'w') as f:
            f.write(libs+compilers)

    def edit(self, spec, prefix):
        # Configure architecture name
        options = ['-m', 'SPACK']

        # Add reference configuration
        ref_conf = self.spec.variants['ref_conf'].value
        options.extend(['-r', '%s' % ref_conf, '-n', 'SPACK-%s' % ref_conf])

        # Configure parallel build
        if self.parallel:
            options.extend([
                '-j', 
                str(make_jobs)])

        # Add/remove CPP keys
        if(self.spec.variants['add_key'].value[0] != 'none'):
            options.extend([
                'add_key', 
                '%s' % ' '.join(self.spec.variants['add_key'].value)])
        if(self.spec.variants['del_key'].value[0] != 'none'):
            options.extend([
                'del_key', 
                '%s' % ' '.join(self.spec.variants['del_key'].value)])

        # Append to global
        self.nemo_options = options

        # Create arch file
        self.nemo_fcm()

    def build(self, spec, prefix):
        make_nemo = Executable('./makenemo')
        make_nemo(*self.nemo_options)

    def install(self, spec, prefix):
        mkdirp(spec.prefix)
        mkdirp(spec.prefix.bin)

        ref_conf = self.spec.variants['ref_conf'].value
        exp00 = spec.prefix + '/cfgs/%s/EXP00' % ref_conf

        install('cfgs/SPACK-%s/BLD/bin/nemo.exe' % ref_conf, 
            spec.prefix.bin + '/nemo.exe')
        install_tree('cfgs/SPACK-%s/BLD' % ref_conf,
            spec.prefix + '/cfgs/%s/BLD' % ref_conf)
        install_tree('cfgs/SPACK-%s/EXP00' % ref_conf,
            spec.prefix + '/cfgs/%s/EXP00' % ref_conf)
        install_tree('cfgs/SPACK-%s/MY_SRC' % ref_conf,
            spec.prefix + '/cfgs/%s/MY_SRC' % ref_conf)
        install_tree('cfgs/SPACK-%s/WORK' % ref_conf,
            spec.prefix + '/cfgs/%s/WORK' % ref_conf, symlinks=False)
        install_tree('cfgs/SHARED', 
            spec.prefix + '/cfgs/SHARED')
        install('cfgs/SPACK-%s/cpp_SPACK-%s.fcm' % (ref_conf, ref_conf), 
            spec.prefix + '/cfgs/%s' % ref_conf)

        # Change symbolic link from build to install directory
        os.chdir(exp00)
        os.unlink('nemo')
        os.symlink('../../../bin/nemo.exe', 'nemo')
