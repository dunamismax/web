# DunamisMax

**DunamisMax** is a suite of modern web applications built with FastAPI. It includes a real-time Messenger and AI-powered Agents, offering seamless communication and intelligent assistance.

## Features

- **Messenger:** Real-time chat using WebSockets.
- **AI Agents:** Interactive AI assistants for various tasks.
- **Responsive Design:** Optimized for all devices.
- **Clean UI:** Consistent styling with the Nord color palette.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/dunamismax/DunamisMax.git
   cd DunamisMax
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the Application**

   - **Main Page:** `http://localhost:8000`
   - **Messenger:** `http://localhost:8000/messenger`
   - **AI Agents:** `http://localhost:8000/ai_agents`

## Contact

- **Email:** [dunamismax@tutamail.com](mailto:dunamismax@tutamail.com)
- **GitHub:** [github.com/dunamismax](https://github.com/dunamismax)
- **Beaker Profile:** [bsky.app/profile/dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)
