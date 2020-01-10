Name:           powertop
Version:        2.3
Release:        4%{?dist}
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
Patch3:         powertop-2.4-unlimit-fds.patch
# Sent upstream
Patch4:         powertop-2.4-fd-limit-err.patch
# Modified version sent upstream
Patch5:         powertop-2.3-improve-reporting-options.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gettext, ncurses-devel, pciutils-devel, zlib-devel, libnl-devel
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
%patch5 -p1 -b .improve-reporting-options

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
* Fri Oct  7 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-4
- Reintroduced -d dump switch and improved reporting options
  (by improve-reporting-options patch)
  Resolves: rhbz#1333439

* Tue Oct  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-3
- New version of unlimit-fds patch
- Fixed error message if FDs limit is reached (by fd-limit-err patch)
  Related: rhbz#998021

* Mon Sep 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-2
- Unlimit FDs (by unlimit-fds patch)
  Resolves: rhbz#998021

* Wed Jul  3 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-1
- New version
  Resolves: rhbz#829800, rhbz#682378, rhbz#697273

* Tue Aug 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.11-6
- Improved sigwinch handling
  Resolves: rhbz#698422

  * Tue Aug 02 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.11-5
- Fixed sigwinch handling
  Resolves: rhbz#698422

* Fri Dec 03 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.11-4
- Backported turbo detection (turbo patch, #610464)
- Show all P-states in dump mode (dump-all-pstates patch, accepted by upstream)
- Backported tty handling for non-interactive mode (notty patch, #628514)
- Output error in interactive mode if there is no tty (checktty patch,
  posted upstream)
- Fixed rpmlint warning about mixed tabs and spaces

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.11-3.1
- Rebuilt for RHEL 6

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
