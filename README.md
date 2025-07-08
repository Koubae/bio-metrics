bio-metrics
===========

Distribuited Web Application Software to collect manage and admin Biological samples.

This is a collection of multiple microservices and tools that helps you manage Biological samples metrics and so on.
The prooject at the moment is small so the different microservice's repository are located within this same repository for ease 
but they could move to their separate repository if this grows (if that happesn this repository could still be the main one having each service as [Git Submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules))

Check **[Architecture](./docs/Architecture.MD)** for more details.


QuickStart
----------

### Database

```bash
make db-up
make db-down
mak db-shell
```

#### PgAdmin (optional)


* PgAdmin: http://localhost:5050/browser/
* email:  admin@example.com
* password: admin

When requested to login in server `Bio Metrics DB` use again password `admin`.