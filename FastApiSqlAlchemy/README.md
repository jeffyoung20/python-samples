# FastApiSqlAlchemy 
Demonstrates a REST API for a SQL Database. The REST web service layer is implemented using the FastAPI and Pydantic python libraries. The data access layer is impelmented using SQLAlchemy

## Docker Deployment Steps
1. docker build -t fast-api-sa .
2. docker tag fast-api-sa jeffyoung20/fast-api-sa
3. docker push jeffyoung20/fast-api-sa
4. docker pull jeffyoung20/fast-api-sa
4. docker run --name FastApiSqlAlchemy -p 8081:80 -d jeffyoung20/fast-api-sa
