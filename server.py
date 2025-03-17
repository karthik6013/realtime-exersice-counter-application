from flask import Flask, render_template
import webbrowser
import subprocess
import threading
import os

app = Flask(__name__)

# Automatically open the web browser to the server's URL
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

@app.route('/')
def index():
    return render_template("index.html")  # Ensure index.html is in the 'templates' folder

@app.route('/start/<exercise>')
def start_exercise(exercise):
    exercise_map = {
        'squat': 'SquatCounter_live.py',
        'bicepCurl': 'BicepCurlCounter_live.py',
        'deadlift': 'DeadliftCounter_live.py',
        'pullUp': 'PullUpCounter_live.py',
        'pushUp': 'PushupCounter_live.py',
        'lunges': 'LungesCounter_live.py'
    }
    
    if exercise in exercise_map:
        script_name = exercise_map[exercise]
        
        try:
            # Launch the exercise script in a separate process
            subprocess.Popen(['python', script_name], shell=True)
            return f"<h3>Started {exercise.capitalize()} Counter</h3>"
        except Exception as e:
            return f"<h3>Error: Could not start {exercise.capitalize()} Counter. {e}</h3>"
    else:
        return "<h3>Error: Invalid exercise selected.</h3>"

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()  # Opens the browser after server starts
    app.run(debug=True)
