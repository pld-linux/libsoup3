#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	HTTP client/server library for GNOME
Summary(pl.UTF-8):	Biblioteka klienta/serwera HTTP dla GNOME
Name:		libsoup3
Version:	3.6.4
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libsoup/3.6/libsoup-%{version}.tar.xz
# Source0-md5:	b42bfcd87a78b82272d2004976e10766
# from libsoup 3.0.0 (waiting for pygobject3 release containing this file)
Source1:	Soup.py
Patch0:		%{name}-path-override.patch
URL:		https://wiki.gnome.org/Projects/libsoup
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.70.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	heimdal-devel
BuildRequires:	libbrotli-devel
BuildRequires:	libpsl-devel >= 0.20.0
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	meson >= 0.54
BuildRequires:	nghttp2-devel >= 1.50.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sqlite3-devel
BuildRequires:	sysprof-devel >= 3.38
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.70.0
Requires:	libpsl >= 0.20.0
Requires:	nghttp2-libs >= 1.50.0
# for TLS support
Suggests:	glib-networking
# ntlm_auth for NTLM support
Suggests:	samba-winbind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libsoup is an HTTP client/server library for GNOME. It uses GObjects
and the glib main loop, to integrate well with GNOME applications.

%description -l pl.UTF-8
libsoup to biblioteka klienta/serwera HTTP dla GNOME. Wykorzystuje
typy GObject oraz pętlę główną glib, aby dobrze integrować się z
aplikacjami GNOME.

%package devel
Summary:	Header files for libsoup 3 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsoup 3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.70.0
Requires:	libbrotli-devel
Requires:	libpsl-devel >= 0.20.0
Requires:	libxml2-devel >= 1:2.6.31
Requires:	sqlite3-devel
Requires:	sysprof-devel >= 3.38
Requires:	zlib-devel

%description devel
Header files for libsoup 3 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsoup 3.

%package static
Summary:	libsoup 3 static library
Summary(pl.UTF-8):	Biblioteka statyczna libsoup 3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libsoup 3 static library.

%description static -l pl.UTF-8
Biblioteka statyczna libsoup 3.

%package apidocs
Summary:	libsoup API documentation
Summary(pl.UTF-8):	Dokumentacja API libsoup
Group:		Documentation
BuildArch:	noarch

%description apidocs
libsoup API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libsoup.

%package -n python3-libsoup3
Summary:	Python 3.x interface for libsoup 3 library
Summary(pl.UTF-8):	Interfejs Pythona 3.x do biblioteki libsoup 3
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-pygobject3 >= 3.0

%description -n python3-libsoup3
Python 3.x interface for libsoup 3 library.

%description -n python3-libsoup3 -l pl.UTF-8
Interfejs Pythona 3.x do biblioteki libsoup 3.

%package -n vala-libsoup3
Summary:	libsoup 3 API for Vala language
Summary(pl.UTF-8):	API libsoup 3 dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-libsoup3
libsoup 3 API for Vala language.

%description -n vala-libsoup3 -l pl.UTF-8
API libsoup 3 dla języka Vala.

%prep
%setup -q -n libsoup-%{version}
%patch -P0 -p1

%build
%meson \
	-Dautobahn=disabled \
	%{!?with_apidocs:-Ddocs=disabled} \
	-Dntlm=enabled \
	-Dntlm_auth=/usr/bin/ntlm_auth \
	-Dtests=false \
	-Dtls_check=false

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides/Soup.py

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libsoup-3.0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%find_lang libsoup-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f libsoup-3.0.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libsoup-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsoup-3.0.so.0
%{_libdir}/girepository-1.0/Soup-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsoup-3.0.so
%{_includedir}/libsoup-3.0
%{_pkgconfigdir}/libsoup-3.0.pc
%{_datadir}/gir-1.0/Soup-3.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libsoup-3.0.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libsoup-3.0
%endif

%files -n python3-libsoup3
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/Soup.py

%files -n vala-libsoup3
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libsoup-3.0.deps
%{_datadir}/vala/vapi/libsoup-3.0.vapi
