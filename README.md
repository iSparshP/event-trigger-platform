# Event Trigger Platform (Segwise.ai)

A robust platform for managing scheduled and API-based event triggers with automatic retention and archival capabilities.

## Architecture

![Image](https://github.com/user-attachments/assets/1340ada4-c17e-418d-a6fa-6c03deba30e1)

## Features

### Core Features
- **Multiple Trigger Types**
  - Scheduled Triggers (one-time and recurring)
  - API Triggers with schema validation
  - Manual Testing capability for both trigger types
- **Event Management**
  - Comprehensive event logging
  - 2-hour active retention with 46-hour archive
  - Automatic cleanup after 48 hours
- **Security & Performance**
  - Basic Authentication
  - Redis-based caching for high-performance event log retrieval
  - Event aggregation with count analytics
- **User Interface**
  - Basic UI for trigger management
  - Swagger/OpenAPI documentation
  - Event log visualization


## Environment Variables

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `ENVIRONMENT`: development/production
- `PORT`: Application port (default: 8000)
- `REDIS_URL`: Redis connection string (default: redis://redis:6379/0)

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- Docker
  

## Local Setup

### Prerequisites
- Docker
- Docker Compose

### Installation Steps

1. Clone the repository
```bash
git clone https://github.com/yourusername/event-trigger-platform.git
cd event-trigger-platform
```

2. Create .env file (use example provided)
```bash
cp .env.example .env
```

3. Start the application using Docker Compose
```bash
docker-compose up -d
```

4. Access the application:
- API Docs: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/docs

## API Documentation

## Authentication
### Token Request
```http
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin
```

### Response
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## Triggers

### Create Trigger
```http
POST /api/v1/triggers
Content-Type: application/json
```

#### Scheduled Trigger (One-time)
```json
{
    "type": "scheduled",
    "schedule": "2024-02-20T10:00:00Z",
    "recurring": false
}
```

#### Scheduled Trigger (Recurring)
```json
{
    "type": "scheduled",
    "recurring": true,
    "recurring_pattern": "*/30 * *"
}
```

#### API Trigger
```json
{
    "type": "api",
    "api_schema": {
        "required_fields": ["event_name", "payload"]
    }
}
```

### Test Trigger
```http
POST /api/v1/triggers/{trigger_id}/test
```

#### Response
```json
{
    "message": "Test trigger executed",
    "event_id": "uuid-of-event"
}
```

## Events

### List Events
```http
GET /api/v1/events
```

#### Query Parameters
- `status`: active|archived
- `aggregate`: true|false
- `hours`: int (default: 48)

#### Response
```json
{
    "events": [
        {
            "id": "uuid",
            "trigger_id": "trigger-uuid",
            "status": "active",
            "triggered_at": "2024-02-16T10:00:00Z",
            "payload": {},
            "is_test": false
        }
    ]
}
```

## Event Retention Policy
- **Active State**: 2 hours
- **Archived State**: 46 hours
- **Total Retention**: 48 hours
- Events are automatically moved to archived state after 2 hours
- Archived events are permanently deleted after 46 hours in archived state


## Development

### Project Structure
```
event-trigger-platform/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
├── docker-compose.yml
└── Dockerfile
```

### Running Tests
```bash
docker-compose run --rm app pytest
```

## Assumptions
1. Free tier services are sufficient for the given load (5 queries/day)
2. Simple JSON schema validation is adequate for API triggers
3. Basic authentication is sufficient for MVP
4. In-memory caching with Redis is suitable for event log performance

## Credits and Tools Used
- **Framework**: FastAPI (https://fastapi.tiangolo.com/)
- **ORM**: SQLAlchemy
- **Task Scheduler**: APScheduler
- **Caching**: Redis
- **Development Tools**:
  - Docker
  - pytest for testing
  - Black for code formatting
  - flake8 for linting

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request
