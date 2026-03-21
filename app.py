import streamlit as st
import sqlite3
import random
import os
import base64
import urllib.parse

def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

st.set_page_config(page_title="CineFliz", page_icon="icon.png", layout="wide", initial_sidebar_state="auto")

# --- Custom CSS ---
st.markdown("""
<style>
    /* Hide ONLY the Deploy button and right menu, keeping the sidebar toggle visible! */
    [data-testid="stHeaderActionElements"] {display: none;}
    header {background-color: transparent !important;}

    /* Dark Black Background */
    .stApp { background-color: #000000; color: white; }
    
    /* Pushed down slightly to perfectly fit the screen */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; max-width: 100%; }
    
    .bms-logo { font-size: 24px; font-weight: bold; color: white; margin-top: 5px;}
    .bms-logo span { background-color: #E50914; color: white; padding: 2px 5px; border-radius: 4px; margin-left: 2px;}
    
    /* Netflix Red Buttons with Animations */
    .stButton > button {
        background-color: #E50914 !important;
        color: white !important;
        border: 1px solid #E50914 !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease !important;
    }
    
    /* Hover Animation: Slight zoom and red glow */
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0px 4px 15px rgba(229, 9, 20, 0.5) !important;
        background-color: #f6121d !important;
        border-color: #f6121d !important;
        color: white !important;
    }
    
    /* Click Animation: Shrink slightly */
    .stButton > button:active {
        transform: scale(0.95) !important;
        box-shadow: none !important;
    }
    
    /* Disabled buttons (Taken Seats) styling */
    .stButton > button:disabled {
        background-color: #333 !important;
        border-color: #444 !important;
        color: #888 !important;
        transform: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Database Setup & Migration ---
conn = sqlite3.connect('cinema.db', check_same_thread=False, timeout=15)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users (username TEXT PRIMARY KEY, password TEXT)")

# Safely add the resale column to existing databases
try:
    c.execute("ALTER TABLE Bookings ADD COLUMN is_resale INTEGER DEFAULT 0")
    conn.commit()
except sqlite3.OperationalError:
    pass # Column already exists

conn.commit()

# --- Session State Management ---
if 'current_page' not in st.session_state: st.session_state.current_page = 'home'
if 'booking_movie_id' not in st.session_state: st.session_state.booking_movie_id = None
if 'selected_seats' not in st.session_state: st.session_state.selected_seats = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'show_auth' not in st.session_state: st.session_state.show_auth = False
if 'auth_mode' not in st.session_state: st.session_state.auth_mode = "Login"

# --- Authentication Logic ---
def authenticate(username, password, mode):
    if mode == "Sign Up":
        try:
            c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            st.success("Account created! Please log in.")
            st.session_state.auth_mode = "Login"
        except sqlite3.IntegrityError:
            st.error("Username already exists.")
        except sqlite3.OperationalError as e:
            st.error(f"Database error: {e}")
    else:
        c.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.show_auth = False
            st.rerun()
        else:
            st.error("Invalid credentials.")

# --- Sidebar (Help Manual & Contact) ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("---")
    
    st.header("Help Manual")
    with st.expander("How to Book a Ticket", expanded=True):
        st.markdown("""
        1. **Search**: Find your favorite movie using the top bar.
        2. **Location**: Select your city from the dropdown.
        3. **Book**: Click the red 'Book Tickets' button under a movie.
        4. **Sign In**: Log into your CineFliz account.
        5. **Select Seats**: Click available seats on the screen layout.
        6. **Pay & Checkout**: Click 'Pay & Book' to generate your E-Ticket!
        """)
        
    with st.expander("💺 Seat Legend", expanded=True):
        st.markdown("""
        * **🟥 Premium**: ₹250 (Top Rows)
        * **🟩 Standard**: ₹150 (Lower Rows)
        * **🟨 Resale**: 10% Discounted Tickets
        * **🟦 Selected**: Your current picks
        * **🚫 Taken**: Unavailable / Sold out
        """)
        
    st.markdown("---")
    st.header("Contact Us")
    
    st.markdown("**Arjun Pardeshi**")
    st.markdown("📧 [pardeshiarjun999@gmail.com](mailto:pardeshiarjun999@gmail.com)")
    st.markdown("🔗 [LinkedIn Profile](https://www.linkedin.com/in/arjun-pardeshi-05719b321)")
    
    st.markdown("<hr style='margin: 10px 0; border-top: 1px solid #333;'>", unsafe_allow_html=True)
    
    st.markdown("**Vedant Wahare**")
    st.markdown("📧 [vedantavcoe@gmail.com](mailto:vedantavcoe@gmail.com)")
    st.markdown("🔗 [LinkedIn Profile](https://www.linkedin.com/in/vedant-wahare-1964bb347?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Contact Support", use_container_width=True):
        st.success("Our support team has been notified. We will reach out to you shortly!")

# --- Navbar ---
col1, col2, col3, col4, col5 = st.columns([1.5, 4.5, 2, 1, 1])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h2 style='color:#E50914;'>CineFliz</h2>", unsafe_allow_html=True)
        
with col2:
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    search_query = st.text_input("Search", placeholder="🔍 Search for Movies, Events, Plays...", label_visibility="collapsed")
    
with col3:
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    selected_city = st.selectbox("Location", ["Pune", "Mumbai", "Delhi", "Bangalore", "Wardha", "Nashik", "Sangamner"], label_visibility="collapsed")
    
with col4:
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.session_state.logged_in:
        if st.button("My Bookings", use_container_width=True):
            st.session_state.current_page = 'my_bookings'
            st.session_state.show_auth = False
            st.rerun()
    else:
        if st.button("Sign In", use_container_width=True, type="primary"):
            st.session_state.show_auth = True
            st.rerun()
            
with col5:
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.session_state.logged_in:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.current_page = 'home'
            st.rerun()

st.markdown("---")

# --- Authentication Page ---
if st.session_state.show_auth:
    st.header(st.session_state.auth_mode)
    auth_col1, auth_col2 = st.columns([1, 2])
    with auth_col1:
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        if st.button("Submit", type="primary"):
            if user_input and pass_input:
                authenticate(user_input, pass_input, st.session_state.auth_mode)
            else:
                st.warning("Please fill all fields.")
        
        toggle_text = "Need an account? Sign Up" if st.session_state.auth_mode == "Login" else "Already have an account? Login"
        if st.button(toggle_text):
            st.session_state.auth_mode = "Sign Up" if st.session_state.auth_mode == "Login" else "Login"
            st.rerun()
        if st.button("← Back to Home"):
            st.session_state.show_auth = False
            st.rerun()

# --- Page 1: Home (Movie Grid) ---
elif st.session_state.current_page == 'home':
    st.image("https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=1600&h=300&q=80", width="stretch")
    
    if search_query:
        st.markdown(f"### Search Results for '{search_query}' in {selected_city}")
    else:
        st.markdown(f"### Recommended Movies in {selected_city}")
    
    try:
        if search_query:
            c.execute("SELECT id, title, genre, poster_url, trailer_url, review_url FROM Movies WHERE cities LIKE ? AND title LIKE ? COLLATE NOCASE", ('%' + selected_city + '%', '%' + search_query + '%'))
        else:
            c.execute("SELECT id, title, genre, poster_url, trailer_url, review_url FROM Movies WHERE cities LIKE ?", ('%' + selected_city + '%',))
        movies = c.fetchall()
    except sqlite3.OperationalError:
        c.execute("SELECT id, title, genre, poster_url, '', '' FROM Movies")
        movies = c.fetchall()
    
    if len(movies) == 0:
        st.warning(f"No movies currently showing for your search in {selected_city}.")
    else:
        cols = st.columns(5)
        for index, movie in enumerate(movies):
            m_id, m_title, m_genre, m_poster, m_trailer, m_review = movie
            with cols[index % 5]:
                
                if not os.path.exists(m_poster) and os.path.exists(m_poster.replace(".jpg", ".jpeg")):
                    m_poster = m_poster.replace(".jpg", ".jpeg")
                
                if os.path.exists(m_poster) and os.path.getsize(m_poster) > 1000:
                    img_b64 = get_image_base64(m_poster)
                    st.markdown(f"""
                    <img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; height: 350px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.4);">
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='height: 350px; background-color: #111111; border: 2px solid #E50914; 
                    color: #E50914; display: flex; align-items: center; justify-content: center; 
                    border-radius: 8px; text-align: center; padding: 10px; font-weight: bold; 
                    font-size: 18px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(229, 9, 20, 0.2); overflow: hidden;'>
                        {m_title}
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown(f"""
                <div style='height: 140px; display: flex; flex-direction: column; justify-content: flex-start;'>
                    <div style='font-weight: bold; line-height: 1.2; margin-bottom: 5px; font-size: 16px;'>{m_title}</div>
                    <div style='color: #888; font-size: 14px; margin-bottom: 10px;'>{m_genre}</div>
                    <div style='display: flex; gap: 5px; margin-top: auto;'>
                        <a href='{m_trailer}' target='_blank' style='flex: 1; text-align: center; background-color: #222; color: #ccc; text-decoration: none; padding: 6px; border-radius: 4px; font-size: 12px; border: 1px solid #444;'>▶ Trailer</a>
                        <a href='{m_review}' target='_blank' style='flex: 1; text-align: center; background-color: #222; color: #ccc; text-decoration: none; padding: 6px; border-radius: 4px; font-size: 12px; border: 1px solid #444;'>⭐ Moctale</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Book Tickets", key=f"btn_{m_id}_{selected_city}", use_container_width=True):
                    if not st.session_state.logged_in:
                        st.warning("Please Sign In to book tickets.")
                        st.session_state.show_auth = True
                        st.rerun()
                    else:
                        st.session_state.booking_movie_id = m_id
                        st.session_state.booking_movie_title = m_title
                        st.session_state.selected_seats = []
                        st.session_state.current_page = 'booking'
                        st.rerun()

    # ==========================================
    # NEW COMING SOON SECTION 
    # ==========================================
    st.markdown("<br><hr style='border: 1px solid #333;'><br>", unsafe_allow_html=True)
    st.markdown("### 🍿 Coming Soon to Theaters")
    
    upcoming_movies = [
        ("Toxic: A Fairy Tale for Grown-ups", "Action/Crime", "https://youtu.be/LYK5ETKbODE", "https://www.moctale.in/content/toxic-a-fairy-tale-for-grown-ups-2026"),
        ("Spider-Man: Brand New Day", "Action/Superhero", "https://youtu.be/aBlsrtxuwss", "https://www.moctale.in/content/spider-man-brand-new-day-2026"),
        ("Avengers: Doomsday", "Action/Sci-Fi", "https://www.youtube.com/watch?v=399Ez7WHK5s", "https://www.moctale.in/content/avengers-doomsday-2026"),
        ("The Odyssey", "Adventure/Fantasy", "https://www.youtube.com/watch?v=Mzw2ttJD2qQ", "https://www.moctale.in/content/the-odyssey-2026"),
        ("The Pride of Bharat - Chhatrapati Shivaji Maharaj", "Historical/Epic", "https://youtu.be/JwDD8ohhQ38", "https://www.moctale.in/content/the-pride-of-bharat-chhatrapati-shivaji-maharaj-20"),
        ("Mortal Kombat II", "Action/Fantasy", "https://www.youtube.com/watch?v=alVyFX7iQg8", "https://www.moctale.in/content/mortal-kombat-ii-2026"),
        ("Street Fighter", "Action/Martial Arts", "https://www.youtube.com/watch?v=tV2qoDVnfxs", "https://www.moctale.in/content/street-fighter-2026"),
        ("King", "Action/Thriller", "https://www.youtube.com/watch?v=M3mfut2RdHk", "https://www.moctale.in/content/king-2026"),
        ("Raja Shivaji", "Historical/Action", "https://youtu.be/02W08xqhmv0", "https://www.moctale.in/content/raja-shivaji-2026"),
        ("Drishyam 3", "Mystery/Thriller", "https://www.youtube.com/watch?v=jYbEYF1t-hk", "https://www.moctale.in/content/drishyam-3-2026-2")
    ]
    
    up_cols = st.columns(5)
    
    for idx, (u_title, u_genre, u_trailer, u_review) in enumerate(upcoming_movies):
        with up_cols[idx % 5]:
            upcoming_poster = f"posters/upcoming_{idx + 1}.jpg.jpeg"
            
            if os.path.exists(upcoming_poster) and os.path.getsize(upcoming_poster) > 1000:
                img_b64 = get_image_base64(upcoming_poster)
                st.markdown(f"""
                <div style="position: relative; margin-bottom: 15px;">
                    <img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; height: 350px; object-fit: cover; border-radius: 8px; box-shadow: 0px 4px 10px rgba(0,0,0,0.4);">
                    <div style='position: absolute; bottom: 15px; left: 50%; transform: translateX(-50%); background-color: rgba(0,0,0,0.85); font-size: 11px; color: #E50914; border: 1px solid #E50914; padding: 4px 10px; border-radius: 4px; font-weight: bold; letter-spacing: 1px; white-space: nowrap;'>RELEASING SOON</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='height: 350px; background-color: #0a0a0a; border: 2px dashed #444; 
                color: #888; display: flex; flex-direction: column; align-items: center; justify-content: center; 
                border-radius: 8px; text-align: center; padding: 10px; font-weight: bold; 
                font-size: 18px; margin-bottom: 15px; overflow: hidden;'>
                    <div>{u_title}</div>
                    <div style='margin-top: 15px; font-size: 12px; color: #E50914; border: 1px solid #E50914; padding: 3px 8px; border-radius: 4px;'>RELEASING SOON</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='height: 100px; display: flex; flex-direction: column; justify-content: space-between;'>
                <div>
                    <div style='font-weight: bold; line-height: 1.2; margin-bottom: 5px; font-size: 14px; color: #ccc;'>{u_title}</div>
                    <div style='color: #666; font-size: 13px; margin-bottom: 10px;'>{u_genre}</div>
                </div>
                <div style='display: flex; gap: 5px;'>
                    <a href='{u_trailer}' target='_blank' style='flex: 1; text-align: center; background-color: #1a1a1a; color: #aaa; text-decoration: none; padding: 5px; border-radius: 4px; font-size: 11px; border: 1px solid #333;'>▶ Trailer</a>
                    <a href='{u_review}' target='_blank' style='flex: 1; text-align: center; background-color: #1a1a1a; color: #aaa; text-decoration: none; padding: 5px; border-radius: 4px; font-size: 11px; border: 1px solid #333;'>⭐ Moctale</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- Page 2: My Bookings (Resale & Cancel Tickets) ---
elif st.session_state.current_page == 'my_bookings':
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.header(f"🎟️ My Bookings ({st.session_state.username})")
    
    # Updated query to pull the is_resale status
    c.execute('''
        SELECT Bookings.id, Movies.title, Showtimes.show_time, Bookings.seat_number, Bookings.is_resale
        FROM Bookings 
        JOIN Showtimes ON Bookings.showtime_id = Showtimes.id 
        JOIN Movies ON Showtimes.movie_id = Movies.id 
        WHERE Bookings.customer_name = ?
    ''', (st.session_state.username,))
    
    user_bookings = c.fetchall()
    
    if user_bookings:
        for booking in user_bookings:
            b_id, m_title, s_time, b_seat, is_resale = booking
            col_info, col_resale, col_cancel = st.columns([3, 1, 1])
            
            with col_info:
                badge = " &nbsp;|&nbsp; 🟨 **Listed for Resale**" if is_resale else ""
                st.markdown(f"**🎬 {m_title}** &nbsp;|&nbsp; 🕒 {s_time} &nbsp;|&nbsp; 💺 **Seat: {b_seat}**{badge}")
            
            with col_resale:
                if is_resale:
                    if st.button("Cancel Listing", key=f"unlist_{b_id}"):
                        c.execute("UPDATE Bookings SET is_resale = 0 WHERE id = ?", (b_id,))
                        conn.commit()
                        st.rerun()
                else:
                    if st.button("List for Resale", key=f"list_{b_id}"):
                        c.execute("UPDATE Bookings SET is_resale = 1 WHERE id = ?", (b_id,))
                        conn.commit()
                        st.rerun()
                        
            with col_cancel:
                if st.button("Cancel Ticket", key=f"cancel_{b_id}"):
                    c.execute("DELETE FROM Bookings WHERE id = ?", (b_id,))
                    conn.commit()
                    st.success(f"Seat {b_seat} has been successfully cancelled.")
                    st.rerun()
            st.markdown("---")
    else:
        st.info("You currently have no active movie bookings.")

# --- Page 3: Booking (Seat Grid & Purchasing) ---
elif st.session_state.current_page == 'booking':
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.header(f"Booking: {st.session_state.booking_movie_title} ({selected_city})")
    st.caption(f"Logged in as: **{st.session_state.username}**")
    
    c.execute("SELECT id, show_time FROM Showtimes WHERE movie_id = ?", (st.session_state.booking_movie_id,))
    showtime = c.fetchone()

    if showtime:
        showtime_id = showtime[0]
        st.write(f"**🕒 Showtime:** {showtime[1]}")
        
        # Updated query to check for resale status and current owner
        c.execute("SELECT seat_number, customer_name, is_resale FROM Bookings WHERE showtime_id = ?", (showtime_id,))
        seat_info = {row[0]: {'owner': row[1], 'is_resale': row[2] if len(row) > 2 else 0} for row in c.fetchall()}

        st.markdown("<br><h4 style='text-align: center; background-color: white; color: black; padding: 5px; border-radius: 5px; max-width: 600px; margin: auto;'>SCREEN THIS WAY</h4><br>", unsafe_allow_html=True)
        
        rows = ['A', 'B', 'C', 'D', 'E']
        _, col_center, _ = st.columns([1, 2, 1])
        
        with col_center:
            st.caption("🟥 Premium (₹250) | 🟩 Standard (₹150) | 🟨 Resale (-10%) | 🟦 Selected")
            for r in rows:
                cols = st.columns(5)
                for i, col in enumerate(cols):
                    seat_name = f"{r}{i+1}"
                    with col:
                        # Check if the seat is in the database
                        if seat_name in seat_info:
                            info = seat_info[seat_name]
                            
                            # If it's listed for resale and belongs to someone else
                            if info['is_resale'] == 1 and info['owner'] != st.session_state.username:
                                btn_label = f"🟦 {seat_name}" if seat_name in st.session_state.selected_seats else f"🟨 {seat_name}"
                                if st.button(btn_label, key=f"avail_res_{seat_name}"):
                                    if seat_name in st.session_state.selected_seats:
                                        st.session_state.selected_seats.remove(seat_name)
                                    else:
                                        st.session_state.selected_seats.append(seat_name)
                                    st.rerun()
                            else:
                                # Normal booked seat or user's own ticket
                                st.button(f"🚫 {seat_name}", disabled=True, key=f"taken_{seat_name}")
                        else:
                            # Standard available seat
                            if seat_name in st.session_state.selected_seats:
                                btn_label = f"🟦 {seat_name}"
                            else:
                                btn_label = f"🟥 {seat_name}" if r in ['A', 'B'] else f"🟩 {seat_name}"
                            
                            if st.button(btn_label, key=f"avail_{seat_name}"):
                                if seat_name in st.session_state.selected_seats:
                                    st.session_state.selected_seats.remove(seat_name)
                                else:
                                    st.session_state.selected_seats.append(seat_name)
                                st.rerun()

        st.markdown("---")
        
        if len(st.session_state.selected_seats) > 0:
            # Calculate price dynamically considering the 10% discount for resale tickets
            total_price = 0
            for s in st.session_state.selected_seats:
                base_price = 250 if s.startswith('A') or s.startswith('B') else 150
                if s in seat_info and seat_info[s]['is_resale'] == 1:
                    total_price += int(base_price * 0.9)  # 10% off
                else:
                    total_price += base_price
                    
            seats_str = ", ".join(st.session_state.selected_seats)
            
            st.info(f"**Seats:** {seats_str} | **Total:** ₹{total_price}")
            
            if st.button(f"Pay ₹{total_price} & Book", type="primary"):
                for seat in st.session_state.selected_seats:
                    if seat in seat_info and seat_info[seat]['is_resale'] == 1:
                        c.execute("UPDATE Bookings SET customer_name = ?, is_resale = 0 WHERE showtime_id = ? AND seat_number = ?", 
                                  (st.session_state.username, showtime_id, seat))
                    else:
                        c.execute("INSERT INTO Bookings (showtime_id, seat_number, customer_name, is_resale) VALUES (?, ?, ?, 0)", 
                                  (showtime_id, seat, st.session_state.username))
                conn.commit()
                
                st.session_state.selected_seats = [] 
                st.success("✅ Payment Successful!")
                
                # --- Dynamic QR Code Generation ---
                booking_id = random.randint(100000, 999999)
                qr_text = f"CineFliz Ticket | ID: #{booking_id} | Movie: {st.session_state.booking_movie_title} | Seats: {seats_str}"
                safe_qr_text = urllib.parse.quote_plus(qr_text)
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={safe_qr_text}"
                
                # --- UPDATED: Smart Logo Encoding (Checks for both .jpg and .png) ---
                logo_path = "logo.jpg"
                if not os.path.exists(logo_path) and os.path.exists("logo.png"):
                    logo_path = "logo.png"
                    
                logo_b64 = get_image_base64(logo_path) if os.path.exists(logo_path) else ""
                
                # Injecting the logo into the HTML
                logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 65px; margin-bottom: 15px;">' if logo_b64 else '<h3 style="color: #E50914; margin-top: 0; margin-bottom: 15px;">🎬 CineFliz E-Ticket</h3>'
                
                # --- UI: Display Dark-Mode Ticket in App ---
                st.markdown(f"""
                <div style="border: 2px solid #E50914; padding: 20px; border-radius: 10px; background-color: #111111; color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: 0px 4px 15px rgba(229, 9, 20, 0.2);">
                    <div>
                        {logo_html}
                        <div style="line-height: 1.6;">
                            <b>Booking ID:</b> #{booking_id}<br>
                            <b>Account:</b> {st.session_state.username}<br>
                            <b>Location:</b> {selected_city}<br>
                            <b>Movie:</b> {st.session_state.booking_movie_title}<br>
                            <b>Seats:</b> <span style="color: #E50914; font-weight: bold;">{seats_str}</span><br>
                            <b>Total Paid:</b> ₹{total_price}<br>
                        </div>
                    </div>
                    <div style="background-color: white; padding: 10px; border-radius: 8px; margin-left: 20px;">
                        <img src="{qr_url}" alt="Ticket QR Code" style="display: block; width: 110px; height: 110px;">
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # --- Generate Printable / PDF Format Ticket ---
                printable_logo = f'<img src="data:image/png;base64,{logo_b64}" style="height: 70px; margin-bottom: 10px;">' if logo_b64 else '<h2 style="color: #E50914;">CineFliz</h2>'
                
                printable_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>CineFliz Ticket #{booking_id}</title>
                    <style>
                        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                        .ticket {{ background-color: white; border: 2px dashed #888; padding: 40px; border-radius: 15px; width: 650px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0px 10px 30px rgba(0,0,0,0.1); }}
                        .details {{ line-height: 1.8; font-size: 18px; color: #333; }}
                        .highlight {{ color: #E50914; font-weight: bold; }}
                        .qr-box {{ border: 3px solid #eee; padding: 15px; border-radius: 10px; background: white; }}
                        @media print {{
                            body {{ background-color: white; align-items: flex-start; padding-top: 50px; }}
                            .ticket {{ box-shadow: none; border: 2px solid black; }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="ticket">
                        <div>
                            {printable_logo}
                            <div class="details">
                                <b>Booking ID:</b> #{booking_id}<br>
                                <b>Account:</b> {st.session_state.username}<br>
                                <b>Location:</b> {selected_city}<br>
                                <b>Movie:</b> {st.session_state.booking_movie_title}<br>
                                <b>Seats:</b> <span class="highlight">{seats_str}</span><br>
                                <b>Total Paid:</b> ₹{total_price}<br>
                            </div>
                        </div>
                        <div class="qr-box">
                            <img src="{qr_url}" alt="QR Code" width="150" height="150">
                        </div>
                    </div>
                    <script>
                        window.onload = function() {{ window.print(); }}
                    </script>
                </body>
                </html>
                """
                
                # --- UPDATED: Red Download Button (Added type="primary") ---
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="Download & Print Ticket",
                    data=printable_html,
                    file_name=f"CineFliz_Ticket_{booking_id}.html",
                    mime="text/html",
                    use_container_width=True,
                    type="primary"
                )

# ==========================================
# --- GLOBAL FOOTER ---
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True)

