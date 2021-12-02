%global debug_package %{nil}

Name:    ea-nodejs16
Vendor:  cPanel, Inc.
Summary: Node.js 16
Version: 16.13.1
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group:   Development/Languages
URL:  https://nodejs.org
Source0: https://nodejs.org/dist/v%{version}/node-v%{version}-linux-x64.tar.gz
Provides: ea4-nodejs
Conflicts: ea4-nodejs

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

%prep
%setup -qn node-v%{version}-linux-x64

%build
# empty build section since we're just putting the tarball's contents in place

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

#
# I was told to do this but I have no idea what to do with it
#
#%postrans
#
## Copied verbatim from ea-ruby24
## We will have to figure this out
#RESTART_NEEDED=""
#PERL=/usr/local/cpanel/3rdparty/bin/perl
#UPDATE_USERDATA='my ($y, $r)=@ARGV;my $u="";my $apps=eval {Cpanel::JSON::LoadFile($y)}; if ($@) { warn $@; exit 0 } for my $app (keys %{$apps}) { if(!$apps->{$app}{ruby}) { $apps->{$app}{ruby} = $r;if(!$u) { $u=$y;$u=~ s{/[^/]+$}{};$u=~s{/var/cpanel/userdata/}{}; } } } Cpanel::JSON::DumpFile($y, $apps);print $u'
#UPDATE_INCLUDES='my $ch="";my $obj=Cpanel::Config::userdata::PassengerApps->new({user=>$ARGV[0]});my $apps=$obj->list_applications();for my $name (keys %{$apps}) {my $data=$apps->{$name};if ($data->{enabled}) {$obj->generate_apache_conf($name);$ch++;}}print $ch;'
#
#for appconf in $(ls /var/cpanel/userdata/*/applications.json); do
#    REGEN_USER=$($PERL -MCpanel::JSON -e "$UPDATE_USERDATA" $appconf /opt/cpanel/ea-ruby24/root/usr/libexec/passenger-ruby24)
#
#    if [ ! -z "$REGEN_USER" ]; then
#        MADE_CHANGES=$($PERL -MCpanel::Config::userdata::PassengerApps -e "$UPDATE_INCLUDES" $REGEN_USER)
#
#        if [ ! -z "$MADE_CHANGES" ]; then
#            RESTART_NEEDED=1
#
#            if [ -x "/usr/local/cpanel/scripts/ea-nginx" ]; then
#                /usr/local/cpanel/scripts/ea-nginx config $REGEN_USER --no-reload
#            fi
#        fi
#    fi
#done
#
#if [ ! -z "$RESTART_NEEDED" ]; then
#   /usr/local/cpanel/scripts/restartsrv_httpd --restart
#
#   if [ -x "/usr/local/cpanel/scripts/ea-nginx" ]; then
#       /usr/local/cpanel/scripts/ea-nginx reload
#   fi
#fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
/opt/cpanel/ea-nodejs16
/etc/cpanel/ea4/passenger.nodejs
%attr(0755,root,root) /opt/cpanel/ea-nodejs16/bin/*


%changelog
* Thu Dec 02 2021 Julian Brown <julian.brown@webros.com> - 16.13.1-1
- ZC-9550 - Create package

