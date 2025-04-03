# Super Heroes API

This project is a Flask-based API for managing superheroes, their powers, and their relationships. It uses SQLAlchemy for database interactions and Flask-Migrate for database migrations.

## Features

- **Heroes Management**: Create, read, and manage superheroes.
- **Powers Management**: Create, read, update, and manage superhero powers.
- **Hero Powers**: Assign powers to heroes with varying strengths.

## Endpoints

### Heroes
- `GET /heroes`: Retrieve a list of all heroes.
- `GET /heroes/<int:hero_id>`: Retrieve details of a specific hero, including their powers.

### Powers
- `GET /powers`: Retrieve a list of all powers.
- `GET /powers/<int:power_id>`: Retrieve details of a specific power.
- `PATCH /powers/<int:power_id>`: Update the details of a specific power.

### Hero Powers
- `POST /hero-powers`: Assign a power to a hero with a specified strength.

## Database Models

### Hero
- `id`: Integer, primary key.
- `name`: String, required.
- `super_name`: String, required.

### Power
- `id`: Integer, primary key.
- `name`: String, required.
- `description`: String, required (minimum 20 characters).

### HeroPower
- `id`: Integer, primary key.
- `strength`: String, required (must be "Strong", "Weak", or "Average").
- `hero_id`: Foreign key to `Hero`.
- `power_id`: Foreign key to `Power`.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Super_Heroes