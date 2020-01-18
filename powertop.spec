Name:           powertop
Version:        2.3
Release:        8%{?dist}
Summary:        Power consumption monitor

Group:          Applications/System
License:        GPLv2
URL:            http://01.org/powertop/
Source0:        http://01.org/powertop/sites/default/files/downloads/%{name}-%{version}.tar.gz

# Sent upstream
Patch0:         powertop-2.3-always-create-params.patch
# Sent upstream (http://github.com/fenrus75/powertop/pull/11)
Patch1:         powertop-2.3-man-fix.patch
# Sent upstream (http://github.com/fenrus75/powertop/pull/12)
Patch2:         powertop-2.3-ondemand-check.patch
# Accepted upstream
Patch3:         powertop-2.3-unlimit-fds.patch
# Accepted upstream
Patch4:         powertop-2.3-fd-limit-err.patch
# Sent upstream
Patch5:         powertop-2.3-reg-net-params.patch
Patch6:         powertop-2.3-tunable-overflow-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gettext, ncurses-devel, pciutils-devel, zlib-devel, libnl3-devel
Requires(post): coreutils

%description
PowerTOP is a tool that finds the software component(s) that make your
computer use more power than necessary while it is idle.

%prep
%setup -q
%patch0 -p1 -b .always-create-params
%patch1 -p1 -b .man-fix
%patch2 -p1 -b .ondemand-check
%patch3 -p1 -b .unlimit-fds
%patch4 -p1 -b .fd-limit-err
%patch5 -p1 -b .reg-net-params
%patch6 -p1 -b .tunable-overflow-fix.patch

# remove left over object files
find . -name "*.o" -exec rm {} \;

%build
%configure
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -Dd %{buildroot}%{_localstatedir}/cache/powertop
touch %{buildroot}%{_localstatedir}/cache/powertop/{saved_parameters.powertop,saved_results.powertop}
%find_lang %{name}

%post
# Hack for powertop not to show warnings on first start
touch %{_localstatedir}/cache/powertop/{saved_parameters.powertop,saved_results.powertop}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README TODO
%dir %{_localstatedir}/cache/powertop
%ghost %{_localstatedir}/cache/powertop/saved_parameters.powertop
%ghost %{_localstatedir}/cache/powertop/saved_results.powertop
%{_sbindir}/powertop
%{_mandir}/man8/powertop.8*

%changelog
* Tue Mar 25 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-8
- Fixed buffer overflow in cpufreq tunables on systems with many CPUs
  (by tunable-overflow-fix patch)
  Resolves: rhbz#1080191

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.3-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.3-6
- Mass rebuild 2013-12-27

* Tue Oct 29 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-5
- Fixed some possible unregistered parameters errors
  (by reg-net-param patch)
  Resolves: rhbz#1014662
- Unlimit FDs (by unlimit-fds patch)
  Printed friendly error message if the system is running out
  of FDs (by fd-limit-err patch)
  Resolves: rhbz#1017668

* Fri Jun 28 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-4
- Added check if ondemand governor is applicable (by ondemand-check patch)
  Resolves: rhbz#697273

* Tue Jun 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-3
- Added workload option to the man page

* Wed Apr 10 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-2
- Added post requirements for coreutils

* Wed Mar 20 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-1
- New version
  Resolves: rhbz#923729
- Dropped fix-crash-on-readonly-fs, reduce-syscalls,
  gpu-wiggle-fix patches (upstreamed)
- Dropped version-fix patch (not needed)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dan Horák <dan@danny.cz> - 2.2-6
- rebuilt again for fixed soname in libnl3

* Sun Jan 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.2-5
- Rebuilt for libnl3

* Mon Jan 14 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-4
- Reduced number of useless syscalls (reduce-syscalls patch) and
  fixed gpu wiggle (gpu-wiggle-fix patch)
  Resolves: rhbz#886185

* Sun Dec  2 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-3
- Updated version to show 2.2 (by version-fix patch)

* Wed Nov 28 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-2
- Fixed crash when writing report on readonly filesystem
  (fix-crash-on-readonly-fs patch)

* Fri Nov 23 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2-1
- New version
  Resolves: rhbz#877373
- Dropped html-escape patch (not needed)

* Thu Aug 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1-2
- Removed left over object files

* Thu Aug 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1-1
- New version
- Removed patches (all upstreamed): show-watts-only-if-discharging,
  valid-html-output, factor-out-powertop-init, catch-fstream-errors

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0-3
- Catch fstream exceptions
  Resolves: rhbz#832497

