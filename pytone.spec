%define name	pytone
%define version 3.0.2
%define release %mkrel 1

Summary:	Mp3/ogg mixer for DJ's
Name:		%name
Version:	%version
Release:	%release
Group:          Sound
License:	GPLv2
URL:		http://www.luga.de/pytone/
Source:		http://www.luga.de/pytone/download/PyTone-%version.tar.bz2
BuildRoot:	%_tmppath/%{name}-%{version}-%{release}-buildroot
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
rm -rf   %buildroot
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

%__python %_libdir/python%pyver/site-packages/%name/pytone.pyc $@
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
            %__python %_libdir/python%pyver/site-packages/%name/pytonectl.pyc \$@
        ;;
esac
EOF_rpm

%find_lang PyTone

%clean
rm -rf %buildroot

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
