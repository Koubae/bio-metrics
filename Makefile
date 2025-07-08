
# ============================
#       Docker
# ============================


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
	docker-compose exec -it bio-metrics-db psql -U admin
