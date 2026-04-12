Hello!
Before explaining how to run the project, I want to clarify an important detail about my development environment.

During implementation, I encountered a critical issue with WSL on my machine. This caused docker-compose to fail on startup, and after investigating, it appeared to be a deeper Windows/WSL subsystem problem that would require a full system repair or reinstallation. Because of this, I was unable to run Docker locally and fully test the application in a containerized environment.

I attempted to connect the backend to a local PostgreSQL instance (PGAdmin), but due to the same underlying WSL issue, the database connection could not be established reliably.

Despite these limitations, the project structure, code, and logic were implemented according to the requirements. Below is the intended way to launch the application once the environment is functioning normally.

**Starting the app**
To start the app you need to have docker-compose. 
Add your env as shown in the .env.sample. Add secret key all other env values may not be changed.
Download requirements via **pip install -r requirements.txt**
Start the docker-compose application and run **docker-compose up --build** command.
Then run **alembic upgrade heads**
That is it, the application works.