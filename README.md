# Test_case_Webtronics
Simple RESTful API using FastAPI for a social networking application

# How to run a project on your local machine?
1. Install Docker https://docs.docker.com/engine/install/
2. Rename dot_env to .env
3. Run `docker-compose up -d --build`
4. Create migrations by `docker-compose exec web alembic revision --autogenerate -m "init"`
5. Run migrations by `docker-compose exec web alembic upgrade head`
6. Open http://localhost:8080/docs/ in browser

