# Cosmic Cycles

Cosmic Cycles is a web application that helps users understand the different cycles of their lives, based on the book "Self Mastery and Fate with the Cycles of Life" by H. Spencer Lewis. The application calculates and displays various cycles, such as the daily, yearly, human life, soul, and business cycles, providing users with insights and suggestions for each period.

## Features

*   **User Authentication:** Users can sign up, log in, and manage their profiles.
*   **Personalized Cycles:** The application calculates personalized cycles based on the user's date of birth and other significant dates.
*   **Dashboard:** Authenticated users have a personalized dashboard that displays all their cycles in one place.
*   **Daily Cycle:** Non-authenticated users can view the current daily cycle.
*   **Business Cycles:** Users can add their businesses and track their business cycles.
*   **Cycle Templates:** The application uses pre-defined templates for each cycle, which include descriptions, principles, and suggestions for each period.
*   **API Endpoints:** The application provides API endpoints to retrieve cycle data in JSON format.

## Recent Changes

*   **Daily Cycle for All:** The daily cycle is now the default home page and is accessible to all users, authenticated or not.
*   **About Page:** A new "About" page has been added to explain the purpose and principles of the application, with references to the book "Self-Mastery and Fate with the Cycles of Life" by H. Spencer Lewis.
*   **UI/UX Refinements:** The user interface has been refined for better mobile compatibility and a more consistent user experience across the application.
*   **Favicon:** A favicon has been added to the project.
*   **Bug Fixes:** Fixed a bug where the profile update API URL was not being resolved correctly.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.10 or higher
*   Node.js and npm

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/cosmic-cycles.git
    cd cosmic-cycles
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install the npm dependencies:**

    ```bash
    npm install
    ```

5.  **Run the initial database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Run the Tailwind CSS build process:**

    ```bash
    python manage.py tailwind install
    python manage.py tailwind build
    ```

### Running the Application

To start the development server, run the following command:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Usage

1.  **Sign up for a new account:** Go to the signup page and create a new user account.
2.  **Log in:** Log in with your new account.
3.  **Edit your profile:** Go to the dashboard and edit your profile to add your date of birth and other significant dates.
4.  **View your cycles:** The dashboard will display all your personalized cycles.
5.  **Add a business:** Go to the business page to add your businesses and track their cycles.

## Technology Stack

*   **Backend:**
    *   Python 3
    *   Django 4.2
    *   Django REST Framework (for APIs)
*   **Frontend:**
    *   HTML5
    *   Tailwind CSS
    *   JavaScript
*   **Database:**
    *   SQLite (for development)
    *   PostgreSQL (recommended for production)

## Project Structure

```
cosmic-cycles/
├── .venv/                     # Virtual environment files
├── cycle_project/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── cycles/                    # Core application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   ├── templates/
│   └── ...
├── theme/                     # Tailwind CSS theme app
│   ├── static_src/
│   └── ...
├── static/                    # Static files (CSS, JS, images)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── ...
```

## API Endpoints

The application provides the following API endpoints:

*   `/api/user_cycle/human/`: Returns the human life cycle data for the logged-in user.
*   `/api/user_cycle/<str:cycle_type>/`: Returns the cycle data for the specified cycle type.

## Preparing for Production

Before deploying the application to a production environment, you should make the following changes:

1.  **`SECRET_KEY`:** Set the `SECRET_KEY` setting to a long, random string and load it from an environment variable.
2.  **`DEBUG`:** Set the `DEBUG` setting to `False`.
3.  **`ALLOWED_HOSTS`:** Add your production domain name to the `ALLOWED_HOSTS` list.
4.  **Database:** Switch from SQLite to a more robust database like PostgreSQL.
5.  **Static Files:** Run `python manage.py collectstatic` to collect all static files into the `STATIC_ROOT` directory.
6.  **Web Server:** Use a production-ready web server like Gunicorn or uWSGI.