* Mon May 21 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0-2
- Fixed segfault during calibration
  Resolves: rhbz#823502
- Used macro optflags instead of variable RPM_OPT_FLAGS

* Wed May 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0-1
- New version
  Resolves: rhbz#821144
- Dropped patches: unknown-readings-fix (upstreamed), compile-fix (upstreamed),
  power-supply-add-power-now-support (upstreamed),
  html-print-commands (upstreamed), add-power-supply-class-support (obsoleted),
  power-supply-units-fix (obsoleted)
- Updated patches: show-watts-only-if-discharging patch (sent upstream),
  html-escape patch
- Added patch: valid-html-output (sent upstream)

* Tue Apr 17 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-9
- Show power consumption only if discharging
  Resolves: rhbz#811949

* Tue Apr 03 2012 Jan Kaluza <jkaluza@redhat.com> - 1.98-8
- Escape scripts in HTML output

* Mon Mar 26 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-7
- Print commands which reproduce the tunings into html log (html-print-commands patch)

* Wed Mar  7 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-6
- Fixed power_supply units
  Resolves: rhbz#800814

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98-5
- Rebuilt for c++ ABI breakage

* Fri Feb 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-4
- Backported support for power_supply class
  (add-power-supply-class-support patch)
- Added support for POWER_NOW readings
  (power-supply-add-power-now-support patch)
  Resolves: rhbz#796068

* Tue Jan 10 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-3
- Fixed 'unknown' readings from ACPI meters
  Resolves: rhbz#770289
- Fixed compilation on f17

* Fri Dec  2 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-2
- Always create params file
  Resolves: rhbz#698020
- Added cache files

* Wed May 25 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.98-1
- New version

* Wed Mar 23 2011 Dan Horák <dan[at]danny.cz> - 1.97-2
- csstoh should return 0

* Tue Feb 15 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.97-1
- New version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.13-2
- Fixed sigwinch handling (#644800)
- Readded strncpy patch as strncpy is safer than strcpy
- Print all P-states in dump mode
- Added explicit requires for pcituils (#653560)
- Output error in interactive mode if there is no tty (#657212)
- Do not suggest ondemand when p4-clockmod scaling driver is used (#497167)
- Fixed rpmlint warning about mixed tabs and spaces

* Wed Aug 25 2010 Adam Jackson <ajax@redhat.com> 1.13-1
- powertop 1.13

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Adam Jackson <ajax@redhat.com> 1.11-1
- powertop 1.11

* Thu Nov 20 2008 Adam Jackson <ajax@redhat.com>
- Spec only change, fix URL.

* Thu Nov  6 2008 Josh Boyer <jwboyer@gmail.com> - 1.10-1
- Update to latest release
- Drop upstreamed patch

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.9-4
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.9-3
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Adam Jackson <ajax@redhat.com> 1.9-2
- Use full path when invoking hciconfig. (Ville Skyttä, #426721)

* Mon Dec 10 2007 Josh Boyer <jwboyer@gmail.com> 1.9-1
- Update to latest release

* Mon Aug 20 2007 Josh Boyer <jwboyer@jdub.homelinux.org> 1.8-1
- Update to latest release

* Mon Jul 23 2007 Bill Nottingham <notting@redhat.com> 1.7-4
- add patch to allow dumping output to stdout

* Mon Jul 09 2007 Adam Jackson <ajax@redhat.com> 1.7-3
- powertop-1.7-strncpy.patch: Use strncpy() to avoid stack smash. Patch from
  Till Maas. (#246796)

* Thu Jul 05 2007 Adam Jackson <ajax@redhat.com> 1.7-2
- Don't suggest disabling g-p-m.  Any additional power consumption is more
  than offset by the ability to suspend.

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.7-1
- powertop 1.7.

* Mon Jun 11 2007 Adam Jackson <ajax@redhat.com> 1.6-1
- powertop 1.6.

* Tue May 29 2007 Adam Jackson <ajax@redhat.com> 1.5-1
- powertop 1.5.

* Mon May 21 2007 Adam Jackson <ajax@redhat.com> 1.3-1
- powertop 1.3.

* Tue May 15 2007 Adam Jackson <ajax@redhat.com> 1.2-1
- powertop 1.2.  Fixes power reports on machines that report power in Amperes
  instead of Watts.

* Sun May 13 2007 Adam Jackson <ajax@redhat.com> 1.1-1
- powertop 1.1.

* Fri May 11 2007 Adam Jackson <ajax@redhat.com> 1.0-1
- Initial revision.
