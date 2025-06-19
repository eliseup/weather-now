# 🌦️ Weather Now API

**Weather Now API** is a Django-based RESTful service that provides real-time weather data for cities using
the [OpenWeatherMap API](https://openweathermap.org/api). It offers endpoints to retrieve the current weather for a
given city, maintains a cache to reduce redundant external requests, stores a history of recent queries, and supports
rate limiting to protect from abuse.

---

## 🧰 Tech Stack

- **Redis** for caching
- **PostgreSQL** for data persistence
- **Celery** for asynchronous task execution
- **Docker** for containerization

---

---

## ⚙️ Main Technical Decisions

- **Django REST Framework**: Chosen for its robustness and ease of building RESTful APIs quickly.
- **PostgreSQL**: Used as the primary relational database to store weather queries and scheduled jobs reliably.
- **Redis**: Utilized both as a caching layer to reduce redundant external API calls and as the broker for Celery tasks.
- **Celery**: Handles asynchronous background tasks, such as scheduled weather data fetching, improving responsiveness and scalability.
- **Docker & Docker Compose**: Containerize the app and orchestrate dependencies like Redis and PostgreSQL for easy setup and consistent environments.
- **Modular Project Structure**: Separates core utilities, shared code, and domain-specific apps (`current_weather`) for better maintainability.
- **Rate Limiting**: Implemented using Django REST Framework’s throttling classes to prevent abuse.
- **Testing**: Combination of unit and integration tests with DRF’s `APITestCase` to ensure code quality and API correctness.

---

## 🚀 Getting Started

### 🔧 Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/eliseup/weather-now.git
   ```

---

### 🔧 Development Environment

After cloning the repository, follow these steps:

1. **Navigate to the `weather-now` directory**
   ```bash
   cd weather-now
   ```

2. **Start Development Containers**
    - To start the development environment, use the following command:
   ```bash
   docker compose -f docker/docker-compose-dev.yml up
   ```
    - To run the containers in the background, add the -d flag:
   ```bash
   docker compose -f docker/docker-compose-dev.yml up -d
   ```

In another terminal, access the containers:

3. **Access the application container**
   ```bash
   docker exec -it weather-now-app-1 bash
   ```   
    - **Apply migrations**
      ```bash
      python manage.py migrate
      ```

    - **Start the Django development server:**
      ```bash
      python manage.py runserver 0.0.0.0:8000
      ```  
    - **Run tests:**
      ```bash
      python manage.py test
      ```

**Port Mapping for Django Development Server**

- **Container Port**: `8000`
- **Host Port**: `8009`

The Django development server runs on port `8000` inside the Docker container. This port is exposed to the host machine on port `8009`

- Access the server **on the host machine** at `http://localhost:8009`


---

### 🔧 Production Environment

After cloning the repository, follow these steps:

1. **Navigate to the `weather-now` directory**
   ```bash
   cd weather-now
   ```

2. **Build the application Docker image**
   ```bash
   docker build -f docker/prod/app/Dockerfile -t weather-now-app-prod .
   ```

3. **Apply migrations**
   ```bash
   docker compose -f docker/docker-compose-prod.yml run --rm app bash -c "sleep 7 && python app/manage.py migrate"
   ```

4. **Start the Application**
   ```bash
   docker compose -f docker/docker-compose-prod.yml up
   ```

**Port Mapping for Production Application**

- **Container Port**: `8000`
- **Host Port**: `8080`

The production application runs on port `8000` inside the Docker container. This port is exposed to the host machine on port `8080`

- Access the application **on the host machine** at `http://localhost:8080`

---

# API Endpoints Documentation
*Production environment*

## Base URL
`http://localhost:8080/api`

---

## 1. **Retrieve current weather data for a given city**
**Endpoint**: `GET /weather`  
**Method**: `GET`  
**Description**:  
Fetches the current weather data for the provided city.  
If recent data exists in the cache, it is returned directly. Otherwise, a request is made to the OpenWeatherMap API and the result is stored and returned.

**Query Parameters**:
- `city` (required): Name of the city (e.g., `city=London`)

**Response (200)**:
```json
{
  "query_id": "c5e4d910-8bc2-4b12-9b90-a9bcae5a5cb0",
  "city": "London",
  "temperature": 18.5,
  "description": "light rain",
  "created_at": "2025-06-18T14:00:00Z",
  "status": "done"
}
```

## 2. **Schedule a weather data query (asynchronous)**
**Endpoint**: `GET /weather/schedule`  
**Method**: `GET`  
**Description**:  
Schedules a background task to fetch weather data for the specified city.
The returned data will have a query_id that can be used to retrieve the result later.

**Query Parameters**:
- `city` (required): Name of the city (e.g., `city=London`)

**Response (200)**:
```json
{
  "query_id": "c5e4d910-8bc2-4b12-9b90-a9bcae5a5cb0",
  "status": "pending"
}
```

## 3. **Retrieve the result of a scheduled weather query**
**Endpoint**: `GET /weather/result/<query_id>`  
**Method**: `GET`  
**Description**:  
Fetches the result of a previously scheduled weather query using the provided query_id.

**Response (200)**:
```json
{
  "query_id": "c5e4d910-8bc2-4b12-9b90-a9bcae5a5cb0",
  "city": "London",
  "temperature": 18.5,
  "description": "light rain",
  "created_at": "2025-06-18T14:00:00Z",
  "status": "done"
}
```

## 4. **List recent weather queries**
**Endpoint**: `GET /weather/history`  
**Method**: `GET`  
**Description**:  
Returns a list of the 10 most recent weather queries, ordered by most recent first.

**Response (200)**:
```json
[
  {
    "query_id": "c5e4d910-8bc2-4b12-9b90-a9bcae5a5cb0",
    "city": "London",
    "temperature": 18.5,
    "description": "light rain",
    "created_at": "2025-06-18T14:00:00Z",
    "status": "done"
  },
  {
    "query_id": "c5e4d910-8bc2-4b12-9b90-a98b8c8cc871",
    "city": "Paris",
    "temperature": 8.5,
    "description": "light rain",
    "created_at": "2025-06-18T14:00:00Z",
    "status": "done"
  }
]
```

---

## ⏳ What I Would Improve With More Time

- **Add authentication and user-based rate limiting** to better control API usage and secure endpoints.
- **Integrate Celery Beat** to schedule periodic weather data refreshes for popular or cached cities.
- **Improve API documentation** OpenAPI/Swagger docs.
- **Increase test coverage**, including edge cases and Celery task testing, to ensure robustness.
- **Optimize Docker configuration** for production deployment (multi-stage builds, gunicorn, etc.).

---

---

## ⚠️ Note about Production Environment

The production environment has **not been fully tested** in this project.  
It is included only to serve as a basic example or starting point.  

Further configuration and testing are needed before using it in a real production scenario.

---