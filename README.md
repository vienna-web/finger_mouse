# 🖐️ Finger Mouse – Hand Tracking Mouse Control
made by xmcure enjoy guys 

Control your mouse using your hand through a webcam using **Python**, **OpenCV**, and **MediaPipe**.

This project tracks your hand and translates gestures into mouse movement and actions.

---
## 💖 Support / Donate

If you enjoy using **Finger Mouse** and want to support development, you can make a donation via PayPal:

[Donate via PayPal](https://www.paypal.com/paypalme/aymanehaddouba)

Every contribution helps keep this project alive and updated!  
Thank you for your support 🙏 
## Commercial License

This project is free for personal and educational use.

Commercial use requires a paid license.

Buy here: https://payhip.com/b/JuBhw

If the Payhip checkout does not work for you, you may donate via PayPal.

After completing the PayPal payment, please email me:
- A screenshot or receipt of the PayPal transaction
- Your name or PayPal email

Once confirmed, I will personally send you the Commercial License by email.

Contact: sadlyrics121@gmail.com  
PayPal: https://www.paypal.com/paypalme/aymanehaddouba

## 📦 Requirements

- Windows 10 / 11  
- Webcam  
- Python **3.10 or 3.11** (⚠️ Python 3.14 is NOT supported)  
- Internet connection (for installing dependencies)

---

## 🚀 Installation Guide (Step by Step)

### 1️⃣ Install Python (IMPORTANT)

Download Python from the official website:

👉 https://www.python.org/downloads/

✅ **Recommended version:** Python **3.11.x**

During installation:
- ✔️ Check **Add Python to PATH**
- ✔️ Click **Install Now**

Verify installation:
```cmd
python --version
Expected output:

nginx
Copier le code
Python 3.11.x
2️⃣ Open Command Prompt (CMD)
Press Windows key

Type cmd

Press Enter

3️⃣ Install Required Libraries
Run this command:

python -m pip install --upgrade pip
python -m pip install opencv-python mediapipe pyautogui pynput
4️⃣ Verify Installed Libraries
Check OpenCV:

python -c "import cv2; print(cv2.__version__)"
Check MediaPipe:

python -c "import mediapipe as mp; print(mp.__version__)"
If both commands print version numbers → ✅ installation successful.

5️⃣ Run the Program
Navigate to the project directory:

cd path\to\your\project
Run:

python finger_mouse.py
🖥️ Running in VS Code (Optional)
If the program works in CMD but not in VS Code:

Open VS Code
Press Ctrl + Shift + P
Select Python: Select Interpreter
Choose Python 3.11.x
Open a new terminal

Run:
python finger_mouse.py

 🧯 Troubleshooting

❌ ModuleNotFoundError: No module named 'cv2'
Cause:
OpenCV not installed in the active Python environment
Fix:

python -m pip install opencv-python
Verify:

python -c "import cv2"
❌ AttributeError: module 'mediapipe' has no attribute 'solutions'
Possible causes:

Typo in code (mediapiipi, solitions, etc.)

A file named mediapipe.py exists in your project folder

MediaPipe installed in a different Python version

Fix:

python -m pip uninstall mediapipe -y
python -m pip install mediapipe
Make sure no file named:

mediapipe.py
exists in your project directory.

❌ pip is not recognized
Fix:

python -m pip install --upgrade pip
❌ metadata-generation-failed / installation errors
Cause:

Python 3.14 is too new and not supported

✅ Solution:
Use Python 3.10 or 3.11


❌ Camera does not open
Try changing the camera index in the code:

cap = cv2.VideoCapture(1)

⚠️ Notes
Avoid touching the physical mouse while testing
Allow camera access in Windows privacy settings
Good lighting improves hand detection accuracy

🧠 Technologies Used
OpenCV
MediaPipe Hands
PyAutoGUt
Pynput

📜 License
MIT License
Free to use, modify, and distribute.
