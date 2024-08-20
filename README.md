# GuidBot

### Migration

1) alembic init -t async alembic
2) alembic init -t sync alembic

3) alembic revision --autogenerate -m "init models" (makemigrations)
4) alembic upgrade head (migrate)
5) alembic downgrade -1/base