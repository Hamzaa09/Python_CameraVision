🖐️ Hand Gesture Controller
A Touch-Free Human–Computer Interaction System Powered by Computer Vision

🌟 Overview
This project turns your webcam into an intelligent gesture-controlled interface, allowing you to interact with your computer using nothing but hand movements.
Built using Python, OpenCV, Mediapipe, and PyCAW, it redefines basic interactions like mouse movement, scrolling, media control, and system volume — all through real-time gesture recognition.

🎥 Demo
https://www.linkedin.com/feed/update/urn:li:activity:7403464015386959873/
A short demonstration showcasing real-time gesture recognition and system control.

✨ Highlights

✔ Real-time hand tracking using Mediapipe
✔ Touchless mouse movement
✔ Gesture-based left & right clicks
✔ Volume adjustment using pinch distance
✔ Scrolling controls
✔ Media skip forward/backward
✔ Smooth & responsive performance (High FPS)
✔ Clean, intuitive on-screen UI overlay

🧠 How It Works (Conceptual Overview)

Detects your hand through the webcam
Identifies 21 landmark points
Determines which fingers are up
Maps each gesture to a specific computer action
Executes system-level functions such as mouse movement, scroll, or volume control

No buttons. No keyboard. No mouse.
Just pure hand interaction.

📌 Features in Action

🖱️ Mouse Control
Move your hand with Index and Middle fingers up → Move your cursor in real time

👆 Clicks
Index finger up → Left click
Middle finger up → Right click

🎵 Media Control
Pinky up → Skip forward
Thumb up → Skip backward

🔊 Volume Control
Bring thumb + index together → Adjust system volume
Smooth animation + visual volume bar included

🔄 Scrolling
Three or four fingers → Scroll up/down

🛠️ Tech Stack

Python
OpenCV
Mediapipe (Custom module)
NumPy
Mouse & PyAutoGUI

PyCAW (System volume control)
