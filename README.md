# Routiner: CS50 Final Project

### Video Demo: <URL HERE>

### Description:

Routiner is a website that helps user to manage their to-do list.
A User can

- Add, Delete, or Edit tasks
- Choose a prioirty
- Set start date
- Set end date
- Change status

### Contact me: <a herf= "https://www.linkedin.com/in/ahmed-yasser-elbrmbaly/"> Linked In </a>

<br>

# Libraries

- `cs50`

  - `SQL`

- `flask`

  - `Flask`
  - `flash`
  - `redirect`
  - `render_template`
  - `request`
  - `session` -` url_for`

- `flask_session`

  - `Session`

- `tempfile`

  - `mkdtemp`

- `werkzeug.security`

  - `check_password_hash`
  - `generate_password_hash`

- `pyIsEmail` library used to validate email address

  - `is_email`

- `datetime`

  - `datetime`

- `calendar`

- `os`

- `requests`

- `urllib.parse`

# Files Structure

├── Database schema - Copy.drawio >> DataBase light Deisgn<br>
├── Database schema - Copy.drawio.png >> DataBase light Deisgn<br>
├── Database schema.drawio >> DataBase Heavy Deisgn<br>
├── Database schema.drawio.png >> DataBase Heavy Deisgn <br>
├── README.md >> Readme file<br>
├── app.py >> Flask Application<br>
├── helper.py >> Python helper file<br>
├── routiner.db >> database<br>
├── static<br>
│ └── logo.png >> wesite logo<br>
└── templates<br>
├── add.html<br>
├── edit.html<br>
├── index.html<br>
├── layout.html<br>
├── login.html<br>
├── profile.html<br>
└── register.html<br>

# Templates

- [x] Layout
- [x] Index
- [x] Registration
- [x] Login
- [x] Profile
- [x] Add
- [x] Edit
- [x] Profile

# Routes

- [x] Index
- [x] Registration
- [x] Login
- [x] Profile
- [x] Add
- [x] Edit
- [x] Profile
- [x] Delete

# CRUD Operations Implemented

- `Create`
  - New user
  - New Task
- `Read`

  - User details
  - Task details

- `Update`

  - User Details
  - Task details

- `Delete`
  - Task Details

# Database Deigning - Light Version

(I found it very complicated to implement this version of the app so I implemeted a light version)

<img src="Database schema - Copy.drawio.png">

# Database configration - Light version

- Create Tables:

  - ```
    CREATE TABLE users(
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        user_name TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
      );

    ```

- ```
    CREATE TABLE routines(
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        priority INT,
        start_date DATETIME NOT NULL,
        end_date DATETIME,
        status text,

        CONSTRAINT fk_user_id
          FOREIGN KEY (user_id)
          REFERENCES users(id),

        CONSTRAINT CHK_Name
        CHECK (
                status = "Done-On-Time"
                OR status = "Done"
                OR status = "Not-Set"
                OR status = "Missed"),

        CONSTRAINT CHK_Priority
        CHECK(
              priority>=1
              AND priority<=5)


      );

  ```

  # Database Deigning - Heavy Version

(I found it very complicated to implement this version of the app so I implemeted a light version)

<img src="Database schema.drawio.png">

# Database configration - heavy version

- Create Tables:

  - ```
    CREATE TABLE users(
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        user_name TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
      );

    ```

  - ```
    CREATE TABLE routines(
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        start_date DATETIME NOT NULL,
        end_date DATETIME,
        weight INT,
        degree INT,
        CONSTRAINT fk_user_id
          FOREIGN KEY (user_id)
          REFERENCES users(id)

      );

    ```

  - ```
    CREATE TABLE status(
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,

        CONSTRAINT CHK_Name
        CHECK (
                name = "Done On Time"
                OR name = "Done"
                OR name = "Not Set"
                OR name = "Missed")

      );

    ```

  - ```
    CREATE TABLE logs(
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        user_id INTEGER NOT NULL,
        routine_id INTEGER NOT NULL,
        date DATETIME NOT NULL,
        status_id INTEGER NOT NULL,

        CONSTRAINT fk_user_id
          FOREIGN KEY (user_id)
          REFERENCES users(id),

         CONSTRAINT fk_routine_id
          FOREIGN KEY (routine_id)
          REFERENCES routines(id),

         CONSTRAINT fk_status_id
          FOREIGN KEY (status_id)
          REFERENCES status(id)

      );

    ```

- Create indexes

  - ```
    CREATE UNIQUE INDEX user_id
      ON users (id);
    ```

  - ```
    CREATE UNIQUE INDEX user_name
      ON users (user_name);
    ```

  - ```
    CREATE UNIQUE INDEX routine_id
      ON routines (id);
    ```

  - ```
    CREATE UNIQUE INDEX logs_id
      ON logs (id);
    ```

  - ```
    CREATE UNIQUE INDEX status_id
      ON status (id);
    ```

- ```
  ALTER TABLE routines RENAME COLUMN weight To priority;
  ```

- I have to edit the database but the sqlite doesn't support and I lazy to drop the table and create it again 😂

  ```
    ALTER TABLE routines
    add check(priority>=1 and priority<=5>);
  ```
