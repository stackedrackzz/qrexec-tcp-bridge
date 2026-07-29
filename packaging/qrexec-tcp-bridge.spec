Name:           qrexec-tcp-bridge
Version:        0.3.0
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

Also installs generate-policy.sh (/usr/share/qrexec-tcp-bridge/), which
regenerates /etc/qubes/policy.d/30-qrexec-tcp-bridge.policy from every
fragment in /etc/qrexec-tcp-bridge/access.conf.d/*.conf. Each fragment
line is "origin_tag destination port": e.g. "devel gitea-forge-host
3000". OR semantics: either tag alone is sufficient, on either side --
a qube tagged devel may call local.ConnectTCP+3000 against ANY qube,
and a qube tagged gitea-forge-host may be called by ANY qube on that
port; the two tags are not a matched pair that both have to hold at
once. Expands to 4 policy lines per tag-based fragment (Qubes RPC
Policy 4.0 has no OR combinator within one source/destination field),
except the literal string "dom0" on the destination side, kept as a
single unexpanded line (source must carry origin_tag; dest fixed dom0,
not opened to @anyvm) -- dom0 does not participate in the OR pool as a
taggable destination, and whether dom0 itself can carry a qvm-tag is
unverified here regardless. See the comment at the top of
generate-policy.sh for the full rationale.

Runs generate-policy.sh from %post, but only takes effect on dom0
(detected via the qubesd binary being present -- also unverified
against a live system); harmlessly skipped elsewhere. Consuming
packages (qubes-rpc-user, gitea-tor-forge) each drop their own fragment
into access.conf.d/ and re-run generate-policy.sh from their own %post,
since a fragment landing after this package's own install wouldn't
otherwise be picked up.

RECONSTRUCTED, NOT VERIFIED against a real dom0's
/etc/qubes-rpc/local.ConnectTCP or a live qubesd -- built from a
session with no working qrexec connection to any real Qubes dom0 to
diff against. See the warning comment at the top of
rpc/local.ConnectTCP and packaging/generate-policy.sh.

%prep
%setup -q

%build
# nothing to compile

%install
install -Dm0755 rpc/local.ConnectTCP %{buildroot}%{_sysconfdir}/qubes-rpc/local.ConnectTCP
install -Dm0755 packaging/generate-policy.sh %{buildroot}%{_datadir}/%{name}/generate-policy.sh
install -dm0755 %{buildroot}%{_sysconfdir}/qrexec-tcp-bridge/access.conf.d

%post
%{_datadir}/%{name}/generate-policy.sh || :

%files
%{_sysconfdir}/qubes-rpc/local.ConnectTCP
%{_datadir}/%{name}/generate-policy.sh
%dir %{_sysconfdir}/qrexec-tcp-bridge
%dir %{_sysconfdir}/qrexec-tcp-bridge/access.conf.d

%changelog
* Wed Jul 29 2026 stackedrackzz <noreply@users.noreply.github.com> - 0.3.0-1
- Change to OR semantics: either tag (origin or destination) alone is
  now sufficient, expanded into 4 policy lines per tag-based fragment,
  rather than requiring both tags to match simultaneously as a pair.
  Confirmed with the user after the previous (AND) behavior was flagged
  as not matching the originally stated design.
* Wed Jul 29 2026 stackedrackzz <noreply@users.noreply.github.com> - 0.2.0-1
- Add config-driven policy generation: access.conf.d/*.conf fragments
  ("origin_tag destination port") -> generate-policy.sh ->
  /etc/qubes/policy.d/30-qrexec-tcp-bridge.policy. Consuming packages
  contribute their own fragment instead of hand-writing policy files.
* Wed Jul 29 2026 stackedrackzz <noreply@users.noreply.github.com> - 0.1.0-1
- Initial packaging: factored out of qubes-rpc-user now that a second
  consumer (gitea-tor-forge's git-server qube) needs the same service
