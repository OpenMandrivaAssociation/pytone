%define name	pytone
%define version 3.0.3
%define release 2

Summary:	Mp3/ogg mixer for DJ's
Name:		%name
Version:	%version
Release:	%release
Group:          Sound
License:	GPLv2
URL:		http://www.luga.de/pytone/
Source:		http://www.luga.de/pytone/download/PyTone-%version.tar.gz
Requires:	pyogg pyvorbis pymad pyao
BuildRequires:  python-devel
BuildRequires:  libao-devel

%description
PyTone is a music jukebox written in Python with a curses based
GUI. While providing advanced features like crossfading and multiple
players, special emphasis is put on ease of use, turning PyTone into an
ideal jukebox system for use at parties.

%prep
%setup -q -n PyTone-%version

%build
%__python setup.py build_ext -i

%install
# TODO try --prefix next time.
%__python setup.py install --root %buildroot
%__install conf/pytonerc -D %buildroot/%_datadir/%name/pythonerc

# Lets make a wrapper.
%__install -d %buildroot/%_bindir
cat << EOF > %buildroot%_bindir/%name
#!/bin/sh
if [ ! -d ~/.pytone ]; then
   echo 'Creating pytone configuration directory: ~/.pytone'
   %__install -d ~/.pytone
fi

if [ ! -e ~/.pytone/pytonerc ]; then
   echo 'Installing pytone configuration file: ~/.pytone/pytonerc'
   %__install  %_datadir/%name/pythonerc ~/.pytone/pytonerc
   echo
fi

if [ ! -e ~/.pytone/pytonectl ]; then
   touch ~/.pytone/pytonectl
   echo
fi

%__python %_libdir/python%pyver/site-packages/%name/pytone.py $@
EOF

# lets make another wrapper. Should be fixed in the next release.
cat << EOF_rpm > %buildroot%_bindir/%{name}ctl
#!/bin/sh
case \$@ in
    -h|--help)
        cat << EOF
pytonectl %version
Copyright (C) 2003 Jörg Lehmann <joerg@luga.de>
usage: pytonectl.py [options] command

Possible options are:
   -h, --help:              show this help
   -s, --server <hostname>: connect to PyTone server on hostname
   -p, --port <portnumber>: connect to PyTone server on given port
   -f, --file <filename>:   connect to PyTone UNIX socket filename

The supported commands are:
    playerforward:                  play the next song in the playlist
    playerpause:                    pause the player
    playerstart:                    start/unpause the player
    playerstop:                     stop the player
    playerratecurrentsong <rating>: rate the song currently being played (1<=rating<=5)
    playlistaddsongs <filenames>:   add files to end of playlist
    playlistaddsongtop <filename>:  play file immediately
    playlistclear:                  clear the playlist
    playlistdeleteplayedsongs:      remove all played songs from the playlist
    playlistreplay:                 mark all songs in the playlist as unplayed
    playlistshuffle:                shuffle the playlist

EOF
        ;;
        *)
            %__python %_libdir/python%pyver/site-packages/%name/pytonectl.py \$@
        ;;
esac
EOF_rpm

%find_lang PyTone

%files -f PyTone.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING PKG-INFO README TODO
%dir %python_sitearch/%name
%python_sitearch/%name/*
%python_sitearch/*.egg-info
%dir %_datadir/%name
%_datadir/%name/pythonerc

%defattr(755,root,root,755)
%_bindir/%name
%_bindir/%{name}ctl


%changelog
* Mon Nov 01 2010 Ahmad Samir <ahmadsamir@mandriva.org> 3.0.2-3mdv2011.0
+ Revision: 591602
- rebuild for python 2.7

* Sun Mar 28 2010 Funda Wang <fwang@mandriva.org> 3.0.2-2mdv2010.1
+ Revision: 528372
- rebuild

* Mon Feb 15 2010 Sandro Cazzaniga <kharec@mandriva.org> 3.0.2-1mdv2010.1
+ Revision: 506084
- update to 3.0.2

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 3.0.1-4mdv2010.0
+ Revision: 442551
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 3.0.1-3mdv2009.0
+ Revision: 242468
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Aug 15 2007 Funda Wang <fwang@mandriva.org> 3.0.1-1mdv2008.0
+ Revision: 63717
- fix file list
- New version 3.0.1
- Import pytone




* Sat Dec 17 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.3.0-2mdk
- Add BuildRequires : libao-devel

* Wed Oct 26 2005 Lenny Cartier <lenny@mandriva.com> 2.3.0-1mdk
- 2.3.0

* Tue Jun 21 2005 Lenny Cartier <lenny@mandriva.com> 2.2.4-1mdk
- 2.2.4

* Thu Apr 28 2005 Lenny Cartier <lenny@mandrakesoft.com> 2.2.3-1mdk
- 2.2.3

* Tue Feb 08 2005 Lenny Cartier <lenny@mandrakesoft.com> 2.2.1-1mdk
- 2.2.1

* Wed Feb 02 2005 Lenny Cartier <lenny@mandrakesoft.com> 2.2.0-1mdk
- 2.2.0

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 2.1.3-2mdk
- Rebuild for new python

* Tue Nov 30 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-1mdk
- 2.1.3

* Mon Nov 08 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.1.1-1mdk
- 2.1.1

* Thu Aug 05 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.1.0-1mdk
- 2.1.0

* Fri Jul 23 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.0.14-1mdk
- 2.0.14

* Mon Jun 14 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.0.13-1mdk
- 2.0.13

* Fri May 14 2004 Michael Scherer <misc@mandrake.org> 2.0.12-1mdk
- New release 2.0.12
- rpmbuildupdate aware

* Sun Feb 15 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.0.9-1mdk
- 2.0.9

* Mon Jan 19 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-1mdk
- 2.0.8

* Sat Dec 13 2003 Han Boetes <han@linux-mandrake.com> 2.0.6-1mdk
- New version.

* Fri Nov 28 2003 Han Boetes <han@linux-mandrake.com> 2.0.5-1mdk
- initial mandrake release
