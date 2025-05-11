# Notes App API

A FastAPI-based backend for a notes application with secure authentication via username/password or OTP (email or phone).

## Features

- JWT-based login
- OTP verification (email + Twilio SMS)
- Password reset via email or phone
- Modular and scalable FastAPI structure

## Getting Started

1. Clone this repo
2. Create a virtual environment and install dependencies:
```pip install -r requirements.txt```

3. Set up your `.env` file with appropriate credentials.
4. Run the app:
```uvicorn app.main:app --reload```


## Project Structure

Refer to the codebase and `/app` directory for structure and responsibility of each module.
