# StackIt – A Minimal Q&A Forum Platform

## Overview

StackIt is a minimal, user-friendly question-and-answer platform designed to foster collaborative learning and structured knowledge sharing. It provides a focused environment for communities to ask questions, provide detailed answers, and build a shared knowledge base.

## Core Features

*   **Question & Answer System:**
    *   Users can post questions with a title, a detailed description, and relevant tags.
    *   Users can provide answers to any existing question.
    *   Question owners can mark one answer as the "accepted" answer.

*   **Rich Text Editor:**
    *   Both question descriptions and answers can be formatted using a powerful rich text editor supporting:
        *   **Text Formatting:** Bold, Italic, Strikethrough
        *   **Lists:** Numbered and bulleted lists
        *   **Media:** Image uploads and emoji insertion
        *   **Links:** Hyperlink insertion
        *   **Alignment:** Left, Center, and Right text alignment

*   **Voting System:**
    *   Users can upvote or downvote answers to highlight the most helpful and relevant content.

*   **Tagging:**
    *   Questions are categorized using tags (e.g., `Python`, `Django`, `React`) for easy discovery and filtering.

*   **Notification System:**
    *   A real-time notification system keeps users engaged.
    *   Users receive notifications for:
        *   New answers to their questions.
        *   New comments on their answers or questions.
        *   Mentions via `@username`.
    *   An unread notification count is displayed on a bell icon in the navigation bar.

## User Roles & Permissions

| Role    | Permissions                                                                                             |
| :------ | :------------------------------------------------------------------------------------------------------ |
| **Guest** | Can view all public questions and answers.                                                              |
| **User**  | Can register, log in, post questions, post answers, comment, and vote on answers.                       |
| **Admin** | Has full moderation capabilities, including managing content (questions, answers) and banning users. |

## Tech Stack (Backend)

This repository contains the backend for the StackIt platform, built with:

*   **Framework:** Django & Django REST Framework
*   **Database:** PostgreSQL (recommended) or SQLite (for development)
*   **Authentication:** Token-based (e.g., JWT)

## API Documentation

*(A full API documentation (e.g., using Swagger or Redoc) will be available at an API endpoint like `/api/docs/` once the server is running.)*

Key API resources include:
*   `users/`
*   `questions/`
*   `answers/`
*   `tags/`
*   `comments/`
*   `votes/`

## Design & Mockups

The platform's UI/UX design and wireframes can be viewed on Excalidraw:
View Mockups

## Setup and Installation

To get the backend server running locally:

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd StackIT/server
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/`.

