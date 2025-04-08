PRAGMA foreign_keys = ON;

-- THEATRE
CREATE TABLE IF NOT EXISTS THEATRE (
    theatre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT,
    contact_number TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- SCREEN
CREATE TABLE IF NOT EXISTS SCREEN (
    screen_id INTEGER PRIMARY KEY AUTOINCREMENT,
    theatre_id INTEGER NOT NULL,
    screen_name TEXT NOT NULL,
    capacity INTEGER CHECK(capacity > 0),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (theatre_id) REFERENCES THEATRE(theatre_id) ON DELETE CASCADE
);

-- SEAT_LAYOUT
CREATE TABLE IF NOT EXISTS SEAT_LAYOUT (
    layout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    screen_id INTEGER NOT NULL,
    layout_name TEXT,
    layout_type TEXT CHECK(layout_type IN ('standard', 'recliner')),
    total_rows INTEGER CHECK(total_rows > 0),
    total_columns INTEGER CHECK(total_columns > 0),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (screen_id) REFERENCES SCREEN(screen_id) ON DELETE CASCADE
);

-- SEAT
CREATE TABLE IF NOT EXISTS SEAT (
    seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    layout_id INTEGER NOT NULL,
    row_label TEXT NOT NULL,
    seat_number TEXT NOT NULL,
    seat_category TEXT CHECK(seat_category IN ('Premium', 'Standard')),
    is_accessible INTEGER DEFAULT 0 CHECK(is_accessible IN (0, 1)),
    price REAL CHECK(price >= 0),
    status TEXT DEFAULT 'AVAILABLE' CHECK(status IN ('AVAILABLE', 'BOOKED')),
    FOREIGN KEY (layout_id) REFERENCES SEAT_LAYOUT(layout_id) ON DELETE CASCADE
);

-- MOVIE
CREATE TABLE IF NOT EXISTS MOVIE (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    genre TEXT,
    language TEXT,
    duration INTEGER CHECK(duration > 0),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- SHOW
CREATE TABLE IF NOT EXISTS SHOW (
    show_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    screen_id INTEGER NOT NULL,
    show_time TEXT NOT NULL, -- ISO 8601 (e.g., '2025-04-08T14:30:00')
    ticket_price REAL NOT NULL CHECK(ticket_price >= 0),
    status TEXT DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'CANCELLED', 'COMPLETED')),
    FOREIGN KEY (movie_id) REFERENCES MOVIE(movie_id) ON DELETE RESTRICT,
    FOREIGN KEY (screen_id) REFERENCES SCREEN(screen_id) ON DELETE CASCADE
);

-- CUSTOMER
CREATE TABLE IF NOT EXISTS CUSTOMER (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone_number TEXT UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ADMIN
CREATE TABLE IF NOT EXISTS ADMIN (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone_number TEXT UNIQUE,
    role TEXT NOT NULL DEFAULT 'Manager',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- LOGIN
CREATE TABLE IF NOT EXISTS LOGIN (
    login_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    user_type TEXT NOT NULL CHECK (user_type IN ('CUSTOMER', 'ADMIN')),
    user_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT,
    UNIQUE(user_type, user_id)
);

-- BOOKING
CREATE TABLE IF NOT EXISTS BOOKING (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    booking_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL CHECK(total_amount >= 0),
    payment_method TEXT CHECK(payment_method IN ('CASH', 'CARD', 'UPI')),
    booking_status TEXT NOT NULL CHECK(booking_status IN ('CONFIRMED', 'PENDING', 'CANCELLED')),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id) ON DELETE RESTRICT
);

-- TICKET
CREATE TABLE IF NOT EXISTS TICKET (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER NOT NULL,
    booking_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    ticket_type TEXT CHECK(ticket_type IN ('ADULT', 'CHILD')),
    FOREIGN KEY (show_id) REFERENCES SHOW(show_id) ON DELETE RESTRICT,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES SEAT(seat_id) ON DELETE RESTRICT,
    UNIQUE (show_id, seat_id)
);

-- AUDIT_LOG (for admin actions)
CREATE TABLE IF NOT EXISTS AUDIT_LOG (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    action_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (admin_id) REFERENCES ADMIN(admin_id) ON DELETE RESTRICT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_screen_theatre ON SCREEN(theatre_id);
CREATE INDEX IF NOT EXISTS idx_seatlayout_screen ON SEAT_LAYOUT(screen_id);
CREATE INDEX IF NOT EXISTS idx_seat_layout ON SEAT(layout_id);
CREATE INDEX IF NOT EXISTS idx_show_movie ON SHOW(movie_id);
CREATE INDEX IF NOT EXISTS idx_show_screen ON SHOW(screen_id);
CREATE INDEX IF NOT EXISTS idx_show_time ON SHOW(show_time);
CREATE INDEX IF NOT EXISTS idx_booking_customer ON BOOKING(customer_id);
CREATE INDEX IF NOT EXISTS idx_ticket_show ON TICKET(show_id);
CREATE INDEX IF NOT EXISTS idx_ticket_booking ON TICKET(booking_id);
CREATE INDEX IF NOT EXISTS idx_ticket_seat ON TICKET(seat_id);
CREATE INDEX IF NOT EXISTS idx_audit_admin ON AUDIT_LOG(admin_id);