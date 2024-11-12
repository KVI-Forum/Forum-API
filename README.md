# Forum System

A web-based forum system that allows users to interact through categories, topics, and replies. This project is built with FastAPI and MySQL.
Note! This project is missing some functionality buttons . This is just a training project for our technical skills.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [Contributing](#contributing)

## Features

- User Authentication and Authorization
- Category and Topic Creation
- Message and Reply Threads
- User Access Management for Categories
- Topic Locking for Moderation
- Conversations and Messaging System

## Technologies Used

- **Backend**: FastAPI, Uvicorn
- **Database**: MySQL (MariaDB)
- **Tools**: MySQL Workbench for Database Design

## Installation

### Prerequisites

- Python and pip
- MySQL or MariaDB

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/KVI-Forum/Forum-System.git
   cd Forum-System/backend
2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
3. Set up the database:
   - Use MySQL Workbench or your preferred tool to import the provided SQL schema.
   - Configure database credentials in the backend configuration file.

4. Run the backend server:

   ```bash
   uvicorn main:app --reload
## Usage

- Register and log in as a user.
- Create or view categories, topics, and replies.
- Participate in conversations or private messages with other users.
- As a moderator, manage user access and lock categories or topics as needed.

## Database Structure

The forum system database consists of the following tables:

- **users**: Stores user information and credentials.
- **categories**: Defines different discussion areas.
- **topics**: Represents discussion threads within categories.
- **replies**: Stores user responses within topics.
- **messages**: Facilitates private conversations between users.
- **access**: Manages user permissions for categories.
- **member**: Keeps track of members added to specific categories.
- **votes**: Handles user votes on topics or replies.

## Contributing

Contributions are welcome! Please fork the repository and make a pull request with your proposed changes.
