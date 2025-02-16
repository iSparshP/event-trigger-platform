# Event Trigger Platform

A platform for managing scheduled and API-based event triggers.

## Features
- Scheduled triggers (one-time and recurring)
- API triggers with schema validation
- Event logging with retention
- Authentication
- Event aggregation

## Local Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/event-trigger-platform.git
cd event-trigger-platform
```

2. Run with Docker Compose
```bash
docker-compose up -d
```

3. Access the application at http://localhost:8000

## API Documentation

### Create Trigger
```bash
POST /api/v1/triggers
Content-Type: application/json

{
  "type": "scheduled",
  "schedule": "2024-02-20T10:00:00Z",
  "recurring": false
}
```

### Create API Trigger
```bash
POST /api/v1/triggers
{
  "type": "api",
  "api_schema": {
    "required_fields": ["name", "value"]
  }
}
```

## Cost Estimation (30 days, 5 queries/day)
- Compute (Free tier): $0
- Database (Free tier): $0
- Redis Cache (Free tier): $0
Total: $0 (Using free tiers)

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- React
- Docker

## Deployment
Deployed URL: [Add your deployment URL here]

## Credits
- FastAPI framework
- SQLAlchemy
- APScheduler
- React