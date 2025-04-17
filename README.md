Medical Image Improvement — Setup Guide
This guide walks you through setting up and running the Medical Image Improvement project from scratch. It's written to be beginner-friendly — no prior experience with Git or VS Code is assumed.
Prerequisites
Before you begin, make sure you have the following installed:

Git
Python 3.8 or higher
Node.js and npm
Visual Studio Code

Download Links

Git: https://git-scm.com/downloads
Python: https://www.python.org/downloads/
Node.js: https://nodejs.org/
VS Code: https://code.visualstudio.com/

Overview of Steps
You will:

Create a GitHub repository and connect it to your computer
Clone the project files
Install required dependencies
Run the backend (Python)
Run the frontend (React)

1. Set Up Git and GitHub
a. Create a GitHub Repository

Go to github.com and sign in (or create an account).
Click the "+" in the top-right and choose "New repository".
Name the repository MedicalImageImprovement.
Do not initialize with a README, .gitignore, or license.
Click "Create repository".

b. Set Up Your Project Folder Locally
Open your terminal (Mac) or Command Prompt (Windows):
bashmkdir MedicalProject
cd MedicalProject
# Initialize a Git repository
git init
# Add your GitHub repo as the remote (replace URL with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/MedicalImageImprovement.git
2. Clone the Repository
Download the project files to your local machine:
bashgit clone https://github.com/TanmayJDesai/MedicalImageImprovement.git
cd MedicalImageImprovement
3. Install Project Dependencies
A. Backend (Python/Flask)
Mac
bashcd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Windows
bashcd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
B. Frontend (React)
Works the same on Mac and Windows:
bashcd ../frontend
npm install
4. Running the Application
A. Start the Backend Server
Mac
bashcd backend
source venv/bin/activate
python3 app.py
Windows
bashcd backend
venv\Scripts\activate
python app.py
The backend will run at http://localhost:5000.
B. Start the Frontend Server
Open a new terminal window:
bashcd frontend
npm start
This will open the frontend at http://localhost:3000.
5. Opening the Project in VS Code

Open Visual Studio Code
Click "File" > "Open Folder"
Select the MedicalImageImprovement folder
Open a terminal in VS Code: "Terminal" > "New Terminal"
Follow the instructions above to install dependencies and run the backend and frontend

Troubleshooting
Port 5000 Already in Use (Backend)
Mac
bashlsof -i :5000
kill -9 [PID]
Windows
bashnetstat -ano | findstr :5000
taskkill /PID [PID] /F
npm Install Fails (Frontend)
bashrm -rf node_modules
npm cache clean --force
npm install
Notes

The backend runs on port 5000, and the frontend runs on port 3000.
Both must be running simultaneously for the application to function.
RetryClaude does not have the ability to run the code it generates yet.Claude can make mistakes. Please double-check responses.
