# CS50P Todo API
#### Video Demo:  <URL HERE>
#### Description:

## Overview

This project is a RESTful Todo API built with FastAPI, a modern Python web framework. The API provides full CRUD (Create, Read, Update, Delete) functionality for managing a todo list, with data persistence through JSON file storage. The application demonstrates core concepts of web API development, including HTTP methods, request/response handling, data validation with Pydantic, and comprehensive testing with pytest.

## Project Files

### project.py

This is the main application file containing all the business logic and API endpoints. It includes:

**Core Functions:**
- `load_data()` - Reads todos from the JSON file, returning an empty list if the file doesn't exist or contains invalid JSON
- `save_data(data)` - Writes the todo list to the JSON file with pretty-printed formatting
- `add_task(current_todos, task_name)` - Adds a new task to the list with auto-incrementing ID, validates that task name is not empty
- `updated_status(current_todos, todo_id)` - Toggles the completed status of a task by ID, returns None if task not found
- `remove_task(current_todos, todo_id)` - Removes a task from the list by ID, returns boolean indicating success
- `main()` - Launches the uvicorn ASGI server on localhost:8000

**API Endpoints:**
- `GET /todos` - Lists all todos
- `POST /todos` - Creates a new todo (accepts JSON body with "task" field)
- `GET /todos/{todo_id}` - Retrieves a single todo by ID
- `PUT /todos/{todo_id}` - Toggles the completed status of a todo
- `DELETE /todos/{todo_id}` - Removes a todo from the list

**Pydantic Models:**
- `Todo` - Defines the structure of a todo item (id, task, completed)
- `TodoCreate` - Request model for creating new todos (task only)

### test_project.py

Contains comprehensive unit and integration tests for the project:

**Unit Tests:**
- `test_add_task()` - Verifies task creation, ID assignment, and empty task validation
- `test_updated_status()` - Tests status toggling and handling of non-existent IDs
- `test_remove_task()` - Validates task deletion and edge cases

**Integration Test:**
- `test_get_todo_api()` - End-to-end test using FastAPI's TestClient to verify the GET endpoint works correctly, including creating a todo, fetching it by ID, and testing 404 responses for missing items. Uses `tmp_path` and `monkeypatch` fixtures to isolate the test database file.

### requirements.txt

Lists all Python dependencies needed to run the project:
- fastapi - Modern web framework for building APIs
- uvicorn - ASGI server for running FastAPI applications
- pydantic - Data validation using Python type annotations
- pytest - Testing framework
- httpx - Required for FastAPI's TestClient

### todos.json

Automatically created JSON file that persists todo data between server restarts. Each todo contains an id, task description, and completed status.

## Design Choices

**1. FastAPI over Flask**
I chose FastAPI for this project because of its automatic API documentation (via Swagger UI at `/docs`), built-in data validation with Pydantic models, and modern async support. The automatic OpenAPI schema generation makes the API immediately usable and testable through a web interface.

**2. JSON File Storage vs Database**
For this project, I opted for simple JSON file storage rather than a full database system. This decision was made to keep the project focused on API design and testing fundamentals without the complexity of database setup. JSON storage is adequate for a learning project and makes the code more portable. The trade-off is that this approach wouldn't scale well for concurrent users or large datasets, but for a demonstration project, it provides sufficient persistence with minimal dependencies.

**3. Function Separation**
I deliberately kept the business logic functions (`add_task`, `updated_status`, `remove_task`) separate from the FastAPI route handlers. This separation of concerns makes the code more testable (as evidenced by the unit tests that don't require spinning up the API server) and follows the principle of keeping business logic independent from the web framework.

**4. Auto-incrementing IDs**
Rather than using UUIDs or database-generated IDs, I implemented a simple max-based ID generation system. While this approach has limitations (IDs could theoretically collide if todos are deleted and the JSON file is manually edited), it provides predictable, user-friendly integer IDs suitable for a learning project.

**5. PUT for Toggle vs PATCH for Update**
I used PUT for the toggle endpoint rather than implementing a full PATCH endpoint for partial updates. This simplifies the API while still demonstrating HTTP method semantics. In a production API, I might add a PATCH endpoint to allow updating the task text itself, but for this project, the toggle functionality demonstrates state modification adequately.

**6. Test Isolation**
In the integration test, I used pytest's `tmp_path` fixture and `monkeypatch` to isolate the test database file from the production `todos.json`. This ensures tests don't interfere with actual data and can run in any environment without side effects.

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start the server:
   ```
   python project.py
   ```

3. Access the API:
   - Interactive docs: http://127.0.0.1:8000/docs
   - API endpoint: http://127.0.0.1:8000/todos

4. Run tests:
   ```
   pytest test_project.py
   ```

## Example Usage

Create a todo:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"task":"Buy groceries"}' http://127.0.0.1:8000/todos
```

List all todos:
```bash
curl http://127.0.0.1:8000/todos
```

Toggle completion status:
```bash
curl -X PUT http://127.0.0.1:8000/todos/1
```

Delete a todo:
```bash
curl -X DELETE http://127.0.0.1:8000/todos/1
```

## Future Enhancements

Potential improvements for future versions:
- Add user authentication and multi-user support
- Implement task categories/tags
- Add due dates and priority levels
- Migrate to a proper database (PostgreSQL or SQLite)
- Add task search and filtering capabilities
- Implement PATCH endpoint for updating task text
- Add task sorting options

This project demonstrates proficiency in Python web development, API design, data validation, error handling, and comprehensive testing practices.
