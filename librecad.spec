Summary:	Generic 2D CAD program
Name:		librecad
Version:	2.0.8
Release:	1
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	https://github.com/LibreCAD/LibreCAD/archive/%{version}.tar.gz
# Source0-md5:	b8dc5383c299ef31481ef4db76958225
URL:		http://www.librecad.org/
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtHelp-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtSvg-devel
BuildRequires:	QtXml-devel
BuildRequires:	boost-devel
BuildRequires:	freetype-devel
BuildRequires:	muparser-devel
BuildRequires:	qt4-assistant
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
Requires:	QtCore >= 4.8.0
Requires:	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibreCAD is a Qt4 application to design 2D CAD drawing based on the
community edition of QCad.

%prep
%setup -q -n LibreCAD-%{version}
%{__sed} -e 's|imgs/LibreCADicon|img/librecadlogo|' -i librecad/support/doc/LibreCADdoc.qhcp
:> librecad/support/doc/about.txt
%{__sed} -e 's|lrelease|lrelease-qt4|' -i scripts/postprocess-unix.sh

%build
qmake-qt4 %{name}.pro \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_datadir}/{mime/packages,%{name}},%{_libdir},%{_mandir}/man1,%{_pixmapsdir}}

install unix/{%{name},ttf2lff} $RPM_BUILD_ROOT%{_bindir}
ln -s %{_libdir}/%{name} $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins
cp -r unix/resources/plugins $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -r unix/resources/{doc,qm} $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a librecad/support/{fonts,library,patterns} $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a desktop/%{name}.1 tools/ttf2lff/ttf2lff.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a desktop/%{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a librecad/res/main/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}
cp -a desktop/%{name}.sharedmimeinfo $RPM_BUILD_ROOT%{_datadir}/mime/packages/%{name}.xml

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database

%postun
%update_mime_database

%files
%defattr(644,root,root,755)
%doc plugins/importshp/shapelib/ChangeLog
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/ttf2lff
# TODO: mark qm/*.qm files with %lang() as %%find_lang doesn't handle files outside */share/locale
%{_datadir}/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/lib*.so
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man1/*.1*
