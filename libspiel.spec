#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# unit tests
#
Summary:	Shared library for speech synthesis clients
Summary(pl.UTF-8):	Biblioteka współdzielona dla klientów syntezy mowy
Name:		libspiel
Version:	1.0.4
%define	gitref	SPIEL_%(echo %{version} | tr . _)
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/project-spiel/libspiel/tags
Source0:	https://github.com/project-spiel/libspiel/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	462459849eefea7501df1bdf09136af0
URL:		https://project-spiel.org/libspiel/
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.76
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
BuildRequires:	libspeechprovider-devel >= 1.0.3
BuildRequires:	meson >= 0.64.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
%if %{with tests}
BuildRequires:	dbus-devel >= 1.14.4
%endif
Requires:	glib2 >= 1:2.76
Requires:	libspeechprovider >= 1.0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This client library is designed to provide an ergonomic interface to
the myriad of potential speech providers that are installed in a given
session. The API is inspired by the W3C Web Speech API.

%description -l pl.UTF-8
Ta biblioteka kliencka jest zaprojektowana w celu dostarczenia
ergonomicznego interfejsu dla miriady potencjalnych dostawców mowy
zainstalowanych w danej sesji. API jest zainspirowane W3C Web Speech
API.

%package devel
Summary:	Header files for spiel library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki spiel
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.76
Requires:	libspeechprovider-devel >= 1.0.3

%description devel
Header files for spiel library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki spiel.

%package apidocs
Summary:	API documentation for spiel library
Summary(pl.UTF-8):	Dokumentacja API biblioteki spiel
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for spiel library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki spiel.

%prep
%setup -q -n %{name}-%{gitref}

%build
%meson \
	%{!?with_apidocs:-Ddocs=false} \
	%{!?with_tests:-Dtests=false}

%meson_build

%if %{with tests}
%meson_test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libspiel $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/spiel
%attr(755,root,root) %{_libdir}/libspiel-1.0.so.1.0.4
%ghost %{_libdir}/libspiel-1.0.so.1
%{_libdir}/girepository-1.0/Spiel-1.0.typelib
%{_datadir}/glib-2.0/schemas/org.monotonous.libspiel.gschema.xml

%files devel
%defattr(644,root,root,755)
%{_libdir}/libspiel-1.0.so
%{_includedir}/spiel
%{_datadir}/gir-1.0/Spiel-1.0.gir
%{_pkgconfigdir}/spiel-1.0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libspiel
%endif
