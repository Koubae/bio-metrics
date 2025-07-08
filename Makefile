# ============================
#       Docker
# ============================
up:
	@docker compose up

down:
	@docker compose down

build:
	@echo 'Building images ...🛠️'
	@docker compose build

# ////////////////////
#		DB -- PostGRESQL
# ////////////////////
db-up:
	@docker compose up pgadmin
db-down:
	@docker compose down pgadmin
db-down-clean-up:
	@docker compose down -v pgadmin

db-shell:
	docker exec -it bio-metrics-db psql -Uadmin -didentity
