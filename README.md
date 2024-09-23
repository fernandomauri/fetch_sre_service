# Fetch SRE Service

This microservice acts as a monitoring tool in that it pings given HTTP endpoints every 15 seconds.

## Prerequisites

#### Implementation 1 (Using Docker):
- Docker

#### Implementation 2 (Local machine):
- Python 3
- Python Libraries: requests, PyYAML


## Setting Up

#### Implementation 1:
After cloning this codebase and having Docker set up, make sure that you're in the working directory and have the Docker daemon running.
Then run the following command in your terminal to create a Docker image of the microservice:

```bash
docker build -t fetch_sre_service .
```

#### Implementation 2
After cloning this codebase and having Python (and dependent libraries) installed, make sure that you're in the working directory.

## Running the Service

#### Implementation 1
We will want to create and run a container from this image to start the service. Run the following command in your terminal:

```bash
docker run -it fetch_sre_service
```

[!WARNING] If you omit the "-it" tag, you'll get an EOF error.

Once the container starts, it runs the microservice and prints availability information to the console every 15 seconds.

#### Implementation 2
Run the Python microservice by running the following command in your terminal:

```bash
python3 fetch.py
```

The service should start making HTTP requests to the endpoints and print availability information to the console every 15 seconds.
