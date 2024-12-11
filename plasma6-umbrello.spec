#define git 20240218
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")
%define stable %([ "$(echo %{version} |cut -d. -f3)" -ge 70 ] && echo -n un; echo -n stable)

Summary:	UML diagramming tool for KDE
Name:		plasma6-umbrello
Version:	24.11.90
Release:	%{?git:0.%{git}.}1
Group:		Graphical desktop/KDE
License:	GPLv2+
Url:		https://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/sdk/umbrello/-/archive/%{gitbranch}/umbrello-%{gitbranchd}.tar.bz2#/umbrello-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/release-service/%{version}/src/umbrello-%{version}.tar.xz
%endif
Patch0:		umbrello-20.03.80-llvm-10.patch
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Test)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Xml)
BuildRequires:	cmake(KF6Archive)
BuildRequires:	cmake(KF6Completion)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6DocTools)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6IconThemes)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6TextEditor)
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(KF6XmlGui)
BuildRequires:	cmake(KDevPlatform)
BuildRequires:	cmake(KDevelop-PG-Qt)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
BuildRequires:	cmake(KDevPlatform)
BuildRequires:	doxygen
BuildRequires:	cmake(Qt6ToolsTools)
# Not sure why, but building docs wants to translate from CP1260 to UTF-8...
BuildRequires:	locales-extra-charsets
# FIXME can be removed when LLVM cmake files stop referencing them
BuildRequires:	llvm-mlir-tools
BuildRequires:	llvm-static-devel
BuildRequires:	llvm-polly-devel
BuildRequires:	cmake(MLIR)
BuildRequires:	spirv-llvm-translator
BuildRequires:	%{_lib}gpuruntime
BuildRequires:	llvm-bolt
BuildRequires:	libclc-amdgcn
BuildRequires:	libclc-nvptx
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	cmake(KDevPlatform)
Requires:	kinit
Requires:	kio

%description
Umbrello UML Modeller is a UML diagramming tool for KDE.

%files -f %{name}.lang
%{_bindir}/umbrello5
%{_bindir}/po2xmi5
%{_bindir}/xmi2pot5
%{_datadir}/applications/org.kde.umbrello.desktop
%{_datadir}/metainfo/org.kde.umbrello.appdata.xml
%{_datadir}/umbrello5
%{_iconsdir}/hicolor/*/*/*.*[gz]
%{_docdir}/qt5/umbrello.qch

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n umbrello-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja -G Ninja -DBUILD_KF6:BOOL=ON

%build
%ninja_build -C build
# FIXME why doesn't ninja do this? It does respect the
# generated files in the install step...
cd build
doxygen Doxyfile.apidoc

%install
%ninja_install -C build
%find_lang %{name} --all-name --with-html
