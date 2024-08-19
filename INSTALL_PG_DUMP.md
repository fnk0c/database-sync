# PostgreSQL Client Installation Guide

This guide provides step-by-step instructions on how to install the PostgreSQL 15 client on your system using the official PostgreSQL APT repository. Follow these steps to ensure a successful installation.

## Prerequisites

- A machine running Ubuntu or a Debian-based Linux distribution.
- Access to a terminal and permission to execute `sudo` commands.

## Installation Steps

### 1. Update the APT Package Index

First, update your APT package index to make sure you have the latest list of available packages:

```shell
sudo apt update
```

### 2. Add the Official PostgreSQL APT Repository

Add the PostgreSQL official APT repository to your system to ensure you get the latest versions of PostgreSQL packages:

```shell
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

### 3. Update the APT Package Index Again

After adding the new repository, update your APT package index again to include the newly available PostgreSQL packages:

```shell
sudo apt update
```

### 4. Install PostgreSQL 15 Client

Now, install the PostgreSQL 15 client package:

```shell
sudo apt install postgresql-client-15
```

### 5. Verify the Installation

After the installation is complete, verify that the PostgreSQL client has been installed correctly by checking its version:

```shell
psql --version
```

You should see the version of the PostgreSQL client displayed, confirming that the installation was successful.
