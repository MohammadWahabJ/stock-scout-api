# Stock Scout API

A FastAPI-based application that provides stock tracking and analysis functionalities. This project includes a PostgreSQL database for managing data and Alembic for database migrations.

## Features

- **FastAPI**: High-performance API framework based on Python 3.11
- **PostgreSQL**: Relational database for managing data
- **Alembic**: Database migrations
- **Docker**: Containerized environment for easy setup
- **Uvicorn**: ASGI server for serving FastAPI
- **Alembic migrations**: Database versioning and schema changes

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.11 installed if running without Docker

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MohammadWahabJ/stock-scout-api.git
    cd stock-scout-api
    ```

2. Create a `.env` file or export the required environment variables:

    ```bash
    cp .env.example .env
    ```
3. Build the Docker containers:

    ```bash
    docker-compose build

### Running the Application

1. Start the application:

    ```bash
    docker-compose up
    ```

2. The FastAPI app will be available at `http://localhost:8000`.

3. You can access the interactive API documentation at `http://localhost:8000/docs`.

### Running Migrations

Alembic is used to handle database migrations. When the application starts, it will automatically run migrations.

If you need to run migrations manually, use the following command:

```bash
docker-compose exec api alembic upgrade head   
```
