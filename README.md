# FastAPI Vue Fullstack Documentation

## Overview

This project is a full-stack web application developed for a school project. It includes:
- **Backend**: A FastAPI application with SQLModel for handling the database (SQLite) and pydantic validation.
- **Frontend**: A Vue 3 application built with Vite and Vuetify, with Pinia for state management and Axios for API calls.

This documentation provides technical details about the project, including file structure, dependencies, configuration, and instructions on how to run it.

---

## Project Structure

The project consists of two main parts: **Backend** and **Frontend**.

### Backend (FastAPI)

The backend is implemented using FastAPI, with SQLModel for database management (SQLite) and pydantic for data validation. The API has endpoints for user management, authentication, and configuration settings.

**Directory Structure:**

```plaintext
backend/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── config.py
│   │   └── users.py
│   ├── core/
│   │   ├── deps.py
│   │   ├── jwt.py
│   │   ├── password.py
│   │   ├── security.py
│   │   └── settings.py
│   └── database/
│       ├── crud.py
│       ├── database.py
│       ├── models.py
│       └── schemas.py
├── database.db
├── main.py
└── requirements.txt
```

#### Key Files:
- **main.py**: Entry point for the FastAPI application.
- **app/api**: Contains the API endpoints for authentication, user management, and configuration settings.
- **app/core**: Holds core utilities such as dependencies (`deps.py`), JWT handling (`jwt.py`), and password validation (`password.py`).
- **app/database**: Contains database models, CRUD functions, and schema definitions.
- **requirements.txt**: Lists all dependencies for the backend.

### Frontend (Vue 3)

The frontend is a Vue 3 application built with Vite and Vuetify. It uses Pinia for state management and Axios for making HTTP requests to the backend.

**Directory Structure:**

```plaintext
frontend/
├── src/
│   ├── api/
│   ├── assets/
│   ├── components/
│   ├── functions/
│   ├── interfaces/
│   ├── layouts/
│   ├── pages/
│   ├── plugins/
│   ├── router/
│   ├── stores/
│   └── styles/
├── App.vue
├── main.ts
└── vite.config.ts
```

#### Key Directories:
- **components**: Contains reusable Vue components, such as `UpdateUserModal.vue` for editing users and `UsersList.vue` for displaying user lists.
- **stores**: Contains Pinia stores for managing application state, including the `useConfig` store for application configuration.
- **api**: Handles API calls with Axios.
- **interfaces**: Defines TypeScript interfaces for data models, ensuring type safety.

---

## Backend Details

### Dependencies

The backend dependencies are listed in `requirements.txt`. Key dependencies include:

- **FastAPI**: Web framework for building APIs with Python.
- **SQLModel**: ORM layer that combines SQLAlchemy and Pydantic for easy database interactions.
- **Pydantic**: Data validation and settings management.
- **PyJWT**: Used for JSON Web Token (JWT) authentication.
- **Uvicorn**: ASGI server to run the FastAPI application.
- **bcrypt and passlib**: For secure password hashing.

#### `requirements.txt` Content

```plaintext
annotated-types==0.7.0
anyio==4.6.2.post1
bcrypt==4.2.0
click==8.1.7
colorama==0.4.6
fastapi==0.115.4
greenlet==3.1.1
h11==0.14.0
idna==3.10
passlib==1.7.4
pydantic==2.9.2
pydantic-settings==2.6.1
pydantic_core==2.23.4
PyJWT==2.9.0
python-dotenv==1.0.1
sniffio==1.3.1
SQLAlchemy==2.0.36
sqlmodel==0.0.22
starlette==0.41.2
typing_extensions==4.12.2
uvicorn==0.32.0
```

### Configuration and Security

- **CORS**: CORS is configured with `"*"` to allow all origins for development. For production, it’s recommended to replace this with the actual frontend domain to enhance security.
- **Authentication**: JWT authentication is implemented for user sessions. Tokens are created and verified using PyJWT.

### API Endpoints

The backend has endpoints for authentication, user management, and configuration settings. Below is a summary of the key endpoints:

- **/auth/login**: Login endpoint to obtain a JWT token.
- **/auth/password**: Endpoint to change the user's password.
- **/users/me**: Fetches the details of the logged-in user.
- **/users/all**: Fetches a list of all users (admin-only).
- **/users/{user_id}**: Endpoint to update or delete a specific user by ID.
- **/config/**: Get and update application configuration settings.

For detailed information, refer to the OpenAPI JSON documentation generated by FastAPI.

### Running the Backend

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

---

## Frontend Details

### Dependencies

The frontend dependencies are managed in `package.json`. Key dependencies include:

- **Vue 3**: Progressive JavaScript framework.
- **Vuetify**: Material Design component library.
- **Pinia**: State management library.
- **Axios**: HTTP client for making API requests.
- **Vue Toastification**: Toast notification library for Vue 3.

#### `package.json` Dependencies

```json
{
  "@mdi/font": "7.4.47",
  "axios": "^1.7.7",
  "buffer": "^6.0.3",
  "core-js": "^3.37.1",
  "pinia-plugin-persistedstate": "^4.1.2",
  "roboto-fontface": "*",
  "vue": "^3.4.31",
  "vue-toastification": "^2.0.0-rc.5",
  "vuetify": "^3.6.11"
}
```

### State Management with Pinia

The frontend uses Pinia as its state management solution. Pinia's `useConfig` store manages configuration settings, including password validation requirements. These settings are fetched from the backend and stored persistently with `pinia-plugin-persistedstate`.

### User Interface

The frontend utilizes Vuetify to create a responsive, Material Design-inspired user interface. Key components include:
- **UsersList.vue**: Displays a list of users with options to edit, ban, or delete.
- **UpdateUserModal.vue**: Modal dialog for updating user information, such as username and password.
- **ConfigSettings.vue**: Allows configuration settings like password requirements to be managed by admins.

### Running the Frontend

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

### Key Features

1. **Password Validation**: Password validation rules can be dynamically configured via the backend's settings (e.g., minimum length, digit requirement).
2. **Toast Notifications**: Vue Toastification is used to show notifications for actions like saving, updating, and error messages.
3. **Vuetify Components**: The UI is built with Vuetify components, including `v-list`, `v-dialog`, and `v-text-field`, providing a consistent and modern look.

---

## Important Notes

- **Environment Configuration**: For production, ensure that the backend CORS configuration specifies the frontend domain.
- **Persistent Configuration**: The frontend configuration fetched from the backend is stored in Pinia with persistent state, making it resilient across page reloads.
- **OpenAPI Documentation**: FastAPI automatically generates OpenAPI documentation, accessible at `/docs` when the backend server is running. This documentation can be used to explore the available endpoints in detail.
