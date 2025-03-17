# realtime-exersice-counter-application

## Overview
This project is a real-time exercise counter that uses **MediaPipe** to track body movements and count repetitions for various exercises. It is an AI-powered web application that enables users to monitor their workout progress using computer vision.

## Features
- Real-time exercise tracking using **MediaPipe**
- Supports multiple exercises:
  - Bicep Curls
  - Squats
  - Push-ups
  - Pull-ups
  - Deadlifts
  - Lunges
- Live video feed processing
- Interactive and intuitive UI for users
- Web-based interface for accessibility

## Technologies Used
- **Python** (for backend and AI processing)
- **MediaPipe** (for pose detection and tracking)
- **Flask** (backend server)
- **JavaScript, HTML, CSS** (for frontend development)
- **OpenCV** (for real-time video processing)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- OpenCV
- MediaPipe
- Flask

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/real_time_exercise_counter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd real_time_exercise_counter
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python server.py
   ```
5. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Usage
- Open the web application in a browser.
- Enable camera access when prompted.
- Select the desired exercise.
- Perform the exercise in front of the camera, and the system will count your repetitions in real time.

## Future Enhancements
- Add more exercise types
- Improve accuracy of pose detection
- Provide real-time feedback on form
- Develop a mobile app version

## Contributing
Feel free to contribute by submitting issues, feature requests, or pull requests.

## License
This project is licensed under the MIT License.

---
Developed by **[Your Name]**

