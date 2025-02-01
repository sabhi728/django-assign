# ASSIN FAQ API

ASSIN FAQ API is a Django-based RESTful service designed to manage Frequently Asked Questions (FAQs). It supports multi-language queries through Google Translate and leverages Redis for caching responses to enhance performance.

## Features

- **FAQ Management**: Create, retrieve, update, and delete FAQs.
- **Multi-language Support**: Translate FAQs into multiple languages using Google Translate.
- **Caching**: Use Redis to cache API responses and reduce load times.
- **Docker Integration**: Easily deploy using Docker and Docker Compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sabhi728/django-assign
   ```

2. Navigate to the project directory:
   ```bash
   cd assin
   ```

3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

The application will be accessible at `http://localhost:80`.

### Running Tests

To run the tests, use the following command:
```bash
pytest app/test.py
```

This will execute all the tests defined in the project. Ensure you have pytest installed and configured as per the `pytest.ini` file in the project.

## API Endpoints

### Retrieve FAQs

- **URL**: `/api/faqs/`
- **Method**: `GET`
- **Query Parameters**:
  - `lang`: Language code for translation (default is 'en').
  - `question`: Search term to filter FAQs.

```

### Environment Variables

- `DEBUG`: Django debug mode (`0` or `1`).
- `DJANGO_ALLOWED_HOSTS`: Host/domain names that this Django site can serve.
- `REDIS_URL`: URL of the Redis server.

### Technologies Used

- **Django** for the backend framework.
- **Django REST Framework** for creating RESTful APIs.
- **Google Translate** for translation services.
- **Redis** for caching responses.
- **Docker** for containerization and orchestration.
