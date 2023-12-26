# Multiplication Game Web Application

## Overview
This web application is a simple yet interactive multiplication game that includes user authentication and score tracking. It is built using Python with `wsgiref` for server functionality and `sqlite3` for database management.

## Features

**User Authentication:**
- Users can register with a username and password.
- User login functionality with username and password validation.
- User logout feature that clears the session.

**Multiplication Game:**
- Once logged in, users are presented with random multiplication questions.
- Users can choose their answers, and the application will track correct and wrong responses.
- The application maintains a score (correct and wrong answers) using cookies.

**Persistent Data:**
- User credentials and game data are stored in a SQLite database (`users.db`).

**Simple Web Interface:**
- Basic HTML forms for login, registration, and game interaction.

## Requirements

- Python 3
- SQLite3

## Usage

1. Start the web server by running the script:
   ```bash
   python multiplication.py
