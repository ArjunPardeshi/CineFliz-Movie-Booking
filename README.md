

 CineFliz - Premium Movie Ticket
## Booking Platform
CineFliz is a fully functional, highly interactive movie ticket booking application built using
Python and Streamlit. Designed with a sleek, custom dark-mode UI, it replicates the core
functionalities of modern ticketing platforms like BookMyShow, while introducing unique
features like Peer-to-Peer ticket reselling and dynamic QR code generation.
## ✨ Key Features
User Authentication: Secure sign-up and login system for users to manage their
bookings.
Location-Based Filtering: Browse recommended movies actively showing in selected
cities (Pune, Mumbai, Delhi, etc.).
Interactive Seat Selection: Visual theater screen layout with categorized pricing (
## Premium - ₹250,  Standard - ₹150).
 Peer-to-Peer Ticket Resale: Users can list their purchased tickets for resale. Other
users can buy these listed tickets at a 10% discount.
E-Tickets with Dynamic QR Codes: Generates a real-time, scannable QR code on the
final ticket for easy validation.
 Downloadable PDF Tickets: One-click generation of a white-themed, ink-friendly
printable HTML/PDF ticket.
Media Integration: Direct links to official YouTube trailers and Moctale/IMDb reviews for
upcoming and current movies.
Custom UI/UX: Fully customized CSS overriding standard Streamlit elements to provide a
seamless, native website feel (hidden default headers, custom Netflix-red animated
buttons, professional footer).
##  Tech Stack
Frontend & Framework:Streamlit
Backend & Database: Python, SQLite (sqlite3)
External APIs:QR Server API (for dynamic QR code generation)
3/21/26, 8:57 PMCineFliz Documentation
file:///C:/Users/parde/Downloads/CineFliz_Documentation.html1/3

## 
Styling: Custom HTML/CSS injected via Streamlit markdown
##  Project Structure
CineFliz/
## │
├── app.py              # Main Streamlit application file containing UI and logic
├── seed_db.py          # Database initialization script (creates tables & populates init
├── cinema.db           # SQLite database (generated automatically)
├── logo.png / .jpg     # Main branding logo used in the navbar and tickets
├── icon.png / .jpg     # Custom favicon for the browser tab
└── posters/            # Directory containing dynamically fetched movie poster images
##  Installation & Setup
Because CineFliz relies largely on Python's built-in libraries (sqlite3, urllib, base64, os),
the setup process is incredibly lightweight.
- Clone or Download the Repository
Ensure all files (app.py, seed_db.py, and your logo files) are in the same folder.
## 2. Install Streamlit
Open your terminal or command prompt and run:
pip install streamlit
- Initialize the Database
Run the seeder script to build the SQLite database, fetch the movie posters, and populate the
movie tables with YouTube and Moctale links.
python seed_db.py
- Run the Application
Launch the Streamlit app locally:
streamlit run app.py
The app will automatically open in your default web browser at http://localhost:8501.
3/21/26, 8:57 PMCineFliz Documentation
file:///C:/Users/parde/Downloads/CineFliz_Documentation.html2/3

 How to Use
- Sign Up / Log In: Create an account using the "Sign In" button in the top right.
- Select a City: Use the dropdown in the navbar to filter movies by your location.
- Book Tickets: Click on a movie to view showtimes and access the interactive seat map.
- Checkout: Pay for your selected seats to instantly generate your E-Ticket and QR Code.
- Print: Click the "Download & Print" button to save your ticket as a PDF.
- Resell: Go to "My Bookings" via the navbar to cancel tickets or list them on the resale
market for other users to buy.
## ‍ Creators & Support
## Arjun Pardeshi
 Email: pardeshiarjun999@gmail.com
 LinkedIn
## Vedant Wahare
 Email: vedantavcoe@gmail.com
 LinkedIn
Copyright 2026 ©CineFliz All Rights Reserved.
3/21/26, 8:57 PMCineFliz Documentation
file:///C:/Users/parde/Downloads/CineFliz_Documentation.html3/3