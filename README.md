# Fetch SRE Service

This microservice acts as a monitoring tool in that it pings given HTTP endpoints every 15 seconds.
Endpoint data comes from a YML file that the user chooses.
This repo currently has one YML file (sample_file.yml), but users can add
additional YML files to the working directory to run the service against.

## Prerequisites

- Docker (Install for your OS here: https://docs.docker.com/desktop/)


## Setting Up

After cloning this codebase and having Docker set up, make sure that you're in the working directory and have the Docker daemon running.
Then run the following command in your terminal to create a Docker image of the microservice:

```bash
docker build -t fetch_sre_service .
```


## Running the Service

We will want to create and run a container from this image to start the service. Run the following command in your terminal:

```bash
docker run -it fetch_sre_service
```
**WARNING**
If you omit the "-it" tag, you'll get an EOF error.


Once the container starts, it runs the microservice and prints availability information for each domain to the console every 15 seconds.
