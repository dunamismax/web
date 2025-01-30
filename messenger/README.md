# DunamisMax Messenger

**DunamisMax Messenger** is a real-time chat application built with FastAPI and WebSockets, enabling instant communication between users.

## Features

- **Real-Time Chat:** Instant message delivery using WebSockets.
- **User Authentication:** Unique username-based login.
- **Responsive Interface:** Works seamlessly on all devices.
- **Clean Design:** Consistent styling with the main DunamisMax site.

## Installation

1. **Navigate to Messenger Directory**

   ```bash
   cd app/messenger
   ```

2. **Activate Virtual Environment**

   ```bash
   source ../../venv/bin/activate  # On Windows: ../../venv/Scripts/activate
   ```

3. **Run the Messenger**

   ```bash
   uvicorn messenger.messenger:app --host 0.0.0.0 --port 8001 --reload
   ```

4. **Access Messenger**

   Open [http://localhost:8001](http://localhost:8001) in your browser.

## Contact

- **Email:** [dunamismax@tutamail.com](mailto:dunamismax@tutamail.com)
- **GitHub:** [github.com/dunamismax](https://github.com/dunamismax)
- **Beaker Profile:** [bsky.app/profile/dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)