logo_path_footer = "logo.jpg"
if not os.path.exists(logo_path_footer) and os.path.exists("logo.png"):
    logo_path_footer = "logo.png"

footer_logo_b64 = get_image_base64(logo_path_footer) if os.path.exists(logo_path_footer) else ""
footer_logo_html = f'<img src="data:image/png;base64,{footer_logo_b64}" style="height: 50px; margin: 0 auto; display: block;">' if footer_logo_b64 else '<h2 style="color: #E50914; text-align: center; margin: 0;">CineFliz</h2>'

# Note: All HTML is pushed to the far left so Streamlit doesn't turn it into a Code Block!
st.markdown(f"""
<div style="background-color: #0a0a0a; padding: 40px 20px 30px 20px; border-top: 1px solid #333; margin-top: 40px; text-align: center;">
<div style="margin-bottom: 25px;">
{footer_logo_html}
</div>
<div style="color: #777; font-size: 12px; line-height: 1.6; max-width: 900px; margin: 0 auto;">
Copyright 2026 © CineFliz Entertainment Pvt. Ltd. All Rights Reserved.<br><br>
The content and images used on this site are copyright protected and copyrights vests with the respective owners. The usage of the content and images on this website is intended to promote the works and no endorsement of the artist shall be implied. Unauthorized use is prohibited and punishable by law.
</div>
</div>
""", unsafe_allow_html=True)