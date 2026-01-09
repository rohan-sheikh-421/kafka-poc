## Kafka Microservices Proof of Concept (Kafka-POC)

### 📌 Overview

This project is a **fully dockerized, event-driven microservices system** built using:

-   **Apache Kafka** (event streaming)
    
-   **FastAPI (Python)** for microservices
    
-   **PostgreSQL** as the database
    
-   **SQLAlchemy** as ORM
    
-   **Kafka UI (Provectus)** for monitoring
    
-   **Docker & Docker Compose** for orchestration
    

The goal is to demonstrate **end-to-end event flow**, fault tolerance, replayability, and service scalability.

----------

## 🧱 Architecture

```
Client (Postman / curl)
        |
        v
Order Service (FastAPI)
        |
        v
Postgres (orders table)
        |
        v
Kafka Topic: order-events
        |
        v
Inventory Service (Consumer + Producer)
        |
        v
Postgres (inventory table)
        |
        v
Kafka Topic: inventory-events
        |
        v
Notification Service (Consumer)
        |
        v
Postgres (notifications table)

```

----------

## 🗂 Project Structure

```
kafka-poc/
│── docker-compose.yml
│── README.md
│── .gitignore
│
├── services/
│   ├── order-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   └── kafka_client.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── inventory-service/
│   │   ├── app/
│   │   │   ├── worker.py
│   │   │   ├── db.py
│   │   │   └── models.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── notification-service/
│       ├── app/
│       │   ├── worker.py
│       │   ├── db.py
│       │   └── models.py
│       ├── Dockerfile
│       └── requirements.txt
│
└── database/
    └── postgres/

```

----------

## 🐳 Services

### Infrastructure

-   **Zookeeper** – Kafka coordination
    
-   **Kafka Broker**
    
-   **Kafka UI** – [http://localhost:8080](http://localhost:8080/)
    
-   **Postgres** – port 5432
    

### Application Services

-   **Order Service** – REST API
    
-   **Inventory Service** – Kafka consumer/producer
    
-   **Notification Service** – Kafka consumer
    

----------

## 🚀 Getting Started

### 1️⃣ Prerequisites

-   Docker Desktop
    
-   Git
    
-   VS Code
    
-   PowerShell / Terminal
    

----------

### 2️⃣ Start Infrastructure & Services

```bash
docker compose up -d --build

```

----------

### 3️⃣ Create Kafka Topics (REQUIRED)

Kafka does **not auto-create topics reliably**, so create them manually.

```bash
docker compose exec kafka kafka-topics \
  --bootstrap-server kafka:29092 \
  --create \
  --topic order-events \
  --partitions 3 \
  --replication-factor 1

```

```bash
docker compose exec kafka kafka-topics \
  --bootstrap-server kafka:29092 \
  --create \
  --topic inventory-events \
  --partitions 3 \
  --replication-factor 1

```

Restart consumers after topic creation:

```bash
docker compose restart inventory-service notification-service

```

----------

## 🧪 Testing the System

### Create an Order

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri http://localhost:8000/orders `
  -ContentType "application/json" `
  -Body '{"item":"Laptop","quantity":1}'

```

----------

### Verify Kafka Messages

-   Open **Kafka UI** → [http://localhost:8080](http://localhost:8080/)
    
-   Check:
    
    -   `order-events`
        
    -   `inventory-events`
        

----------

### Verify Database

```bash
docker compose exec postgres psql -U app -d appdb

```

```sql
SELECT * FROM orders;
SELECT * FROM inventory;
SELECT * FROM notifications;

```

----------

## 📈 Scaling Test

Run multiple notification consumers:

```bash
docker compose up -d --scale notification-service=3

```

Kafka will automatically distribute partitions across consumers.

----------

## ♻ Replay Test

1.  Stop notification service:
    

```bash
docker compose stop notification-service

```

2.  Produce new orders
    
3.  Start service:
    

```bash
docker compose start notification-service

```

Messages replay successfully.

----------

## 🛠 Fault Tolerance Tests

-   Stop Postgres → services retry & recover
    
-   Stop consumers → Kafka retains messages
    
-   Restart services → consumers resume from offsets
    

----------

## 🧠 Key Concepts Demonstrated

-   Event-driven architecture
    
-   Kafka producers & consumers
    
-   Consumer groups & partitions
    
-   Message replay
    
-   Fault tolerance
    
-   Dockerized microservices
    
-   Kafka monitoring
    

----------

## ✅ Deliverables Achieved

✔ Kafka cluster running  
✔ Kafka UI monitoring  
✔ REST API producing events  
✔ Consumers processing events  
✔ DB persistence  
✔ Scaling verified  
✔ Replay verified

----------

## 📌 Notes

-   Kafka topics **must be created manually**
    
-   `__consumer_offsets` is an internal Kafka topic
    
-   `depends_on` does not guarantee readiness — services must retry
    

----------

## 🏁 Conclusion

This project demonstrates a **production-style Kafka microservices pipeline** with real-world behavior, issues, and solutions.

----------
