# Gender Classification API

A backend API built with **Django** and **Django REST Framework** that classifies a given name by gender using the **Genderize.io API**, processes the response, and returns a structured JSON output.


## 🚀 Live API

Base URL:
https://gender-service-git-main-ebenezeramakato96-8725s-projects.vercel.app

📌 Endpoint
Classify Name
GET /api/classify?name={name}
```
Example

```
GET /api/classify?name=alex
```

Full URL:

```
https://gender-service-git-main-ebenezeramakato96-8725s-projects.vercel.app/api/classify?name=alex
``` ✅ Success Response (200 OK)


```json
{
  "status": "success",
  "data": {
    "name": "alex",
    "gender": "male",
    "probability": 0.95,
    "sample_size": 1665200,
    "is_confident": true,
    "processed_at": "2026-04-13T15:28:32Z"
  }
}
```

❌ Error Response (400 Bad Request)

```json
{
  "status": "error",
  "message": "Name query parameter is required"
}
```

⚙️ Processing Logic

The API processes the raw response from Genderize.io as follows:

* `sample_size` = `count` from the API response
* `is_confident` is `true` **only if BOTH conditions are met**:

  * `probability >= 0.7`
  * `sample_size >= 100`
* Otherwise → `false`
* `processed_at` is dynamically generated on each request (UTC, ISO 8601 format)

🛠️ Tech Stack

* Python
* Django
* Django REST Framework
* Requests (for external API calls)
* Vercel (deployment)

📦 Project Structure

```
gender_service/
├── api/
│   ├── views.py
│   ├── urls.py
│   ├── index.py
│   └── ...
├── gender_service/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── manage.py
├── requirements.txt
├── vercel.json
└── runtime.txt
```


⚙️ Setup (Local Development)

1. Clone the repository

```
git clone https://github.com/Ebenezer96/gender_service.git
cd gender_service
```

---

 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---
3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Run server

```
python manage.py runserver
```

---
 🌐 Deployment (Vercel)

This project is deployed on **Vercel using Python serverless functions**.

Key configuration:

* `api/index.py` → Entry point for Django (WSGI)
* `vercel.json` → Routes all requests to Django backend
* `requirements.txt` → Must be UTF-8 encoded

---
⚠️ Important Notes

* API returns **JSON only** (Browsable API disabled)
* Ensure `requirements.txt` is saved as **UTF-8**
* Django 5.x used for compatibility
* Root endpoint `/` serves as a health check

---

 🧪 Testing

Using curl:

```
curl "https://gender-service-git-main-ebenezeramakato96-8725s-projects.vercel.app/api/classify?name=alex"
```

---

 👤 Author

Ebenezer Amakato
GitHub: https://github.com/Ebenezer96

---
 📄 License

This project is for educational and assessment purposes.
