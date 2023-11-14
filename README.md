# FastApi-Social-Media-App

A social media application to posts, comment, react and reply.

# Overview

A social media application to posts, comment, react and reply.

# Prerequisites

Make sure you have Docker installed on your machine. You can download Docker from [here](https://www.docker.com/get-started/).

# Getting Started

## Clone the repository

- git clone https://github.com/EskinderAbera/SocialApp.git
- cd SocialApp

## Create Postgres DB

- create postgres database.
- cd SocialApp
- rename .env.example to .env file
- add postgresql url in to the .env file

## Build and run the docker

- cd SocialApp/
- run docker-compose up --build

## Access the Application

Once the container is up and running, you can access the FastAPI application at
http://127.0.0.1:8040 in your web browser.

# Stopping the Application

To stop the running Docker container, use the following command:
docker-compose down

# Swagger and FastAPI

visit http://127.0.0.1:8040/docs

# Customization

Feel free to customize the FastAPI application code to suit your needs. Additionally, you can modify the Dockerfile if you have specific requirements for your Docker image.
