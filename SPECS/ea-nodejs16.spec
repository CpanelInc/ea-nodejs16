%global debug_package %{nil}

Name:    ea-nodejs16
Vendor:  cPanel, Inc.
Summary: Node.js 16
Version: 16.15.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group:   Development/Languages
URL:  https://nodejs.org
Source0: https://nodejs.org/dist/v%{version}/node-v%{version}-linux-x64.tar.gz

Provides: ea4-nodejs
Conflicts: ea4-nodejs
# Because old ea-nodejs10 does not have ^^^ and DNF wants to solve ^^^ by downgrading ea-nodejs10
Conflicts: ea-nodejs10

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

%prep
%setup -qn node-v%{version}-linux-x64

%build

# nodejs now has support for Microsoft Powershell, since that is not relevant
# to any of our deployed systems, I am removing them so they do not
# automatically require powershell, causing a dependency issue

cat > remove_pwsh.pl <<EOF
use strict;
use warnings;

my @files = split (/\n/, \`find . -type f -print\`);

foreach my \$file (@files) {
    my \$first_line = \`head -n 1 \$file\`;
    if (\$first_line =~ m/env\s+pwsh/) {
        print "Removing file \$file\n";
        unlink \$file;
    }
}
EOF

/usr/bin/perl remove_pwsh.pl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs16
cp -r ./* $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs16

cd $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs16
for file in `find . -type f -print | xargs grep -l '^#![ \t]*/usr/bin/env node'`
do
    echo "Changing Shebang (env) for" $file
    sed -i '1s:^#![ \t]*/usr/bin/env node:#!/opt/cpanel/ea-nodejs16/bin/node:' $file
done

mkdir -p %{buildroot}/etc/cpanel/ea4
echo -n /opt/cpanel/ea-nodejs16/bin/node > %{buildroot}/etc/cpanel/ea4/passenger.nodejs

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
/opt/cpanel/ea-nodejs16
/etc/cpanel/ea4/passenger.nodejs
%attr(0755,root,root) /opt/cpanel/ea-nodejs16/bin/*


%changelog
* Wed Apr 27 2022 Cory McIntire <cory@cpanel.net> - 16.15.0-1
- EA-10667: Update ea-nodejs16 from v16.14.2 to v16.15.0

* Tue Mar 22 2022 Travis Holloway <t.holloway@cpanel.net> - 16.14.2-1
- EA-10588: Update ea-nodejs16 from v16.13.1 to v16.14.2

* Tue Dec 07 2021 Dan Muey <dan@cpanel.net> - 16.13.1-2
- ZC-9571: Explicitly conflict w/ `ea-nodejs10` so that DNF does not simply downgrade it to get around the conflict

* Thu Dec 02 2021 Julian Brown <julian.brown@webros.com> - 16.13.1-1
- ZC-9550 - Create package

