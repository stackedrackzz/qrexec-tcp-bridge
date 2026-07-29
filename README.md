# qrexec-tcp-bridge

A generic Qubes qrexec RPC service (`local.ConnectTCP`) bridging a qrexec
call's stdio to `127.0.0.1:<port>` on whichever qube it's installed on --
dom0 or a regular qube, same script either way.

Factored out of `qubes-rpc-user` once a second consumer
(`gitea-tor-forge`'s dedicated git-server qube) needed the exact same
service. This package installs *only* the RPC script; it grants no access
by itself. Qrexec policy is always dom0-side regardless of which qube the
service itself runs on -- see:

- `qubes-rpc-user` -- policy restricting calls to dom0 to `ia-required`-tagged
  qubes.
- `gitea-tor-forge` -- policy restricting calls to the git-server qube (on
  Gitea's HTTP/SSH ports only) to `devel`-tagged qubes.

**`rpc/local.ConnectTCP` is a reconstruction, not verified against a real
dom0's `/etc/qubes-rpc/local.ConnectTCP`** -- built from a session with no
working qrexec connection to any real Qubes dom0 to diff against. See the
warning comment at the top of the file.

Built with `mock` in `.github/workflows/build-rpm.yml`, published to
`rpm-repo` -- same pipeline as this project's other packages.
