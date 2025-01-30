# DunamisMax AI Agents

**DunamisMax AI Agents** provides interactive AI-powered assistants built with FastAPI, offering intelligent responses and assistance for various tasks.

## Features

- **AI Interaction:** Engage with intelligent AI agents.
- **Multiple Personalities:** Different AI agents with unique traits.
- **Responsive Design:** Accessible on all devices.
- **Seamless Integration:** Consistent UI with the main DunamisMax site.

## Installation

1. **Navigate to AI Agents Directory**

   ```bash
   cd app/ai_agents
   ```

2. **Activate Virtual Environment**

   ```bash
   source ../../venv/bin/activate  # On Windows: ../../venv/Scripts/activate
   ```

3. **Set Up Environment Variables**

   Create a `.env` file and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the AI Agents**

   ```bash
   uvicorn agents.agents:app --host 0.0.0.0 --port 8002 --reload
   ```

5. **Access AI Agents**

   Open [http://localhost:8002](http://localhost:8002) in your browser.

## Contact

- **Email:** [dunamismax@tutamail.com](mailto:dunamismax@tutamail.com)
- **GitHub:** [github.com/dunamismax](https://github.com/dunamismax)
- **Beaker Profile:** [bsky.app/profile/dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)
