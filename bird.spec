%global _hardened_build 1
Name:                bird
Version:             2.13.1
Release:             1
Summary:             BIRD Internet Routing Daemon
License:             GPLv2+
URL:                 https://bird.network.cz/
Source0:             https://bird.network.cz/download/bird-%{version}.tar.gz
Source1:             bird.service
Source2:             bird.tmpfilesd
BuildRequires:       flex bison ncurses-devel readline-devel sed gcc make libssh-devel systemd
Requires(pre):       shadow-utils
Obsoletes:           bird-sysvinit
Obsoletes:           bird6 < 2.0.2-1
Provides:            bird6 = %{version}-%{release}
%description
BIRD is a dynamic IP routing daemon supporting both, IPv4 and IPv6, Border
Gateway Protocol (BGPv4), Routing Information Protocol (RIPv2, RIPng), Open
Shortest Path First protocol (OSPFv2, OSPFv3), Babel Routing Protocol (Babel),
Bidirectional Forwarding Detection (BFD), IPv6 router advertisements, static
routes, inter-table protocol, command-line interface allowing on-line control
and inspection of the status of the daemon, soft reconfiguration as well as a
powerful language for route filtering.
%if 0%{!?_without_doc:1}

%package doc
Summary:             Documentation for BIRD Internet Routing Daemon
BuildRequires:       linuxdoc-tools sgml-common perl(FindBin)
BuildArch:           noarch
%description doc
Documentation for users and programmers of the BIRD Internet Routing Daemon.
BIRD is a dynamic IP routing daemon supporting both, IPv4 and IPv6, Border
Gateway Protocol (BGPv4), Routing Information Protocol (RIPv2, RIPng), Open
Shortest Path First protocol (OSPFv2, OSPFv3), Babel Routing Protocol (Babel),
Bidirectional Forwarding Detection (BFD), IPv6 router advertisements, static
routes, inter-table protocol, command-line interface allowing on-line control
and inspection of the status of the daemon, soft reconfiguration as well as a
powerful language for route filtering.
%endif

%prep
%autosetup -p1

%build
%configure --runstatedir=%{_rundir}/bird
%make_build all %{!?_without_doc:docs}

%install
%make_install
install -d %{buildroot}{%{_localstatedir}/lib/bird,%{_rundir}/bird}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/bird.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/bird.conf

%check
make test

%pre
getent group bird >/dev/null || groupadd -r bird
getent passwd bird >/dev/null || \
  useradd -r -g bird -d %{_localstatedir}/lib/bird -s /sbin/nologin \
  -c "BIRD daemon user" bird
exit 0

%post
%systemd_post bird.service

%preun
%systemd_preun bird.service

%postun
%systemd_postun_with_restart bird.service

%files
%doc NEWS README
%attr(0640,root,bird) %config(noreplace) %{_sysconfdir}/bird.conf
%{_unitdir}/bird.service
%{_tmpfilesdir}/bird.conf
%{_sbindir}/bird
%{_sbindir}/birdc
%{_sbindir}/birdcl
%dir %attr(0750,bird,bird) %{_localstatedir}/lib/bird
%dir %attr(0750,bird,bird) %{_rundir}/bird
%if 0%{!?_without_doc:1}

%files doc
%doc NEWS README
%doc doc/bird.conf.*
%doc obj/doc/bird*.html
%doc obj/doc/bird.pdf
%doc obj/doc/prog*.html
%doc obj/doc/prog.pdf
%endif

%changelog
* Thu Jul 13 2023 yaoxin <yao_xin001@hoperun.com> - 2.13.1-1
- Update to 2.13.1

* Fri May 13 2022 baizhonggui <baizhonggui@h-partners.com> - 2.0.9-1
- update to 2.0.9

* Mon Sep 6 2021 wulei <wulei80@huawei.com> - 2.0.8-1
- package init
