#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	HTTP client/server library for GNOME
Summary(pl.UTF-8):	Biblioteka klienta/serwera HTTP dla GNOME
Name:		libsoup3
Version:	3.4.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libsoup/3.4/libsoup-%{version}.tar.xz
# Source0-md5:	ff455142b84727b7f120befde63f1386
# from libsoup 3.0.0 (waiting for pygobject3 release containing this file)
Source1:	Soup.py
Patch0:		%{name}-path-override.patch
URL:		https://wiki.gnome.org/Projects/libsoup
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.69.1
BuildRequires:	gobject-introspection-devel >= 0.10.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.20}
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
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sqlite3-devel
BuildRequires:	sysprof-devel >= 3.38
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.69.1
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
Requires:	glib2-devel >= 1:2.69.1
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
Requires:	gtk-doc-common
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
%patch0 -p1

%build
%meson build \
	%{!?with_apidocs:-Ddocs=disabled} \
	-Dntlm=enabled \
	-Dntlm_auth=/usr/bin/ntlm_auth \
	-Dtests=false \
	-Dtls_check=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides/Soup.py

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libsoup-3.0 $RPM_BUILD_ROOT%{_gtkdocdir}
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
%{_gtkdocdir}/libsoup-3.0
%endif

%files -n python3-libsoup3
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/Soup.py

%files -n vala-libsoup3
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libsoup-3.0.deps
%{_datadir}/vala/vapi/libsoup-3.0.vapi
