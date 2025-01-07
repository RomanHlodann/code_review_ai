# Code Review AI

## Overview
Code Review AI is a project designed to streamline the code review process using AI-powered tools. The application helps analyze repositories, extract meaningful insights, and provide recommendations to enhance the development workflow. This repository includes all the necessary components to set up and run the application locally or in a production environment.

## Requirements
Before starting, ensure you have the following installed on your system:

- Python 3.11+
- [Poetry](https://python-poetry.org/): Dependency management and packaging tool

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/code_review_ai.git
   cd code_review_ai
   ```

2. **Create a `.env` file**
   Create a `.env` file in the project root based on the `.env.sample` file provided:
   ```bash
   cp .env.sample .env
   ```
   Edit the `.env` file to include your environment variables (e.g., `GITHUB_ACCESS_TOKEN`).

3. **Configure Poetry to use in-project virtual environments**
   ```bash
   poetry config virtualenvs.in-project true
   ```

4. **Install dependencies**
   Use Poetry to install the project's dependencies:
   ```bash
   poetry install
   ```

5. **Run the application**
   Start the FastAPI application using Uvicorn:
   ```bash
   poetry run uvicorn src.code_review_ai.main:app --reload
   ```
   The app will be available at `http://127.0.0.1:8000/docs`.

## Project Structure
The repository is structured as follows:

```
code_review_ai/
├── .env.sample          # Example environment file
├── pyproject.toml       # Poetry configuration file
├── poetry.lock          # Dependency lock file
├── src/                 # Source code directory
│   ├── code_review_ai/  # Main application code
│   │   ├── __init__.py
│   │   ├── main.py      # FastAPI app entry point
│   │   ├── groq_request.py # Handle request to LLM
│   │   └── repo_handler.py # Repository handling logic
├── tests/               # Test suite
│   ├── test_repo_handler.py
│   └── other tests
└── README.md            # Project documentation
```

## Features
- Analyze repositories for code quality and style issues
- Extract files and provide structured outputs
- Easy integration with GitHub via Personal Access Token

## Testing
Run the tests using `pytest`:
```bash
poetry run pytest
```

## To improve this you can:

1. File Processing:
Instead of sending all files in a repository at once, implement a file batching mechanism that processes files incrementally. This avoids overloading the system and ensures smoother handling of large repositories.
Use pre-processing to identify only relevant files for analysis (e.g., source code files) and skip unnecessary ones like documentation or binary files.

2. Asynchronous Task Processing:
Introduce a task queue system using Celery or RabbitMQ to offload review requests. Each review request would become a job in the queue, processed asynchronously, which ensures scalability and smooth handling of traffic spikes.

3. Caching:
Implement caching for files or results that have already been analyzed. For example, if a file hasn't changed in a repository, reuse its previous analysis instead of re-processing it.
Use Redis or Memcached for quick access to cached data, reducing the burden on the AI model and improving response times.

4. Scalable Infrastructure:
Deploy the system on a cloud platform like AWS with auto-scaling groups to dynamically handle increased traffic. Use containerization (Docker) and Kubernetes to orchestrate multiple instances of the backend, allowing horizontal scaling.
Use serverless functions (e.g., AWS Lambda) for short-lived tasks like retrieving files from GitHub, reducing infrastructure costs for sporadic requests.
