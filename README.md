Medical Image Improvement Project Setup Guide
This guide provides step-by-step instructions to set up and run the Medical Image Improvement project on both Mac and Windows.
Prerequisites
Before starting, make sure you have the following installed:

Git
Python (3.8 or higher)
Node.js and npm
Visual Studio Code

Getting Started
1. Clone the Repository
bash# Create a folder for your project
mkdir MedicalProject
cd MedicalProject

# Clone the repository
git clone https://github.com/TanmayJDesai/MedicalImageImprovement.git
cd MedicalImageImprovement
2. Installing Dependencies
Backend Dependencies (Python/Flask)
For Mac:
bash# Navigate to backend folder
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
For Windows:
bash# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
Frontend Dependencies (React)
For both Mac and Windows:
bash# Navigate to frontend folder from project root
cd frontend

# Install Node.js dependencies
npm install
3. Running the Application
Start the Backend Server
Keep your virtual environment activated and run:
For Mac:
bash# Make sure you're in the backend folder with venv activated
python3 app.py
For Windows:
bash# Make sure you're in the backend folder with venv activated
python app.py
The backend server will start running on http://localhost:5000
Start the Frontend Server
Open a new terminal window while keeping the backend running.
bash# Navigate to frontend folder
cd frontend

# Start React development server
npm start
This will automatically open your browser to http://localhost:3000
Using the Application in VS Code

Open VS Code
Go to File > Open Folder
Select the MedicalImageImprovement folder

To run the application:

Open a terminal in VS Code (Terminal > New Terminal)
Follow the "Installing Dependencies" and "Running the Application" steps above

Troubleshooting
Backend Issues
If port 5000 is already in use:

Mac: Run lsof -i :5000 to find the process, then kill -9 [PID]
Windows: Run netstat -ano | findstr :5000, then taskkill /PID [PID] /F

Frontend Issues
If npm install fails:
bashrm -rf node_modules
npm cache clean --force
npm install
Important Notes

Both backend and frontend must run simultaneously
Backend runs on port 5000, frontend on port 3000
Make sure your virtual environment is activated when running the backend
