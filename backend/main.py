from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("company.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database and tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
     # Create companies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Pydantic Models
class Company(BaseModel):
    name: str
    location: str

# Routes
@app.get("/")
async def read_main():
    return {"msg": "Welcome to the Companies API"}

@app.post("/companies/")
async def add_company(company: Company):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (name, location) VALUES (?, ?)", (company.name, company.location))
    conn.commit()
    company_id = cursor.lastrowid
    conn.close()
    return {"id": company_id, "name": company.name, "location": company.location}

@app.get("/companies/")
async def get_companies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    conn.close()

    company_list = [{"id": company[0], "name": company[1], "location": company[2]} for company in companies]

    return {"companies": company_list}

@app.put("/companies/{company_id}")
async def update_company(company_id: int, company: Company):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM companies WHERE id = ?", (company_id,))
    existing_company = cursor.fetchone()

    if not existing_company:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    cursor.execute("UPDATE companies SET name = ?, location = ? WHERE id = ?", (company.name, company.location, company_id))
    conn.commit()
    conn.close()

    return {"id": company_id, "name": company.name, "location": company.location}

@app.delete("/companies/{company_id}")
async def delete_company(company_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM companies WHERE id = ?", (company_id,))
    company = cursor.fetchone()
    if not company:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    cursor.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.commit()
    conn.close()
    return {"detail": "Company deleted successfully"}
