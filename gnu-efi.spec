Summary:	Library for building x86_64 and i386 UEFI Applications
Name:		gnu-efi
Version:	3.0u
Release:	1
# Intel and HP's BSD-like license, except setjmp code coming from GRUB
License:	GPL v2+ (setjmp code), BSD-like (all the rest)
Group:		Development/Libraries
Source0:	http://downloads.sourceforge.net/gnu-efi/%{name}_%{version}.orig.tar.gz
# Source0-md5:	d15d3c700e79a1e2938544d73edc572d
URL:		http://gnu-efi.sourceforge.net/
BuildRequires:	binutils
BuildRequires:	gcc
Requires:	binutils
Requires:	gcc
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-stack-protector
%define		_libexecdir	%{_libdir}/gnuefi

%description
GNU-EFI development environment allows to create EFI applications for
IA-64 and x86 platforms using the GNU toolchain.

%prep
%setup -qn %{name}-3.0

# remove broken ABI
%{__sed} -i "s/-DGNU_EFI_USE_MS_ABI //" Make.defaults

# use CFLAGS
%{__sed} -i "s/-O2 /%{rpmcflags}/" Make.defaults

%build
%{__make} -j1 \
	ARCH=$(echo %{_target_base_arch} | sed -e 's/i386/ia32/')	\
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT	\
	LIBDIR=%{_libexecdir}		\
	PREFIX=%{_prefix}

%{__mv} $RPM_BUILD_ROOT{%{_libexecdir}/*.a,%{_libdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README.*
%{_libdir}/libefi.a
%{_libdir}/libgnuefi.a
%dir %{_libexecdir}
%{_libexecdir}/elf_*_efi.lds
%{_libexecdir}/crt0-efi-*.o
%{_includedir}/efi

