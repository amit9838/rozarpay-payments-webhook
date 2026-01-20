# Minimal Webhook System for Payment Status Updates

This project is a robust, secure, and idempotent webhook listener designed to accept, validate, and store payment status updates from providers like Razorpay or PayPal. It is built using **FastAPI** and **SQLAlchemy**.

## 🚀 Features

* **Secure Webhook Receiver**: Validates the authenticity of incoming requests using HMAC-SHA256 signature verification .
* **Idempotency**: Prevents duplicate processing of the same event ID, ensuring data integrity even if the provider retries the webhook.
* **Data Persistence**: Stores raw payloads and extracted metadata in a relational database (SQLite/PostgreSQL compatible).
* **Query API**: Provides an endpoint to retrieve the historical event log for any specific payment ID, sorted chronologically.
* **Error Handling**: Gracefully handles invalid JSON, missing signatures, and malformed payloads.

---

## 🛠️ Tech Stack

* **Framework**: FastAPI (Python 3.9+)
* **Database**: SQLite (Default) / PostgreSQL (Production ready)
* **ORM**: SQLAlchemy
* **Validation**: Pydantic

---

## 📊 System Architecture
<img src=""/>


## ⚙️ Setup & Installation

### 1. Clone the Repository

git clone [https://github.com/amit9838/webhook-system.git](https://github.com/amit9838/webhook-system.git)
```bash
cd webhook-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic requests

```

### 4. Run the Server

The application will start on `localhost:8000`.

```bash
uvicorn main:app --reload

```

---

## 🧪 Testing & Usage

You can test the system using `curl` or the provided Python test script.

### Configuration

* **Shared Secret**: `test_secret` 


* **Header Key**: `X-Razorpay-Signature` 

### Method 1: Using the Test Runner

Since generating HMAC signatures manually is difficult in the terminal, use the included script to simulate valid requests.

```bash
python test_runner.py

```



### Method 3: View History

To see stored events for a specific payment:

```bash
curl http://localhost:8000/payments/pay_014/events

```

---
