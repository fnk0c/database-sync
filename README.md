<div id="top"></div>

<h3 align="center">Database Sync</h3>

## Getting Started

This guide outlines the necessary steps to set up and use the Database Sync tool. Please ensure you follow all steps in the order presented for a successful setup.

### Bare-metal Setup Instructions

#### Prerequisites

Before proceeding with the installation, ensure the following prerequisites are met:

- **Docker**: Version 18.09 or higher. [Install Docker](https://docs.docker.com/install)
- **Python**: Version 3.9 or higher. [Install Python](https://www.python.org/downloads/)
- **PDM**: Version 2.11.2 or higher. [Install PDM](https://pdm-project.org/latest/#installation)
- **pg_dump**: Version 15. [Install pg_dump](./INSTALL_PG_DUMP.md)
- **psycopg2**: Version 2.9.9. [Install psycopg](https://www.psycopg.org/docs/install.html)

### Installation Guide

### 1. Clone the Repository

Use the following command to clone the database-sync repository from GitLab:

```shell
git clone git@github.com:fnk0c/database-sync.git
```

### 2- Install the application

Navigate to the cloned repository's directory and run the following command to install the necessary dependencies:

```shell
pdm install
```

### 3- Create the .env file

In the root directory of your project, create a .env file. This file will store your environment variables.

### 4- Execute the application

Start the application by running:

```shell
pdm start
```

By following these steps, you should have the Database Sync application up and running on your system.
