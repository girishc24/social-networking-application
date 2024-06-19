# Social Networking Application

Creating an API for a social networking application using Django Rest Framework with all the necessary functionalities.

## Prerequisites

- Python (version 3.x recommended)
- Django
- Django REST Framework
- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the repository

First, you need to clone the repository to your local machine. You can do this using the following command:

```bash
git clone https://github.com/girishc24/social-networking-application.git
cd social-networking-application
```
### 2. Create a virtual environment

Create a virtual environment to install the project dependencies. This helps in maintaining project-specific dependencies and avoiding conflicts with other projects.

- For Linux/Mac:
```
python -m venv venv
source venv/bin/activate
```
- For Windows:
```
python -m venv venv
venv\Scripts\activate
```
### 3. Install dependencies

With the virtual environment activated, install the required dependencies using the requirements.txt file:
```
pip install -r requirements.txt
```
### 4. Database setup
Before running the application, set up the database by running the migrations:
```
python manage.py makemigrations
python manage.py migrate
```
### 5. Run the development server
Start the Django development server to test the application locally:
```
python manage.py runserver
```
You can now access the application at http://localhost:8000.

## Docker Setup
The repository includes Docker files (Dockerfile and docker-compose.yml) for containerizing the application. Follow these steps to set up and run the application using Docker:

### 1. Build and Run the Docker Container
To build the Docker image and run the container, use Docker Compose:
```
docker-compose up --build
```
This command will build the Docker image according to the Dockerfile and start the Django development server inside a Docker container. The application will be accessible at http://localhost:8000.

### 2. Stop the Docker Container
To stop the running Docker containers, use the following command:
```
docker-compose down
```


