Name:           qrexec-tcp-bridge
Version:        0.1.0
Release:        1%{?dist}
Summary:        Generic qrexec RPC service bridging a call to a local TCP port
License:        MIT
URL:            https://example.invalid/qrexec-tcp-bridge
BuildArch:      noarch

Source0:        %{name}-%{version}.tar.gz

Requires:       socat

%description
Installs local.ConnectTCP, a generic qrexec RPC service
(/etc/qubes-rpc/local.ConnectTCP) bridging a qrexec call's stdio to
127.0.0.1:<port> on whichever qube it's installed on -- dom0 or a
regular qube alike, same script either way.

This package installs only the service script. It grants no access by
itself: qrexec policy (always dom0-side, per Qubes' own architecture,
regardless of which qube the service itself runs on) governs who may
call it and against which destination -- see qubes-rpc-user (dom0
access, restricted to ia-required-tagged qubes) and gitea-tor-forge
(git-server access, restricted to devel-tagged qubes on Gitea's ports
only) for the policies currently depending on this package.

RECONSTRUCTED, NOT VERIFIED against a real dom0's
/etc/qubes-rpc/local.ConnectTCP -- built from a session with no
working qrexec connection to any real Qubes dom0 to diff against. See
the warning comment at the top of rpc/local.ConnectTCP.

%prep
%setup -q

%build
# nothing to compile

%install
install -Dm0755 rpc/local.ConnectTCP %{buildroot}%{_sysconfdir}/qubes-rpc/local.ConnectTCP

%files
%{_sysconfdir}/qubes-rpc/local.ConnectTCP

%changelog
* Wed Jul 29 2026 stackedrackzz <noreply@users.noreply.github.com> - 0.1.0-1
- Initial packaging: factored out of qubes-rpc-user now that a second
  consumer (gitea-tor-forge's git-server qube) needs the same service
