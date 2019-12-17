%global         sum The Software Factory project documentation

Name:           sf-docs
Version:        3.4.0
Release:        3%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://softwarefactory-project.io/r/p/%{name}
Source0: HEAD.tgz

BuildArch:      noarch
BuildRequires:  python3-sphinx
BuildRequires:  graphviz
BuildRequires:  python3-sphinx_rtd_theme

%description
%{sum}

%prep
%autosetup -n %{name}-%{version}

%build
sphinx-build-3 -W -b html -d build/doctrees docs/ build/html

%install
mkdir -p %{buildroot}%{_docdir}/software-factory
mv build/html/* %{buildroot}%{_docdir}/software-factory

%files
%license LICENSE
%{_docdir}/software-factory

%changelog
* Tue Sep 24 2019 Tristan Cacqueray <tdecacqu@redhat.com> - 3.3.0-3
- Remove managesf requirement

* Sat Sep 21 2019 Tristan Cacqueray <tdecacqu@redhat.com> - 3.3.0-2
- Use python3-sphinx

* Mon Feb 26 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 3.0.0-1
- Update version to 3.0

* Mon Aug 14 2017 Nicolas Hicher <nhicher@redhat.com> - 2.7.0-1
- add -W flag to ensure to build without warnings
- add graphviz and python-sphinx_rtd_theme build depends

* Wed Apr 12 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 2.5.0-1
- Initial packaging import
