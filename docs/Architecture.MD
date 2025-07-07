Architecture
============


**Note** The service is **intentionally** made into microservice for show-case how we could scale this project up. In a real world scenario we 
would likelly start with a Monolith and if really needed then split it into microservice.

Microservice **will add* complexitly and liability, they are by definition a tech-debt.

### Services

* `identity`    --> manages user logins, signup, user's account and permissisons
* `bio-samples` --> doctors will manage samples, bio-labs will get samples and produce results, the _patients_ will see their results and admins have acess to all

#### `identity`

![identity](image.png)

####  `bio-samples` 

![bio-samples](image-1.png)