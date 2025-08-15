from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app for serving frontend
frontend_app = FastAPI(title="House Price Predictor Frontend")

# Add CORS middleware
frontend_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory of this file
frontend_dir = os.path.dirname(os.path.abspath(__file__))

# Mount static files
frontend_app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "static")), name="static")

@frontend_app.get("/")
async def serve_index():
    """Serve the main index.html file"""
    return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    print("Starting frontend server...")
    print("Frontend will be available at: http://localhost:3000")
    print("Make sure the API server is running at: http://localhost:8000")
    uvicorn.run(frontend_app, host="0.0.0.0", port=3000)
