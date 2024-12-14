# FastAPI Project

This is a FastAPI project for managing users.

## Requirements

- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Python-dateutil
- Freezegun

## Setup

1. Clone the repository:

   ```sh
   git clone <repository_url>
   cd fast_api_test
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server:

   ```sh
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to `http://127.0.0.1:8000` to see the API documentation.

## Project Structure

- [controllers](http://_vscodecontentref_/1): Contains the API endpoint definitions.
- [domain](http://_vscodecontentref_/2): Contains the domain logic.
- [dto](http://_vscodecontentref_/3): Contains the data transfer objects.
- [lib](http://_vscodecontentref_/4): Contains utility functions and decorators.
- [main.py](http://_vscodecontentref_/5): The entry point of the application.

## Endpoints

- `GET /user/`: Browse users.
- `GET /user/{id}`: Read a user by ID.
- `PUT /user/{id}`: Edit a user by ID.
- `POST /user/`: Add a new user.
- `DELETE /user/{id}`: Delete a user by ID.

## License

This project is licensed under the MIT License.
