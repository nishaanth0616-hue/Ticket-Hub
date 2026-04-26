# 🎫 Ticket Hub - Unified Booking System

Welcome to **Ticket Hub**, a comprehensive, state-of-the-art booking platform designed to streamline your travel and entertainment needs. Built with a focus on speed, reliability, and a premium user experience, Ticket Hub integrates various booking services into a single, cohesive ecosystem.

![Ticket Hub Banner](https://img.shields.io/badge/Ticket--Hub-Premium--Booking-blueviolet?style=for-the-badge&logo=appveyor)

---

## 🚀 Features

Ticket Hub offers a wide array of booking services, all managed through a secure user account system:

- **🎬 Movies**: Explore the latest blockbusters and reserve your seats with an interactive seating chart.
- **🚌 Buses**: Real-time bus search between cities with detailed route information.
- **🚆 Trains**: Efficient rail booking with source-to-destination filtering.
- **✈️ Flights**: Quick and easy air travel booking for domestic and international routes.
- **🏨 Hotels**: Find and book premium accommodations with ease.
- **🚕 Cabs**: Seamless inter-city cab booking services.
- **🎟️ Events**: Stay updated with local events and book your tickets instantly.
- **🛒 Unified Cart**: Add multiple bookings from different categories into a single cart.
- **💳 Secure Checkout**: Simulated secure payment gateway for a realistic booking experience.
- **📜 Booking History**: Keep track of all your past and upcoming bookings in one place.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask (Web Framework)
- **Database**: SQLite3 (Session & User Management)
- **Data Handling**: Pandas (CSV-based route and inventory management)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design), JavaScript
- **Deployment**: Gunicorn, Procfile-ready for Heroku/Render

---

## 📦 Installation & Setup

Follow these steps to get the project running locally:

### 1. Clone the Repository
```bash
git clone https://github.com/nishaanth0616-hue/Ticket-Hub.git
cd ticket-hub
```

### 2. Set up a Virtual Environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`.

---

## 📂 Project Structure

```text
ticket-booker/
├── app.py              # Main Flask application logic
├── models.py           # Database models and schemas
├── requirements.txt    # Project dependencies
├── Procfile            # Deployment configuration
├── data/               # CSV/JSON datasets (Buses, Trains, etc.)
├── static/
│   ├── css/            # Custom stylesheets
│   └── js/             # Frontend logic & animations
├── templates/          # HTML views (Jinja2 templates)
└── users.db            # SQLite database (Auto-generated)
```

---

## 🛡️ Security Features

- **Password Hashing**: Secure password storage using `werkzeug.security`.
- **Session Protection**: Encrypted session management for user authentication.
- **Cache Management**: Strict cache-control headers to prevent unauthorized access to sensitive pages.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Built with ❤️ by the Ticket Hub Team
</p>
