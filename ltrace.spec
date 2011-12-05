Summary: Tracks runtime library calls from dynamically linked executables
Name: ltrace
Version: 0.5
Release: 16.45svn.1%{?dist}
URL: http://ltrace.alioth.debian.org/
License: GPLv2+
Group: Development/Debuggers
ExclusiveArch: %{ix86} x86_64 ia64 ppc ppc64 s390 s390x alpha sparc
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: elfutils-libelf-devel dejagnu

# Tarball generated from svn checkout.  To regenerate:
# svn co svn://svn.debian.org/ltrace -r 45
# cd ltrace/ltrace/trunk && ./autogen.sh && ./configure && make dist
Source: ltrace-0.5-svn45.tar.gz

Patch0: ltrace-0.4-exec.patch
Patch1: ltrace-0.4-fork.patch
Patch2: ltrace-0.5-opd.patch
Patch3: ltrace-ppc32fc5.patch
Patch4: ltrace-0.5-gnuhash.patch
Patch5: ltrace-0.5-testsuite.patch
Patch6: ltrace-0.5-ppc-symval.patch
Patch7: ltrace-0.5-a2bp.patch
Patch8: ltrace-0.5-attach.patch
Patch9: ltrace-0.5-fork.patch
Patch10: ltrace-0.5-exec.patch
Patch11: ltrace-0.5-exec-tests.patch
Patch12: ltrace-0.5-man.patch
Patch13: ltrace-0.5-ia64-sigill.patch
Patch14: ltrace-0.5-build.patch
Patch15: ltrace-0.5-o.patch
Patch16: ltrace-0.5-s390-args.patch
Patch17: ltrace-0.5-fork-earlychild.patch
Patch18: ltrace-0.5-s390-31-on-64.patch
Patch19: ltrace-0.5-fork-ppc64.patch
Patch20: ltrace-0.5-exec-stripped.patch
Patch21: ltrace-0.5-ppc-plt-glink.patch

%description
Ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls called by the executed process
and the signals received by the executed process.  Ltrace can also
intercept and print system calls executed by the process.

You should install ltrace if you need a sysadmin tool for tracking the
execution of processes.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
sed -i -e 's/-o root -g root//' Makefile.in

%build
# This ugly hack is necessary to build and link files for correct
# architecture.  It makes a difference on ppc.
export CC="gcc`echo $RPM_OPT_FLAGS | sed -n 's/^.*\(-m[36][124]\).*$/ \1/p'` -D_LARGEFILE64_SOURCE"
%configure CC="$CC"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT bindir=%{_bindir} docdir=%{_docdir}/ltrace-%{version}/ install

# The testsuite is useful for development in real world, but fails in
# koji for some reason.  Disable it, but have it handy.
#%check
#echo ====================TESTING=========================
#make check
#echo ====================TESTING END=====================

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING README TODO BUGS ChangeLog
%{_bindir}/ltrace
%{_mandir}/man1/ltrace.1*
%config(noreplace) %{_sysconfdir}/ltrace.conf

%changelog
* Wed May 19 2010 Petr Machata <pmachata@redhat.com> - 0.5-16.45svn.1
- Support zero value of undefined symbols in PPC binaries.
- Resolves: #588338

* Wed Mar 31 2010 Petr Machata <pmachata@redhat.com> - 0.5-15.45svn.1
- Bring over patches from RHEL 5
- Fix a problem with tracing stripped binary after execl on
  architectures that need PLT reinitalisation breakpoint.
- Resolves: #528466

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.5-14.45svn.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-14.45svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-13.45svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct  7 2008 Petr Machata <pmachata@redhat.com> - 0.5-12.45svn
- Fix fork & exec patches to apply cleanly under --fuzz=0
- Resolves: #465036

* Fri May 23 2008 Petr Machata <pmachata@redhat.com> - 0.5-11.45svn
- Patch from James M. Leddy, fixes interaction of -c and -o
- Fix compilation by using -D_LARGEFILE64_SOURCE
- related: #447404

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5-10.45svn
- Autorebuild for GCC 4.3

* Wed Sep 12 2007 Petr Machata <pmachata@redhat.com> - 0.5-9.45svn
- Cleanup spec.
- Fix parallel make bug in Makefile.
- resolves: #226109

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 0.5-8.45svn
- Fix licensing tag.

* Fri May  4 2007 Petr Machata <pmachata@redhat.com> - 0.5-7.45svn
- added fork/exec patches, mostly IBM's work
- added trace-exec tests into suite
- added ia64 sigill patch

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 0.5-6.45svn
- tidy up the specfile per rpmlint comments
- fix man page

