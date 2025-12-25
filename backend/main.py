
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware

# from services.email_service import generate_email
# from database.db import get_connection   # ✅ ADD THIS

# app = FastAPI(title="AI Email Personalization")

# # ✅ CORS CONFIGURATION (Already correct)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # React frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------------
# # Health check
# # ---------------------------
# @app.get("/")
# def home():
#     return {"message": "AI Email Personalization API is running"}

# # ---------------------------
# # Generate Email (Already working)
# # ---------------------------
# @app.get("/generate-email/{customer_id}/{campaign_id}")
# def get_email(customer_id: int, campaign_id: int):
#     """
#     Generate a personalized email for a given customer and campaign.
#     """
#     try:
#         result = generate_email(customer_id, campaign_id)
#         if "error" in result:
#             raise HTTPException(status_code=404, detail=result["error"])
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ---------------------------
# # ✅ NEW: Get Customers (for dropdown)
# # ---------------------------
# @app.get("/customers")
# def get_customers():
#     try:
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT id, name FROM customers")
#         customers = cursor.fetchall()
#         conn.close()
#         return customers
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ---------------------------
# # ✅ NEW: Get Campaigns (for dropdown)
# # ---------------------------
# @app.get("/campaigns")
# def get_campaigns():
#     try:
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT id, name FROM campaigns")
#         campaigns = cursor.fetchall()
#         conn.close()
#         return campaigns
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/track/{email_log_id}/{action}")
# def track_action(email_log_id: int, action: str):
#     conn = get_connection()
#     cursor = conn.cursor()

#     if action == "open":
#         cursor.execute(
#             "UPDATE email_logs SET opened=TRUE WHERE id=%s",
#             (email_log_id,)
#         )
#     elif action == "click":
#         cursor.execute(
#             "UPDATE email_logs SET clicked=TRUE WHERE id=%s",
#             (email_log_id,)
#         )

#     conn.commit()
#     conn.close()
#     return {"status": "tracked"}


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from services.email_service import generate_email
from database.db import get_connection

app = FastAPI(title="AI Email Personalization")

# ---------------------------
# CORS CONFIGURATION (PROD SAFE)
# ---------------------------
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Health check
# ---------------------------
@app.get("/")
def home():
    return {"message": "AI Email Personalization API is running"}

# ---------------------------
# Generate Email
# ---------------------------
@app.get("/generate-email/{customer_id}/{campaign_id}")
def get_email(customer_id: int, campaign_id: int):
    try:
        result = generate_email(customer_id, campaign_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Get Customers
# ---------------------------
@app.get("/customers")
def get_customers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM customers")
        customers = cursor.fetchall()
        conn.close()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Get Campaigns
# ---------------------------
@app.get("/campaigns")
def get_campaigns():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM campaigns")
        campaigns = cursor.fetchall()
        conn.close()
        return campaigns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Track Email Actions
# ---------------------------
@app.post("/track/{email_log_id}/{action}")
def track_action(email_log_id: int, action: str):
    conn = get_connection()
    cursor = conn.cursor()

    if action == "open":
        cursor.execute(
            "UPDATE email_logs SET opened=TRUE WHERE id=%s",
            (email_log_id,)
        )
    elif action == "click":
        cursor.execute(
            "UPDATE email_logs SET clicked=TRUE WHERE id=%s",
            (email_log_id,)
        )

    conn.commit()
    conn.close()
    return {"status": "tracked"}

# ---------------------------
# Render / Production entry
# ---------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )


