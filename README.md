# Email Manager

Automated Email Sender is a robust application built using `Python` and the `FastAPI` framework, designed to streamline email communications. 
Leveraging `Google Gmail API` for email delivery, this app automates the process of sending emails to large client lists efficiently.

# Key Features:

- `FastAPI Framework`: A high-performance backend for handling **API** requests.
- `Google Gmail Integration`: Seamlessly send emails using **Gmail’s API**.
- Task Queue Management: Utilizes `Celery` and `Redis` to manage and scale email sending tasks. The app sends emails at different times, mimicking manual sending.
- `HTML Template Support`: Choose from various `HTML` templates for customized email content.
- Email History and Client Data Management: `PostgreSQL` database with `SQLAlchemy` for storing email history and client information.
- `JWT Authentication`: Secure user access with **Web Tokens**.
- `Google Authentication`: Integrated OAuth2 flow for obtaining Gmail tokens directly within the app.

# Getting Started:

- Set Up Environment Variables. Create a .env file in the root directory and fill it with the following environment variables from `.env.example`.
- Start the Application. Use **Docker Compose** to build and run the application: `docker-compose up --build`
- Create **user** in App.
- You need to set up an account with the **Google Gmail API**, authorize within the app, and generate the **Token**. The **token** will be saved inside the application for further use. If the token expires, the app will let you know.

# Endpoints:

- `/address_list`: Allows you to manipulate a list of email addresses.
- `/newsletter`: Allows you to manipulate newsletters, view the history of newsletters, repeat them or delete them.
- `/templates`: Allows you to manipulate create HTML templates to organize your email, adding personality to each mailing.
- `/tokens`: Allows you to generate a token to access Google API functionality.
- `/send-mail`: The main point that allows you to initalize your mailing list. 

You can learn more about the functionality using the **OpenAPI** documentation: `/docs`
