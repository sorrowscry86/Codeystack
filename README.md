# Studio Lite Multi-LLM Provider API

Studio Lite is a Flask-based application designed to integrate multiple Large Language Model (LLM) providers, offering a unified API for interacting with various LLMs. The application also includes a Streamlit frontend for user-friendly interaction.

## Features
- **Multi-LLM Provider Integration**: Supports multiple LLM providers, including OpenAI, Anthropic, Google, and LM Studio.
- **Dynamic Model Fetching**: Fetch available models dynamically from LM Studio and other providers.
- **Streamlit Frontend**: Interactive UI for configuring providers, selecting models, and launching tasks.
- **RESTful API**: Provides endpoints for health checks, provider configurations, chat completions, and model listings.

## Installation

### Prerequisites
- Python 3.11 or higher
- Docker (optional, for containerized deployment)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/sorrowscry86/Codeystack.git
   cd Codeystack
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   python app.py
   ```

## Usage

### Endpoints
- **GET `/`**: Health check endpoint.
- **GET `/providers`**: List available LLM providers and their configurations.
- **POST `/chat`**: Generate chat completions using the specified provider and model.
- **GET `/config/<provider_name>`**: Retrieve provider configuration.
- **POST `/config/<provider_name>`**: Update provider configuration.
- **GET `/api/models`**: List available models for all providers.

### Streamlit Frontend
1. Run the Streamlit frontend:
   ```bash
   streamlit run studio_lite.py
   ```
2. Access the UI at `http://localhost:8501`.

## Docker Deployment
1. Build the Docker image:
   ```bash
   docker-compose build
   ```
2. Start the container:
   ```bash
   docker-compose up
   ```

## File Structure
- `app.py`: Main Flask application.
- `studio_lite.py`: Streamlit frontend.
- `llm_providers/`: Contains provider-specific implementations.
- `config/`: Configuration management.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Docker setup.
- `docker-compose.yml`: Docker Compose setup.

## Contributing
Feel free to submit issues or pull requests to improve the application.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, contact [sorrowscry86](https://github.com/sorrowscry86).
