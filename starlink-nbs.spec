Summary:	NBS - NoticeBoard System
Summary(pl):	NBS - system powiadamiania
Name:		starlink-nbs
Version:	2.5_8.218
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.starlink.rl.ac.uk/pub/ussc/store/nbs/nbs.tar.Z
# Source0-md5:	3b3b7b10774d03fca2fb7d4bcdcdbeeb
URL:		http://www.starlink.rl.ac.uk/static_www/soft_further_NBS.html
BuildRequires:	gcc-g77
BuildRequires:	sed >= 4.0
BuildRequires:	starlink-ems-devel
BuildRequires:	starlink-sae-devel
Requires:	starlink-sae
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		stardir		/usr/lib/star

%description
The noticeboard system routines provide a fast means for processes to
share data in global memory. A given process may own as many
noticeboards as it wishes and may access noticeboards owned by other
processes. Normally the only process that writes to a noticeboard is
its owner but other processes that know what they are doing can
subvert this rule either by calling a special routine or else by
accessing noticeboard data by using a pointer.

%description -l pl
Funkcje systemu powiadamiania (NBS - NoticeBoard System) udostêpniaj±
szybki sposób na dzielenie danych miêdzy procesami w globalnej
pamiêci. Dany proces mo¿e u¿ywaæ tyle tablic powiadomieñ, ile tylko
zechce oraz mo¿e odwo³ywaæ siê do tablic nale¿±cych do innych
procesów. Zwykle tylko jeden proces, który jako wy³±czny zapisuje do
tablicy, jest jej w³a¶cicielem, ale inne procesy, wiedz±c z czym to
siê wi±¿e, mog± obaliæ tê zasadê wywo³uj±c specjaln± funkcjê lub
odwo³uj±c siê do danych tablicy poprzez wska¼nik.

%package devel
Summary:	Header files for NBS library
Summary(pl):	Pliki nag³ówkowe biblioteki NBS
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	starlink-ems-devel

%description devel
Header files for NBS library.

%description devel -l pl
Pliki nag³ówkowe biblioteki NBS.

%package static
Summary:	Static Starlink NBS library
Summary(pl):	Statyczna biblioteka Starlink NBS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static Starlink NBS library.

%description static -l pl
Statyczna biblioteka Starlink NBS.

%prep
%setup -q -c

sed -i -e "s/-O'/%{rpmcflags} -fPIC'/" mk
sed -i -e "s/\\(-L\\\$(STAR_\\)LIB)/\\1SHARE)/;s/-L\\. lib\\\$(PKG_NAME)\\.a/-L. -l\\\$(PKG_NAME)/" makefile

%build
SYSTEM=ix86_Linux \
BLD_SHR='f() { %{__cc} -shared $$3 -Wl,-soname=$$1 -o $$1 $$2;}; f' \
./mk build \
	STARLINK=%{stardir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{stardir}/help

SYSTEM=ix86_Linux \
./mk install \
	STARLINK=%{stardir} \
	INSTALL=$RPM_BUILD_ROOT%{stardir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc nbs.news
%attr(755,root,root) %{stardir}/bin/nbtrace
%{stardir}/dates/*
%docdir %{stardir}/docs
%{stardir}/docs/sun*
%{stardir}/help/fac*
%attr(755,root,root) %{stardir}/share/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{stardir}/bin/nbs_dev
%attr(755,root,root) %{stardir}/bin/nbs_link*
%{stardir}/include/*

%files static
%defattr(644,root,root,755)
%{stardir}/lib/*.a