* Mon Sep  4 2006 Petr Machata <pmachata@redhat.com> - 0.5-5.45svn
- fix plt handling on ppc32 (symval patch)
- fix attaching to process (attach patch)
- add fork & exec patches from IBM
- adjust weak symbol handling (ppc32fc5 patch)

* Wed Aug 23 2006 Petr Machata <pmachata@redhat.com> - 0.5-3.45svn
- use "{X}.{release}svn" release string per naming guidelines

* Tue Aug 22 2006 Petr Machata <pmachata@redhat.com> - 0.5-1.1.45svn
- using dist tag

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 0.5-1.0.45svn.6
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Fri Jul 14 2006 Petr Machata <pmachata@redhat.com> - 0.5-1.0.45svn.5
- adding .gnu.hash patch to support new ELF hash table section
- adding testsuite patch to silent some bogus failures

* Fri Jul 14 2006 Petr Machata <pmachata@redhat.com> - 0.5-1.0.45svn
- adding upstream (svn) version.  It contains most of patches that we
  already use, and has support for secure PLTs.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.4-1.7.1
- rebuild

* Wed Jun 14 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.7
- drop broken ppc support

* Thu Jun  1 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.6
- e_entry patch: use elf's e_entry field instead of looking up _start
  symbol, which failed on stripped binaries.

* Tue May  3 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.5
- Correct a typo that prevented the inclusion of "demangle.h"
- Adding -Wl,-z,relro

* Mon Apr 24 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.4
- turn off opd translation on ia64, GElf already gives us function
  address.
- turn on main-internal test, it should pass now.

* Wed Apr 12 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.2
- svn fix for opt_x patch
- patches for testsuite for s390{,x}
- turning off main-internal test. Fails on ia64, needs investigation.

* Fri Apr  7 2006 Petr Machata <pmachata@redhat.com> - 0.4-1
- Upstream 0.4
- opt_x patch: New structure for opt_x list elements, now with
  'found'.  Using it in options.c, elf.c.
- testsuite patch: Automated testsuite for ltrace.

* Wed Mar  1 2006 Petr Machata  <pmachata@redhat.com> - 0.3.36-4.3
- include %%{ix86} to ExclusiveArch, instead of mere i386

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.3.36-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.3.36-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan  9 2006 Jakub Jelinek <jakub@redhat.com> 0.3.36-4
- added ppc64 and s390x support (IBM)
- added ia64 support (Ian Wienand)

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 0.3.36-3
- rebuilt with GCC 4

* Tue Dec 14 2004 Jakub Jelinek <jakub@redhat.com> 0.3.36-2
- make x86_64 ltrace trace both 32-bit and 64-bit binaries (#141955,
  IT#55600)
- fix tracing across execve
- fix printf-style format handling on 64-bit arches

* Thu Nov 18 2004 Jakub Jelinek <jakub@redhat.com> 0.3.36-1
- update to 0.3.36

* Mon Oct 11 2004 Jakub Jelinek <jakub@redhat.com> 0.3.35-1
- update to 0.3.35
- update syscall tables from latest kernel source

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Jakub Jelinek <jakub@redhat.com> 0.3.32-3
- buildreq elfutils-libelf-devel (#124921)

* Thu Apr 22 2004 Jakub Jelinek <jakub@redhat.com> 0.3.32-2
- fix demangling

* Thu Apr 22 2004 Jakub Jelinek <jakub@redhat.com> 0.3.32-1
- update to 0.3.32
  - fix dict.c assertion (#114359)
  - x86_64 support
- rewrite elf.[ch] using libelf
- don't rely on st_value of SHN_UNDEF symbols in binaries,
  instead walk .rel{,a}.plt and compute the addresses (#115299)
- fix x86-64 support
- some ltrace.conf additions
- some format string printing fixes

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb  3 2003 Jakub Jelinek <jakub@redhat.com> 0.3.29-1
- update to 0.3.29

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Sep  1 2002 Jakub Jelinek <jakub@redhat.com> 0.3.10-12
- add a bunch of missing functions to ltrace.conf
  (like strlen, ugh)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 28 2002 Phil Knirsch <pknirsch@redhat.com>
- Added the 'official' s390 patch.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jul 20 2001 Jakub Jelinek <jakub@redhat.com>
- fix stale symlink in documentation directory (#47749)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Aug  2 2000 Tim Waugh <twaugh@redhat.com>
- fix off-by-one problem in checking syscall number

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Matt Wilson <msw@redhat.com>
- rebuilt for next release
- patched Makefile.in to take a hint on mandir (patch2)
- use %%{_mandir} and %%makeinstall

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Jan  7 2000 Jeff Johnson <jbj@redhat.com>
- update to 0.3.10.
- include (but don't apply) sparc patch from Jakub Jellinek.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.3.6.

* Mon Sep 21 1998 Preston Brown <pbrown@redhat.com>
- upgraded to 0.3.4
