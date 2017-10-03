Name:           deepin-wm
Version:        1.9.16
Release:        1%{?dist}
Summary:        Deepin Window Manager
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-wm
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  gnome-common
BuildRequires:  pkgconfig(clutter-gtk-1.0)
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(granite)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libbamf3)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libcanberra-gtk3)
BuildRequires:  pkgconfig(libdeepin-mutter)
BuildRequires:  pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(vapigen)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xkbfile)
Requires:       deepin-desktop-schemas
Requires:       gnome-desktop
Requires:       libcanberra-gtk3
Requires:       hicolor-icon-theme

%description
Deepin Window Manager

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}

%prep
%setup -q

# fix background path
sed -i 's|default_background.jpg|default.png|' \
    src/Background/BackgroundSource.vala

%build
./autogen.sh
%configure --disable-schemas-compile
%make_build

%install
%make_install PREFIX="%{_prefix}"

# Remove libtool archives
find %{buildroot} -name '*.la' -delete

%find_lang %{name}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop ||:

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/lib*.so.*
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/vala/vapi/%{name}*

%files devel
%{_includedir}/%{name}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%changelog
* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 1.9.16-1
- Update to 1.9.16

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 1.9.15-1
- Update to 1.9.15

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.9.14-1.git90453e3
- Update to 1.9.14

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.9.12-1.git42cd230
- Update to 1.9.12

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 1.9.5-1.git3d3e077
- Update to 1.9.5

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.9.2-1.git4cb2f7e
- Update to 1.9.2

* Wed Jan 04 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.0-2
- Split the package to main and devel

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.0-1
- Update to version 1.2.0

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.2-1
- Initial package build
