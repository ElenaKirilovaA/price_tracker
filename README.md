# Tracky Deal (Simulation-Based Price Tracking System)

A Django web application that simulates product price tracking and alert triggering.

---

## Overview

This project demonstrates a backend architecture for handling price tracks, business logic separation, and state transitions between active and archived alerts.

Instead of **automatic** background monitoring, the system uses **manual price simulation** to trigger alert evaluation. This allows the focus to remain on:

- Clean service-layer design
- Query optimization
- Model managers
- State transitions
- Business rule encapsulation

---

## Core Features

- Create price track for products
- Manual simulation of price checks (edit price -> simulate button)
- Price track snapshot each time the price is checked
- Alert triggering when simulated price reaches target
- Send console notification
- Archive of triggered tracks
- Saved money calculation (started vs triggered price)
- Separation of concerns (views vs service layer)

---

## How It Works

1. A product has one or more active alerts.
2. Each alert stores:
   - target price
   - starting price
   - tracking state
3. When a price simulation is triggered:
   - All active alerts for that product are evaluated.
   - If `current_price <= target_price`:
     - The alert is archived.
     - A console notification is generated.
4. The track is archived.

---

## Tech Stack

- Python 3.11+
- Django
- PostgreSQL
- HTML / CSS

## Future improvement:
- Background price checks (Celery + Redis)
- Real email notifications
- User authentication system
- REST API layer
- Deployment to cloud platform

---
## Setup Instructions
1. Clone the repository.
```bash
git clone https://github.com/ElenaKirilovaA/price_tracker.git
cd price_tracker
```
2. Create a virtual environment:
```bash
python -m venv venv
source .venv/bin/activate
```
3. Install requirements.txt
```bash
pip install -r requirements.txt
```
4. Create .env file in the root of the project and copy from .env_copy and fill in with your own values
```bash
SECRET_KEY=your.secret_key
DB_NAME=your.db_name
DB_USER=your.db_user
DB_PASSWORD=your.db_password
HOST=your.host
PORT=your.port

```
5. Apply migrations 
```bash
python manage.py migrate
```
6. Run server
```bash
python manage.py runserver
```
---

## Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Create Track
![Add Track](screenshots/create_track.png)

### Simulation Track After Price Edit
![Products](screenshots/simulation.png)

### Archived Track Info
![Archived Track info](screenshots/track_history.png)


## Author

Elena Kirilova

