%global         sum The Software Factory project documentation

Name:           sf-docs
Version:        3.0.0
Release:        1%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://softwarefactory-project.io/r/p/%{name}
Source0:        https://github.com/softwarefactory-project/sf-docs/archive/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-sphinx
BuildRequires:  graphviz
BuildRequires:  python-sphinx_rtd_theme
Requires:       rh-python35-managesf-doc
Requires:       python-sfmanager-doc

%description
%{sum}

%prep
%autosetup -n %{name}-%{version}

%build
sphinx-build -W -b html -d build/doctrees docs/ build/html

%install
mkdir -p %{buildroot}%{_docdir}/software-factory
mv build/html/* %{buildroot}%{_docdir}/software-factory

%files
%license LICENSE
%{_docdir}/software-factory

%changelog
* Mon Feb 26 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 3.0.0-1
- Update version to 3.0

* Mon Aug 14 2017 Nicolas Hicher <nhicher@redhat.com> - 2.7.0-1
- add -W flag to ensure to build without warnings
- add graphviz and python-sphinx_rtd_theme build depends

* Wed Apr 12 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 2.5.0-1
- Initial packaging import
