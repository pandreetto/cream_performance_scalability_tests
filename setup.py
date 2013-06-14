#!/usr/bin/env python

import sys, os, os.path, shlex, subprocess
from subprocess import Popen as execScript
from distutils.core import setup
from distutils.command.bdist_rpm import bdist_rpm as _bdist_rpm

pkg_name = 'glite-ce-cream-perf-tests'
pkg_version = '1.1.0'
pkg_release = '1'

source_items = "setup.py bin lib config share"

class bdist_rpm(_bdist_rpm):

    def run(self):

        topdir = os.path.join(os.getcwd(), self.bdist_base, 'rpmbuild')
        builddir = os.path.join(topdir, 'BUILD')
        srcdir = os.path.join(topdir, 'SOURCES')
        specdir = os.path.join(topdir, 'SPECS')
        rpmdir = os.path.join(topdir, 'RPMS')
        srpmdir = os.path.join(topdir, 'SRPMS')
        
        cmdline = "mkdir -p %s %s %s %s %s" % (builddir, srcdir, specdir, rpmdir, srpmdir)
        execScript(shlex.split(cmdline)).communicate()
        
        cmdline = "tar -zcf %s %s" % (os.path.join(srcdir, pkg_name + '.tar.gz'), source_items)
        execScript(shlex.split(cmdline)).communicate()
        
        specOut = open(os.path.join(specdir, pkg_name + '.spec'),'w')
        cmdline = "sed -e 's|@PKGVERSION@|%s|g' -e 's|@PKGRELEASE@|%s|g' project/%s.spec.in" % (pkg_version, pkg_release, pkg_name)
        execScript(shlex.split(cmdline), stdout=specOut, stderr=sys.stderr).communicate()
        specOut.close()
        
        cmdline = "rpmbuild -ba --define '_topdir %s' %s.spec" % (topdir, os.path.join(specdir, pkg_name))
        execScript(shlex.split(cmdline)).communicate()

exec_list= ['bin/cream-test-monitored-cancel',
            'bin/cream-test-monitored-lease-updated',  
            'bin/cream-test-monitored-submit',
            'bin/cream-test-notified-lease-expired',
            'bin/cream-test-notified-submit',
            'bin/cream-test-monitored-lease-expired',
            'bin/cream-test-monitored-proxy-expired',
            'bin/cream-test-notified-cancel',
            'bin/cream-test-notified-lease-updated']

manpage_list = ['share/man/man1/cream-test-monitored-cancel.1',
                'share/man/man1/cream-test-monitored-lease-updated.1',
                'share/man/man1/cream-test-monitored-submit.1',
                'share/man/man1/cream-test-notified-lease-expired.1',
                'share/man/man1/cream-test-notified-submit.1',
                'share/man/man1/cream-test-monitored-lease-expired.1',
                'share/man/man1/cream-test-monitored-proxy-expired.1',
                'share/man/man1/cream-test-notified-cancel.1',
                'share/man/man1/cream-test-notified-lease-updated.1']

config_list = ['config/logging.conf']

setup(
      name=pkg_name,
      version=pkg_version,
      description='Performace and scalability testsuite for gLite cream computing element',
      long_description='''The testsuite contains a set of executables
that can be used to analyze the performance of all the services installed on a CE''',
      license='Apache Software License',
      author='CREAM group',
      author_email='CREAM group <cream-support@lists.infn.it>',
      packages=['CREAMTestUtils'],
      package_dir = {'': 'lib/python'},
      data_files=[
                  ('usr/bin', exec_list),
                  ('usr/share/man/man1', manpage_list),
                  ('etc/' + pkg_name, config_list)
                 ],
      cmdclass={'bdist_rpm': bdist_rpm}
     )


