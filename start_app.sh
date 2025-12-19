#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo "Stopping services..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

echo "🚀 Starting Digital Evidence Locker..."

# Start Backend
echo "🔐 Launching Backend (FastAPI)..."
source venv/bin/activate
cd backend
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready (optional check)
sleep 2

# Start Frontend
echo "💻 Launching Frontend (React)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ System Running!"
echo "   - Backend: http://127.0.0.1:8000"
echo "   - Frontend: http://localhost:5173"
echo "   - API Docs: http://127.0.0.1:8000/docs"
echo "Press Ctrl+C to stop both servers."

wait
