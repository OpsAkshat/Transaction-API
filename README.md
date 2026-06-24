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

---

## ⚙️ How It Works

### How each API works

- `POST /api/user`: Registers a new user. It checks if the requested name already exists. If not, it creates a new user with a unique ID and initializes their points and transaction count to 0.
- `POST /api/transaction`: Submits a new transaction for an existing user. The API accepts the `user_id` and the `points` to add (maximum 10,000 points per transaction). It updates the user's total points, increments their transaction count, and records the timestamp of the latest transaction.
- `GET /api/summary/{user_id}`: Retrieves a specific user's summary. This includes their total points, total transaction count, the time of their last transaction, and a descending chronological history of all their individual transactions.
- `GET /api/ranking`: Returns a list of all users, sorted by their dynamically calculated `ranking_score` in descending order.

### How ranking is calculated

The leaderboard ranking is determined by a dynamically calculated **Ranking Score** (out of ~100 points maximum), which comprises three weighted factors:

1. **Total Points (60% weight):** Calculated proportionally against the user with the highest total points globally. 
   *(Formula: `(user.total_points / max_points_among_all_users) * 60`)*
2. **Consistency (25% weight):** Calculated proportionally against the user with the highest transaction count globally. 
   *(Formula: `(user.transaction_count / max_transactions_among_all_users) * 25`)*
3. **Recency (15% weight):** Users receive up to 15 points for recent activity. They lose 1 point for every day of inactivity since their last transaction (down to a minimum of 0 points). 
   *(Formula: `max(0, 15 - days_since_last_transaction)`)*

The final `ranking_score` is the sum of these three factors, rounded to two decimal places. Users are sorted based on this score, with the highest score taking Rank 1.

### How duplicate requests are prevented

Duplicate requests and race conditions are prevented using two main mechanisms:

1. **In-Memory Asynchronous Locks:** When a transaction is submitted (`POST /api/transaction`), the backend acquires an `asyncio.Lock` specifically tied to that `user_id`. This prevents concurrent requests for the same user from executing simultaneously, ensuring that calculations (like adding to total points) do not suffer from race conditions or data overwrites.
2. **Database Integrity and Constraints:** The database utilizes a `UniqueConstraint` on the `idempotency_key` in the transactions table. The backend transaction logic is wrapped in a `try/except IntegrityError` block. If a duplicate transaction insertion is attempted that violates unique constraints, the database safely rolls back the operation, and the API returns a `409 Conflict` (Duplicate transaction) response.
