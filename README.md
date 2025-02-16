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

## Tech Stack
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Caching**: Redis
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker
- **UI**: Swagger

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
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Admin Panel: http://localhost:8000/admin

## API Documentation

### Authentication
All API endpoints require Basic Authentication
```bash
Authorization: Bearer <your_token>
```

### 1. Create Scheduled Trigger
```bash
POST /api/v1/triggers/scheduled
Content-Type: application/json

{
    "type": "scheduled",
    "schedule": {
        "type": "one_time",  // or "recurring"
        "time": "2024-02-20T10:00:00Z",
        "interval_minutes": 30  // required only for recurring
    },
    "description": "Daily data sync"
}

Response:
{
    "trigger_id": "12345",
    "status": "created",
    "next_execution": "2024-02-20T10:00:00Z"
}
```

### 2. Create API Trigger
```bash
POST /api/v1/triggers/api
Content-Type: application/json

{
    "type": "api",
    "schema": {
        "required_fields": ["event_name", "payload"],
        "validation_rules": {
            "event_name": "string",
            "payload": "object"
        }
    },
    "description": "Payment webhook"
}

Response:
{
    "trigger_id": "12346",
    "status": "created",
    "endpoint": "/api/v1/triggers/12346/execute"
}
```

### 3. Test Trigger
```bash
POST /api/v1/triggers/{trigger_id}/test
Content-Type: application/json

{
    "payload": {
        // Trigger specific payload
    }
}

Response:
{
    "test_id": "test_12345",
    "status": "executed",
    "timestamp": "2024-02-16T10:22:41Z"
}
```

### 4. Get Event Logs
```bash
GET /api/v1/events
Query Parameters:
- status: active|archived (default: active)
- aggregate: true|false (default: false)
- trigger_id: optional filter

Response:
{
    "events": [
        {
            "event_id": "evt_12345",
            "trigger_id": "12345",
            "type": "scheduled",
            "execution_time": "2024-02-16T10:22:41Z",
            "status": "success",
            "payload": {},
            "is_test": false
        }
    ],
    "total_count": 1,
    "aggregated_count": null  // present when aggregate=true
}
```

## Event Retention Policy
- **Active State**: 2 hours
- **Archived State**: 46 hours
- **Total Retention**: 48 hours
- Events are automatically moved to archived state after 2 hours
- Archived events are permanently deleted after 46 hours in archived state

## Deployment

### Deployed URL
[Add your deployment URL here]

### Deployment Instructions
1. Fork the repository
2. Set up free tier services:
   - Heroku/Railway for application hosting
   - ElephantSQL for PostgreSQL
   - Redis Labs for Redis cache
3. Configure environment variables
4. Deploy using provided Dockerfile

## Cost Estimation (30 days, 5 queries/day)
- **Compute (Heroku Free Tier)**: $0
- **Database (ElephantSQL Free Tier)**:
  - Storage: 20MB included
  - Connections: 5 concurrent
  - Cost: $0
- **Redis Cache (Redis Labs Free Tier)**:
  - Storage: 30MB included
  - Connections: 30
  - Cost: $0
**Total Monthly Cost**: $0 (Using free tiers)

## Development

### Project Structure
```
event-trigger-platform/
├── api/
│   ├── routes/
│   ├── models/
│   └── services/
├── core/
│   ├── config.py
│   └── database.py
├── tests/
├── docker/
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
