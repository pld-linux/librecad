Summary:	Generic 2D CAD program
Name:		librecad
Version:	2.2.1.4
Release:	1
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	https://github.com/LibreCAD/LibreCAD/archive/refs/tags/v%{version}.tar.gz
# Source0-md5:	b12a8201214c4b481107e4d18a2111c8
URL:		https://librecad.org/
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	boost-devel
BuildRequires:	freetype-devel
BuildRequires:	pkgconfig
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qmake
Requires:	Qt5Core >= 5.15
Requires:	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibreCAD is a Qt application to design 2D CAD drawing based on the
community edition of QCad.

%prep
%setup -q -n LibreCAD-%{version}
%{__sed} -e 's|imgs/LibreCADicon|img/librecadlogo|' -i librecad/support/doc/LibreCADdoc.qhcp
:> librecad/support/doc/about.txt
%{__sed} -e 's|lrelease|lrelease-qt5|' -i scripts/postprocess-unix.sh
%{__sed} -i '/^LC_VERSION=/c LC_VERSION="%{version}"' librecad/src/src.pro

%build
qmake-qt5 %{name}.pro \
	QMAKE_CXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags} %{rpmcppflags}" \
	QMAKE_CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	QMAKE_CFLAGS_RELEASE="%{rpmcflags} %{rpmcppflags}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_datadir}/{mime/packages,%{name},metainfo},%{_libdir},%{_mandir}/man1,%{_pixmapsdir}}

install unix/{%{name},ttf2lff} $RPM_BUILD_ROOT%{_bindir}
ln -s ../../../%{_lib}/%{name} $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins
cp -r unix/resources/plugins $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -r unix/resources/qm $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a librecad/support/{fonts,library,patterns} $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a desktop/%{name}.1 tools/ttf2lff/ttf2lff.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a desktop/%{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a librecad/res/main/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}
cp -a desktop/%{name}.sharedmimeinfo $RPM_BUILD_ROOT%{_datadir}/mime/packages/%{name}.xml
cp -a unix/appdata/org.librecad.%{name}.appdata.xml $RPM_BUILD_ROOT%{_datadir}/metainfo

%find_lang %{name} --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database

%postun
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%license LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/ttf2lff
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/qm
# In RPM, %exclude removes these files from the broad %{_datadir}/%{name}
# entry below, but does not cancel the same paths listed via -f %{name}.lang.
# Keep .qm only through %{name}.lang so they are tagged as %lang(...).
%exclude %{_datadir}/%{name}/qm/*.qm
%{_datadir}/%{name}/fonts
%{_datadir}/%{name}/library
%{_datadir}/%{name}/patterns
%{_datadir}/%{name}/plugins
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/lib*.so
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/metainfo/org.librecad.%{name}.appdata.xml
%{_mandir}/man1/*.1*
