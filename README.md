bio-metrics
===========

Distribuited Web Application Software to collect manage and admin Biological samples.

This is a collection of multiple microservices and tools that helps you manage Biological samples metrics and so on.
The prooject at the moment is small so the different microservice's repository are located within this same repository for ease 
but they could move to their separate repository if this grows (if that happesn this repository could still be the main one having each service as [Git Submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules))

Check **[Architecture](./docs/Architecture.MD)** for more details.


QuickStart
----------

### With Docker

```bash
make up
```

* identity:  http://127.0.0.1:2000 | Open API  http://127.0.0.1:2000/docs#/
* bio-samples: http://127.0.0.1:2001 | Open API http://127.0.0.1:20001/docs#/

I strongly suggest using PostMan Collection [docs/bio-metrcis.postman_collection.json](./docs/bio-metrcis.postman_collection.json)

Or alternatively:

#### 1) Signup + Login

```bash
### Sign up
curl --location 'localhost:20000/api/v1/auth/signup' \
--header 'Content-Type: application/json' \
--data '{
    "username": "user1",
    "password": "pass",
    "role": "doctor"
}'

### Login
access_token=$(curl --location 'localhost:20000/api/v1/auth/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "admin",
    "password": "pass"
}'| jq -r '.access_token');


```

#### 2) Create and Get Samples

```bash
# Create Sample
curl --location 'localhost:20001/api/v1/samples/' \
--header "Authorization: Bearer $access_token" \
--header 'Content-Type: application/json' \
--data '{
    "subject_id": 1,
    "sample_type":"blood",
    "status": "submitted",
    "storage_location": "fridge-lab-001",
    "sample_metadata": {"results": "some results", "values": "some blood values"
    }
}'

## Get Sample
curl --location --request GET 'localhost:20001/api/v1/samples/1' --header "Authorization: Bearer $access_token"

```


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