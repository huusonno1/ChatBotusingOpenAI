# ChatBot using OpenAI

A simple chatbot implementation using OpenAI's API.

## Prerequisites

- Python 3.x
- PyCharm IDE (recommended)
- OpenAI API key

## Installation

1. Clone the repository and open it in PyCharm.

2. Set up a virtual environment (venv):
   - In PyCharm, go to `File → Settings → Project → Python Interpreter`
   - Click the gear icon and select "Add"
   - Choose "Virtual Environment" and select the location and base interpreter
   - For detailed instructions, visit: [PyCharm Virtual Environment Setup](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements)

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the data manager:
   ```bash
   python data_manager.py
   ```
   Note: You can modify the data as needed.

## Configuration

1. Configure the Run Configuration in PyCharm:
   - Click "Add Configuration" or "Edit Configurations"
   - Set the Application file to: `[your_project_path]/ChatBotusingOpenAI/app/main.py`
   - Select the Python interpreter to use your newly created virtual environment
   - ![image](https://github.com/user-attachments/assets/68760559-6ea2-4c84-9b2c-95d16c8b6644)
   - ![image](https://github.com/user-attachments/assets/a21e8315-ee13-4537-9376-79c76680f9eb)

2. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   - ![image](https://github.com/user-attachments/assets/a5c1dfd3-5c68-412e-b4a0-d7d4743e88ce)

## Running the Application

1. Click the Run button in PyCharm or use the following command in terminal:
   ```bash
   python app/main.py
   ```
   - ![image](https://github.com/user-attachments/assets/a422911b-598c-49c2-b470-8a78b4b5edfa)

2. Access the application at: `http://127.0.0.1:8000/`

## Screenshots

The application interface provides a clean chat interface where you can interact with the OpenAI-powered chatbot.
  - ![image](https://github.com/user-attachments/assets/ab2495a9-95bd-4f94-93ba-6a463910c714)

## Note

Make sure to keep your API key confidential and never commit the `.env` file to version control.

## Contributing

Feel free to submit issues and enhancement requests.
