# Termius PPA
![Termius brand](https://assets.website-files.com/5c7036349b5477bf13f828cf/5cc7dff32d982e28cd8e99f3_termius_fb_logo.png)

A package manager that downloads the latest Termius `.deb` file available from official website

# Installation
Full installation tutorial available at: https://blog.javinator9889.com/termius-ppa. The blog
is constantly updated and contains latest fixes (if any). Here is the same procedure but
not as much explanatory as the blog itself.

* * * 

## Motivation

[Termius](https://termius.com/) is the #1 cross-platform terminal for 
Windows, macOS, Linus, iOS, and Android with built-in ssh client which 
works as your own portable server management.

Currently, Termius is available for downloading for all platforms but, in
Linux, it is only available for downloading as a raw .deb file or using
the Snap Store, without any official PPA. As some users are against the
Snap Store (due to its limitations, restrictions and policies), this 
repository aims to provide an easy solution for all users who want to have
Termius installed and upgradeable.

## How it works?

On the one hand, Termius is available for downloading from the official
website, using the following URL: 
https://www.termius.com/download/linux/Termius.deb

With that in mind, the file `lookup-server.py` just runs every fifteen
minutes and downloads the latest .deb file provided by that link. Then, 
using the `reprepro` program, the PPA is updated and, if a new version is
available, served to the users.

In that way, the PPA is always up-to-date (with a delay of at most 15
minutes), and the end-user can have the stable installation of Termius
(or beta one) in their computers.

## Installation

Firstly, we need to **import** the GPG repository keys:

```shell script
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 08633B4AAAEB49FC
```

Then, add the repository to your `sources.list` as follows:

+ For the *stable* version, use the `all` distribution.
+ For the *beta* version, use the `public-beta` distribution.
+ You can use HTTPS if you want.

```shell script
# Stable repository
sudo add-apt-repository "deb [arch=amd64] https://ppa.javinator9889.com all main"

# Beta repository
sudo add-apt-repository "deb [arch=amd64] https://ppa.javinator9889.com public-beta main"
```

Finally, update and install Termius:

```shell script
sudo apt update && sudo apt install termius-app

# If using public beta, install as follows:
sudo apt install termius-beta
```

You can browse the repository at the following URL:
https://ppa.javinator9889.com

## Upgrading

For upgrading Termius, it is as simple as running the `apt update` and `apt
 upgrade` commands:
 
```shell script
sudo apt update && sudo apt upgrade
```

## Uninstalling Termius and repository

If you would like to remove Termius from your computer and remove the repository
from your `sources.list`, run the following commands:

```shell script
sudo apt remove termius-app
# If using public beta, uninstall as follows
sudo apt remove termius-beta

# Remove the repository using the add-apt-repository command
# Keep in mind it must be the same as you added (stable, beta, etc.)
sudo add-apt-repository -r "deb [arch=amd64] https://ppa.javinator9889.com all main"

# Finally, remove the key if you want not to trust it anymore
sudo apt-key del 08633B4AAAEB49FC
```

## License

```
                                Termius PPA
                    Copyright (C) 2021  Javinator9889

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
