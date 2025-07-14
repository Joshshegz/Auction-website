Auction Website
A Django-based online auction platform where users can create, bid on, and manage auction listings. This project includes features like user authentication, listing creation, bidding, watchlists, comments, and category-based browsing.
Table of Contents

Features
Technologies Used
Installation
Usage
Project Structure
Contributing
License

Features

User Authentication: Register, login, and logout functionality.
Auction Listings: Create, view, and manage auction listings.
Bidding System: Place bids on active listings.
Watchlist: Add or remove listings to a personal watchlist.
Comments: Add comments to listings for interaction.
Categories: Browse listings by categories.
Admin Panel: Manage listings, users, and other data via Django admin.

Technologies Used

Backend: Django (Python)
Frontend: HTML, CSS, Bootstrap
Database: SQLite (default, configurable for others like PostgreSQL)
Python Libraries: Django, Pillow (for image handling)

Installation
Prerequisites

Python 3.8+
pip (Python package manager)
Virtualenv (optional but recommended)

Steps

Clone the Repository:
git clone https://github.com/Joshshegz/Auction-website.git
cd Auction-website/commerce


Set Up a Virtual Environment (optional):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Apply Migrations:
python manage.py makemigrations
python manage.py migrate


Create a Superuser (for admin access):
python manage.py createsuperuser


Run the Development Server:
python manage.py runserver


Open your browser and navigate to http://127.0.0.1:8000.


Usage

Homepage: View all active auction listings.
Create Listing: Authenticated users can create new listings with a title, description, starting bid, image, and category.
Bidding: Place bids on listings (must be higher than the current bid).
Watchlist: Add listings to your watchlist for easy access.
Comments: Add comments to listings to ask questions or provide feedback.
Admin Panel: Access http://127.0.0.1:8000/admin to manage the site (requires superuser login).

Project Structure
commerce/
├── auctions/              # Main app directory
│   ├── migrations/        # Database migrations
│   ├── static/            # Static files (CSS, images)
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models (User, AuctionListing, Bid, Comment, etc.)
│   ├── views.py           # View functions for handling requests
│   ├── urls.py            # URL routing
├── commerce/              # Project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Project-wide URL routing
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies

Contributing

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
