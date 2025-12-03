%define debug_package %{nil}

Name:           skopeo
Version:        1.21.0
Release:        1%{?dist}
Summary:        Work with remote images registries - retrieving information, images, signing content
Group:          Applications/System
License:        Apache-2.0
URL:            https://github.com/containers/%{name}
Source:         https://github.com/containers/%{name}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:  golang gpgme-devel libassuan-devel go-md2man git-core glib2-devel make shadow-utils-subid-devel
Requires:       gpgme
Requires:       containers-common >= 4:1-21
Recommends:     bats

%if 0%{?rhel} >= 9
BuildRequires:  btrfs-progs-devel
%endif

%description
skopeo is a command line utility that performs various operations on container images and image repositories.
skopeo does not require the user to be running as root to do most of its operations.
skopeo does not require a daemon to be running to perform its operations.
skopeo can work with OCI images as well as the original Docker v2 images.

%prep
%setup -q -n %{name}-%{version}

%build
make bin/skopeo
# generate docs
make docs
find docs -type f -name "*.1" -exec gzip -9 {} \;
# generate completions
mkdir -p completions/bash completions/zsh completions/fish
bin/%{name} completion bash >| completions/bash/%{name}
bin/%{name} completion zsh >| completions/zsh/_%{name}
bin/%{name} completion fish >| completions/fish/%{name}.fish

%install
install -Dm0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_mandir}/man1
install -Dm0644 docs/*.1.gz %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
install -Dm0644 completions/bash/%{name} %{buildroot}%{_datadir}/bash-completion/completions/%{name}
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
install -Dm0644 completions/zsh/_%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
install -Dm0644 completions/fish/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
mkdir -p %{buildroot}%{_sysconfdir}/containers/registries.d
mkdir -p %{buildroot}%{_localstatedir}/lib/containers/sigstore
install -Dm0644 default-policy.json %{buildroot}%{_sysconfdir}/containers/policy.json
install -Dm0644 default.yaml %{buildroot}%{_sysconfdir}/containers/registries.d/default.yaml

%files
%{_bindir}/%{name}
%{_mandir}/man1/*.1.gz
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_sysconfdir}/containers/policy.json
%{_sysconfdir}/containers/registries.d/default.yaml
%doc LICENSE README.md

%changelog
* Thu Dec 4 2025 Jamie Curnow <jc@jc21.com> 1.21.0-1
- v1.21.0

* Tue Aug 05 2025 Jamie Curnow <jc@jc21.com> 1.20.0-1
- v1.20.0

* Fri May 23 2025 Jamie Curnow <jc@jc21.com> 1.19.0-1
- v1.19.0

* Thu Apr 10 2025 Jamie Curnow <jc@jc21.com> 1.18.0-1
- v1.18.0
