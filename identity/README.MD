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

```bash
make init-venv
```

Development
-----------

### Code Quality

Run quality checks, formatters and so on:

```bash
make quality-checks
```

Check [Makefile](Makefile) in section "Code Quality" for the whole set of commands


Troubleshooting
---------------

### Install Make

If you don't have a make, you should install it via

```bash
sudo apt-get install build-essential
```
