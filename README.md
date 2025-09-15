# Streamlit OpenAI App

This project is a Streamlit application that interacts with the OpenAI API using Azure's ChatCompletionsClient. It provides a user-friendly interface for sending messages and receiving responses from the AI model.

## Project Structure

```
streamlit-openai-app
├── src
│   ├── app.py          # Main entry point of the Streamlit application
│   └── types
│       └── index.py    # Custom types and data structures
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd streamlit-openai-app
   ```

2. **Create a Virtual Environment**
   It is recommended to create a virtual environment to manage dependencies.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   Install the required packages listed in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Make sure to set the `GITHUB_TOKEN` environment variable with your Azure OpenAI API key.
   ```bash
   export GITHUB_TOKEN='your_api_key'  # On Windows use `set GITHUB_TOKEN=your_api_key`
   ```

## Usage

To run the Streamlit application, execute the following command:
```bash
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to interact with the application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.