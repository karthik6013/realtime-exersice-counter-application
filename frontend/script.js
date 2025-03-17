// Function to handle "Start" button clicks for exercises
function startExercise(exercise) {
    fetch("/start-exercise", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ exercise: exercise }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Attach event listeners to each exercise start button
document.getElementById("startSquat").addEventListener("click", function() {
    startExercise("squat");
});

document.getElementById("startBicepCurl").addEventListener("click", function() {
    startExercise("bicep_curl");
});

document.getElementById("startDeadlift").addEventListener("click", function() {
    startExercise("deadlift");
});

document.getElementById("startPullUp").addEventListener("click", function() {
    startExercise("pull_up");
});

document.getElementById("startPushUp").addEventListener("click", function() {
    startExercise("push_up");
});
