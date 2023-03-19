# GoCRM - Travel SMBs CRM ©
![Build Django](https://github.com/astratechz/travelco_crm/actions/workflows/django.yml/badge.svg)

[Product Demo](https://www.loom.com/share/ae66221bf1e740718f39bb625b256d87)

- Create `env`: `python3 -m venv env`

- Clone project `git clone https://github.com/engagepy/go-CRM-andaman.git` 

- In root folder within an activated `(env)` create a file `.env` like this in your terminal

- Step 1 (Type):       `cat > .env` 
- Step 2 (Paste):       `APP_PASSWORD = <your-random-development-insecure-password>`
- Step 3 (Return):       `ctrl+c`

- Now Install Dependencies for the project

        pip install -r requirements.txt

- Navigate to manage.py in terminal. Once in correct directory:

        python manage.py makemigrations
        python manage.py migrate --run-syncdb 
        python manage.py createsuper 
        python manage.py runserver 
        Do try 127.0.0.1:8000/admin
        
[Gmail App Password Support](https://support.google.com/mail/answer/185833?hl=en-GB) 


## Pilot Market = Andaman Islands

## Pilot Test Date = 1 April, 2023

## Phases -> Features: 

### Phase I

```
- Store Hotels and Rates: 
- Store Activities and Excursions
- Store Customers 
- Create Trips
- Create Login 
- Manage Staff Leads and Sales
- Output .pdf itineraries with images
- Deploy for Go Team
```

### Phase II

```
- Basic `Dashboard` with Graphs and Stats
- Ensure Login creates Unique App Instance
- Create Robust Calculation Functions for Staff
- Create Reports & Advanced `Dashboard`
- Send Automated Emails & Reminders
- Integrate Whatsapp
```

### Phase III: 

```
- Create CI/CD Pipeline
- Add PWA Features
- Market with Subscription Feature
```

# Core Functionalities
                                                                                                                
<img width="837" alt="Screenshot 2023-01-10 at 03 08 50" src="https://user-images.githubusercontent.com/42845567/211651077-6c47bb6d-ee0a-4840-b11f-38435be120d5.png">

# Road Map:

<img width="1103" alt="Screenshot 2023-01-10 at 03 05 54" src="https://user-images.githubusercontent.com/42845567/211652883-8078aca4-fe9d-44a8-b3e1-c79ce4c0f7a1.png">





