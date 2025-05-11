from app.main import app  # Import the FastAPI app
import app.db.database  # Import the database module to ensure tables are created

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the FastAPI app 