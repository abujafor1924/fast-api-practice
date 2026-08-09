mkdir fastapi-project
cd fastapi-project
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn



fastapi-project/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes/
│   │       └── users.py
│   │
│   ├── schemas/
│   │   └── user.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   ├── repositories/
│   │   └── user_repository.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   └── db/
│       ├── session.py
│       └── base.py
│
├── tests/
├── .env
├── requirements.txt
└── README.md