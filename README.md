# AI Hand-Controlled Cursor for Windows

A Python desktop application that allows you to control your Windows mouse cursor using right hand gestures detected through a webcam feed. Built with MediaPipe, OpenCV, and PyAutoGUI.

## Features

- **Cursor Movement**: Extend your right index finger to activate cursor control. Moving your finger moves the mouse cursor with smooth, jitter-free movement.
- **Left Click**: Pinch your thumb and index finger together to perform a left-click.
- **Auto-Scrolling**: Extend both your index and middle fingers to automatically scroll down continuously. Lower your fingers to stop scrolling.
- **Browser Back Gesture**: While both index and middle fingers are up, swipe your hand to the right to trigger Alt + Left Arrow (browser back).

## Requirements

- Python 3.8-3.12 (Python 3.11 or 3.12 recommended)
- Windows operating system
- Webcam
- Good lighting for optimal hand detection

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/purpleairfryer/cursor_bender.git
cd cursor_bender
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows PowerShell
# OR
venv\Scripts\activate.bat  # On Windows CMD
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python hand_cursor_control.py
```

2. A window will open showing your webcam feed with hand landmark visualization.

3. Use the following gestures:
   - **Index finger up**: Move the cursor
   - **Index + Thumb pinch**: Left-click
   - **Index + Middle fingers up**: Auto-scroll down (stops when fingers are lowered)
   - **Index + Middle fingers up + Swipe right**: Browser back (Alt + Left Arrow)

4. Press `q` in the webcam window to quit the application.

## Gesture Details

### Cursor Movement
- Raise only your **index finger** (right hand)
- The cursor moves smoothly with your finger position
- Enhanced smoothing prevents jittery movements
- Movement threshold filters out micro-movements

### Click Gesture
- **Pinch** your thumb and index finger together
- Triggers a left-click at the current cursor position
- Debounce prevents multiple rapid clicks

### Scrolling
- Raise both **index and middle fingers** together
- Automatically scrolls down continuously while gesture is active
- Scrolling stops when you lower your fingers
- Configurable scroll speed

### Browser Back Gesture
- While both **index and middle fingers** are up (scroll gesture active)
- Move your hand to the **right** to trigger browser back
- Works in Chrome and other browsers that support Alt + Left Arrow navigation

## Configuration

You can adjust the following parameters at the top of `hand_cursor_control.py`:

**Gesture Detection:**
- `PINCH_THRESHOLD`: Distance threshold for pinch detection (default: 0.04)
- `SWIPE_THRESHOLD`: How far right you need to swipe for browser back (default: 0.15)
  - Lower (0.10) = more sensitive, easier to trigger
  - Higher (0.20) = requires more movement, less accidental triggers

**Performance:**
- `SCROLL_SPEED`: Scroll units per scroll action (default: 10)
  - Higher = faster scrolling
- `SCROLL_INTERVAL`: Time between scroll actions in seconds (default: 0.05)
  - Lower = more frequent scrolling
- `CLICK_DEBOUNCE_TIME`: Minimum time between clicks in seconds (default: 0.5)
- `SWIPE_DEBOUNCE_TIME`: Minimum time between swipe gestures in seconds (default: 0.5)

**Cursor Smoothing:**
- `CURSOR_SMOOTHING`: Smoothing factor (0.0 to 1.0, default: 0.85)
  - Higher = smoother but more lag
  - Lower = more responsive but potentially jittery
- `MIN_MOVEMENT_THRESHOLD`: Minimum pixels of movement to trigger cursor update (default: 2)
  - Prevents jittery micro-movements

## Troubleshooting

**Webcam Issues:**
- Ensure your webcam is working and not being used by another application
- Try closing other applications that might be using the webcam

**Hand Detection:**
- Make sure you have good lighting for better hand detection
- Keep your right hand clearly visible to the camera
- The application only detects the right hand

**Gesture Not Working:**
- Adjust the thresholds in the configuration section if gestures are not being detected correctly
- Try increasing `PINCH_THRESHOLD` if clicks are too sensitive
- Try decreasing `SWIPE_THRESHOLD` if browser back gesture is hard to trigger

**Python Version:**
- Ensure you're using Python 3.8-3.12 (MediaPipe compatibility)
- If you have Python 3.14+, you may need to install Python 3.11 or 3.12

**Virtual Environment:**
- If activation fails, try: `powershell -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1`
- Or use direct Python: `.\venv\Scripts\python.exe hand_cursor_control.py`

## Technical Details

- **MediaPipe**: Hand landmark detection and tracking
- **OpenCV**: Webcam capture and video processing
- **PyAutoGUI**: Mouse cursor control and keyboard shortcuts
- **NumPy**: Numerical operations for gesture calculations

## License

This project is open source and available for personal and educational use.

