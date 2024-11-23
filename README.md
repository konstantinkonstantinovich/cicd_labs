# Matching Service



## Getting started
These instructions are valid for Mac or Linux.

You need to install following software:
* [Docker](https://docs.docker.com/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Prepare environment for development
Create .env file with the following command:
```bash
cp .env.example .env
```

## Usage
Build and run container using following command:
```bash
docker-compose up --build
```
For running in demon mode:
```bash
docker-compose up --build -d
```
