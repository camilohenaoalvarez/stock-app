# FastAPI Stock Management

This project is a FastAPI application for managing users and products in a stock system

# Prerequisites

- Docker
- Docker Compose

# Running the app

1. Clone the repository:
    `git clone ...`

2. Running the app
```bash
    docker-compose up --build
```

### Get the DB volume
```bash
    docker volume ls
```

### Stop running the app
```bash
    docker-compose down
```

# API Docs

Available API endpoints for managing users and products

## Base URL

All endpoints are relative to the base URL: `http://localhost:8000`

## User Endpoints

#### Get Users

- **Endpoint**: `/users/`
- **Method**: `GET`
- **Description**: Retrieve a list of all users
- **Response**: Returns a JSON array of user objects

#### Get User by ID

- **Endpoint**: `/users/{user_id}`
- **Method**: `GET`
- **Description**: Retrieve details of a specific user by ID
- **Response**: Returns a JSON object with the user details

#### Create a New User

- **Endpoint**: `/users/`
- **Method**: `POST`
- **Description**: Create a new user
- **Request Body** (JSON):
```json
    {
        "name": "User Name"
    }
```
- **Response**: Returns a JSON object with the created user details

#### Update a User

- **Endpoint**: /users/{user_id}
- **Method**: PUT
- **Description**: Update the name of an existing user
- **Request Body** (JSON):
```json
    {
        "new_name": "New User Name"
    }
```
- **Response**: Returns a JSON object with the updated user details

#### Delete a User

- **Endpoint**: `/users/{user_id}`
- **Method**: `DELETE`
- **Description**: Delete a user by ID
- **Response**: Returns `204 No Content` on successful deletion

## Product Endpoints

#### Get All Products

- **Endpoint**: `/products/`
- **Method**: `GET`
- **Description**: Retrieve a list of all products
- **Response**: Returns a JSON array of product objects

#### Get Product by ID

- **Endpoint**: `/products/{product_id}`
- **Method**: `GET`
- **Description**: Retrieve details of a specific product by ID
- **Response**: Returns a JSON object with the product details

#### Create a New Product

- **Endpoint**: `/products/`
- **Method**: `POST`
- **Description**: Create a new product
- **Request Body** (JSON):
```json
    {
        "name": "Product Name",
        "user_id": 1
    }
```
- **Response**: Returns a JSON object with the created product details

#### Update a Product

- **Endpoint**: `/products/{product_id}`
- **Method**: `PUT`
- **Description**: Update the name and user ID of an existing product
- **Request Body** (JSON):
```json
    {
        "new_name": "New Product Name",
        "new_user_id": 1
    }
```
- **Response**: Returns a JSON object with the updated product details

#### Delete a Product

- **Endpoint**: `/products/{product_id}`
- **Method**: `DELETE`
- **Description**: Delete a product by ID
- **Response**: Returns `204 No Content` on successful deletion

## Additional Information

- Access the interactive API documentation at `http://localhost:8000/docs` for more details and testing

## Author

- Camilo Henao Alvarez