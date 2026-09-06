# HSA AQL profiling extension. TheRock 10.0.

Name:		aqlprofile
Version:	10.0.0
Release:	1
Summary:	AMD HSA AQL profiling library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-systems
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-10.0/aqlprofile.tar.gz#/aqlprofile-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-runtime-devel

%description
libhsa-amd-aqlprofile64 implements the HSA AQL profile extension
used by rocprofiler-sdk and rocprofv3.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers for the HSA AQL profile extension.

%prep
%autosetup -n aqlprofile -p1

%build
%cmake %{rocm_cmake_fhs} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DAQLPROFILE_BUILD_TESTS=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%ninja_build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib ] && [ ! -e %{buildroot}%{_libdir}/libhsa-amd-aqlprofile64.so ]; then
	mkdir -p %{buildroot}%{_libdir}
	mv %{buildroot}/usr/lib/libhsa-amd-aqlprofile64.so* %{buildroot}%{_libdir}/ 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi
# Legacy NCCL-shaped header is not installed by upstream CMake.
install -D -m644 inc/aql_profile.h %{buildroot}%{_includedir}/aql_profile.h

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libhsa-amd-aqlprofile64.so.*

%files devel
%{_includedir}/aql_profile.h
%{_includedir}/aqlprofile-sdk/
%{_libdir}/libhsa-amd-aqlprofile64.so
