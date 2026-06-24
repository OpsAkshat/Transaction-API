# Transaction Api Backend
This is a Transaction API, built with **FastAPI** and powered by **PostgreSQL**.

## Prerequisites
- **Python 3.8+** installed on your system.
- **PostgreSQL** database running.
- 
## How to Run the Project
Follow these simple steps to run the backend on your local machine:
### 1. Open the backend folder
Open your terminal and navigate to the `backend` folder inside the project directory:
```bash
cd "Transaction app\backend"
```
### 2. Create a Virtual Environment (Optional but recommended)
A virtual environment keeps the project's dependencies separate from your global Python setup.
```bash
python -m venv venv
```
### 3. Activate the Virtual Environment
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```
### 4. Install the Required Packages
Install all the necessary libraries (like FastAPI, SQLAlchemy, Uvicorn, etc.) that the project needs to run.
```bash
pip install -r requirements.txt
```
### 5. Set up Environment Variables
Ensure you have a `.env` file in the `backend` folder. It should contain your database connection string, for example:
```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/transaction_db
```
*(Replace `your_password` and `transaction_db` with your actual database password and database name).*
### 6. Start the API Server
Run the FastAPI development server using Uvicorn.
```bash
uvicorn main:app --reload
```
### 7. View the API Documentation
Once the server is running, open your web browser and go to:
- **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** to see the interactive Swagger UI where you can test the API endpoints.


##  Frontend Setup

The frontend is a React application built using Vite.(Antigravity) 

### 1. Open the frontend folder
Open a new terminal window and navigate to the frontend directory from the root of the project:
```bash
cd frontend
```

### 2. Install Dependencies
Make sure you have Node.js installed, then install the required packages:
```bash
npm install
```

### 3. Run the Development Server
Start the frontend app:
```bash
npm run dev
```
- The React application will be accessible via the local URL provided in your terminal (typically [http://localhost:5173](http://localhost:5173)).
