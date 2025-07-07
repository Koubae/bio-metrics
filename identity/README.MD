Bio-Metrics -- Identity
=======================

Handles the user's identity of [bio-metrics](https://github.com/Koubae/bio-metrics)

### Requirements

* Linux (Ubuntu favorable)
* [GNU Make](https://www.gnu.org/software/make/manual/make.html) (see [Install Make](#install-make) in case needed.)

_If using only docker_

* `docker`
* `docker-compose`

_for local development_

* Python `3.13.5`


QuickStart
----------

### Without docker

```bash
# Install dependencies
make init-venv
# Run the application
make run
```

Development
-----------

### Code Quality

Run quality checks, formatters and so on:

```bash
make quality-checks
```

Check [Makefile](Makefile) in the section "Code Quality" for the whole set of commands

### Tests


```bash
# All
make tests
# unit
make unit
# integration
make integration
```


Troubleshooting
---------------

### Install Make

If you don't have a make, you should install it via

```bash
sudo apt-get install build-essential
```
