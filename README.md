# Routiner

# Database Deigning

<img src="Database schema.drawio.png">

# Database configration

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
