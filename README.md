# RYZFund Stokvel Platform

RYZFund is a comprehensive stokvel management platform for South African savings groups. It enables members to collaborate, manage contributions, track payouts, schedule meetings, and communicate efficiently.

## Features

- **Stokvel Management:** Create, join, and manage stokvels with full visibility over contributions and payouts.
- **Member Dashboard:** View group balance, personal contributions, active members, payouts, and progress.
- **Meetings & Agendas:** Schedule meetings, create agendas, record minutes, and notify members.
- **KYC Onboarding:** Secure onboarding with identity document, proof of address, and selfie verification.
- **Notifications:** Automated alerts for meetings, payouts, and coordinator messages.
- **AI Analytics:** Chatbot for financial queries and insights.
- **Coordinator Messaging:** Direct communication between coordinators and members.

## Tech Stack

- **Backend:** Django 5.2 ([ryzen/](ryzen/))
- **Frontend:** HTML, CSS ([css/styles.css](css/styles.css)), JS ([js/scripts.js](js/scripts.js))
- **Database:** SQLite (default, see [`DATABASES`](ryzen/ryzen/settings.py))
- **AI:** Cohere (see [`requirements.txt`](requirements.txt))

## Structure

- [`ryzen/`](ryzen/) - Django project root
  - [`core/`](ryzen/core/) - Home, login, base templates
  - [`member/`](ryzen/member/) - Member models, onboarding, dashboard, profile, AI analytics
  - [`communications/`](ryzen/communications/) - Coordinator messages, notifications
  - [`stokvel/`](ryzen/stokvel/) - Stokvel models, meetings, analytics
  - [`static/`](ryzen/static/) - Assets, CSS, JS
  - [`templates/`](ryzen/templates/) - Shared base template

- Standalone HTML pages for demo: `index.html`, `dashboard.html`, `profile.html`, `meeting.html`, `chatbot.html`, `KYC_newUser.html`, `KYC_oldUser.html`, `admin-user.html`, `contact.html`

## Setup

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```sh
   python ryzen/manage.py migrate
   ```

3. **Create superuser (optional):**
   ```sh
   python ryzen/manage.py createsuperuser
   ```
4. **(Optional) Load mock data:**
   ```sh
   python ryzen/manage.py mock_data
   ```
5. **Start the server:**
   ```sh
   python ryzen/manage.py runserver
   ```

## Usage

- Access the platform at [http://localhost:8000/](http://localhost:8000/)
- Onboard as a new user or login as an existing user.
- Explore dashboard, meetings, AI analytics, and more.

---

For more details, see the code in [ryzen/](ryzen/) and templates in [ryzen/templates/](ryzen/templates/).
