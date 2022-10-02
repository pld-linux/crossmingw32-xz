Summary:	LZMA library - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka LZMA - wersja skrośna dla MinGW32
Name:		crossmingw32-xz
Version:	5.2.7
Release:	1
License:	LGPL v2.1+
Group:		Development/Libraries
Source0:	https://tukaani.org/xz/xz-%{version}.tar.bz2
# Source0-md5:	154ab8026a415ea6d3026a2c9dc59ec5
URL:		https://tukaani.org/xz/
BuildRequires:	crossmingw32-gcc >= 3.4
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld    -Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
LZMA is default and general compression method of 7z format in 7-Zip
program. LZMA provides high compression ratio and very fast
decompression, so it is very suitable for embedded applications.

This package contains the cross version for Win32.

%description -l pl.UTF-8
LZMA jest domyślnym i ogólnym algorytmem kompresji formatu 7z
stosowanego przez 7-Zip. LZMA zapewnia wysoki stopień kompresji i
bardzo szybką dekompresję, więc nadaje się do zastosowań osadzonych.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static LZMA library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka LZMA (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static LZMA library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka LZMA (wersja skrośna MinGW32).

%package dll
Summary:	LZMA - DLL library for Windows
Summary(pl.UTF-8):	LZMA - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
LZMA - DLL library for Windows.

%description dll -l pl.UTF-8
LZMA - biblioteka DLL dla Windows.

%prep
%setup -q -n xz-%{version}

%build
%configure \
	--target=%{target} \
	--host=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_bindir}/* \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_datadir}/doc/xz \
	$RPM_BUILD_ROOT%{_datadir}/locale

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README THANKS doc/*.txt
%{_libdir}/liblzma.dll.a
%{_libdir}/liblzma.la
%{_includedir}/lzma
%{_includedir}/lzma.h
%{_pkgconfigdir}/liblzma.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblzma.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/liblzma-5.dll
