Name:		librecad
Version:	1.0.2
Release:	0.1
License:	GPL v2
URL:		http://www.librecad.org/
Source0:	https://github.com/LibreCAD/LibreCAD/archive/v%{version}.tar.gz
# Source0-md5:	28f324559f221c1e50dacb15741d09ec
Summary:	An generic 2D CAD program
Group:		X11/Applications
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtHelp-devel
BuildRequires:	QtSql-devel
BuildRequires:	muparser-devel
BuildRequires:	qt4-assistant
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist

%description
LibreCAD is a Qt4 application to design 2D cad drawing based on the
community edition of QCad.

%prep
%setup -q -n LibreCAD-%{version}

%build
qmake-qt4
%{__make}

cd plugins
qmake-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# Let's create the directory structure
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{fonts,patterns,qm,library/misc,library/templates,doc}
install -d $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/html/{classref/html/,img,imgs}
install -d $RPM_BUILD_ROOT%{_desktopdir}/
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins
# Now install all files
install -Dm 755  unix/%{name} $RPM_BUILD_ROOT/%{_bindir}/%{name}
install -Dm 644 res/main/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
install -t $RPM_BUILD_ROOT%{_datadir}/%{name}/patterns/  unix/resources/patterns/*.dxf
install -t $RPM_BUILD_ROOT%{_datadir}/%{name}/fonts/  unix/resources/fonts/*
install -t $RPM_BUILD_ROOT%{_datadir}/%{name}/library/misc  unix/resources/library/misc/*
install -t $RPM_BUILD_ROOT%{_datadir}/%{name}/library/templates unix/resources/library/templates/*
install -t $RPM_BUILD_ROOT%{_datadir}/%{name}/qm/  unix/resources/qm/*.qm
install -t $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/ unix/resources/plugins/*
# Install documentation files
install -t $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/html  support/doc/*.html


# Create the desktop file

cat > $RPM_BUILD_ROOT%{_desktopdir}/%{_real_vendor}-%{name}.desktop <<EOF
[Desktop Entry]
Name=LibreCAD
GenericName=LibreCAD is a general purpose 2D CAD
Type=Application
Categories=Graphics;2DGraphics;VectorGraphics;
Exec=librecad
Icon=librecad

EOF

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/%{_real_vendor}-%{name}.desktop
%{_pixmapsdir}/%{name}.png

#%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}/qm/
%{_datadir}/%{name}/fonts/ %{_datadir}/%{name}/patterns/

#%files parts
%defattr(644,root,root,755)
%{_datadir}/%{name}/library

#%files plugins
%defattr(644,root,root,755)
%{_libdir}/%{name}/plugins/

#%files doc
%defattr(644,root,root,755)
# README is here to workaround a bug in %doc of rpm. Possible fix by rpm-4.9
This package contains documentation for LibreCAD.
%doc README gpl-2.0.txt support/doc/about.txt
This package contains documentation for LibreCAD.
%doc %{_datadir}/doc/%{name}/html/

This package contains documentation for LibreCAD.

