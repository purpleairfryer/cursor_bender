"""
AI Hand-Controlled Cursor for Windows
Controls the Windows mouse cursor using right hand gestures detected via webcam.

Features:
- Cursor Movement: Index finger controls mouse cursor with smooth movement
- Left Click: Pinch thumb and index finger together
- Auto-Scrolling: Raise index and middle fingers to continuously scroll down
- Browser Back: While scrolling, swipe right to trigger Alt + Left Arrow

Installation:
    pip install -r requirements.txt
    or
    pip install opencv-python mediapipe pyautogui numpy
    
Usage:
    python hand_cursor_control.py
"""

import cv2  # type: ignore
import mediapipe as mp  # type: ignore
import pyautogui  # type: ignore
import numpy as np  # type: ignore
import time

# ============================================================================
# CONFIGURATION PARAMETERS
# ============================================================================

# Pinch detection threshold (normalized distance between thumb and index tip)
PINCH_THRESHOLD = 0.04

# Scroll speed (scroll units per scroll action - higher = faster)
SCROLL_SPEED = 10

# Swipe gesture threshold (normalized distance for horizontal swipe detection)
SWIPE_THRESHOLD = 0.15  # How far right you need to swipe (0.0 to 1.0)

# Debounce times (in seconds) to prevent multiple rapid actions
CLICK_DEBOUNCE_TIME = 0.5
SCROLL_INTERVAL = 0.05  # Time between scroll actions (seconds) - lower = faster scrolling
SWIPE_DEBOUNCE_TIME = 0.5  # Time between swipe gestures (seconds)

# Smoothing factor for cursor movement (0.0 to 1.0, higher = smoother)
CURSOR_SMOOTHING = 0.85

# Minimum movement threshold (pixels) to prevent jittery micro-movements
MIN_MOVEMENT_THRESHOLD = 2

# ============================================================================
# MEDIAPIPE INITIALIZATION
# ============================================================================

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize MediaPipe Hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Only detect one hand (right hand)
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_finger_up(landmarks, finger_tip_idx, finger_pip_idx):
    """
    Check if a finger is extended (up).
    
    Args:
        landmarks: List of hand landmarks
        finger_tip_idx: Index of the fingertip landmark
        finger_pip_idx: Index of the PIP (Proximal Interphalangeal) joint
    
    Returns:
        True if finger is up, False otherwise
    """
    finger_tip = landmarks[finger_tip_idx]
    finger_pip = landmarks[finger_pip_idx]
    
    # For fingers, if the tip is above the PIP joint, the finger is up
    # Note: Y-coordinates increase downward in image coordinates
    return finger_tip.y < finger_pip.y


def is_pinch(landmarks, thumb_tip_idx=4, index_tip_idx=8):
    """
    Check if thumb and index finger are pinched together.
    
    Args:
        landmarks: List of hand landmarks
        thumb_tip_idx: Index of thumb tip (default: 4)
        index_tip_idx: Index of index finger tip (default: 8)
    
    Returns:
        True if thumb and index are pinched, False otherwise
    """
    thumb_tip = landmarks[thumb_tip_idx]
    index_tip = landmarks[index_tip_idx]
    
    # Calculate Euclidean distance between thumb and index tips
    distance = np.sqrt(
        (thumb_tip.x - index_tip.x) ** 2 + 
        (thumb_tip.y - index_tip.y) ** 2
    )
    
    return distance < PINCH_THRESHOLD


def is_scroll_gesture(landmarks):
    """
    Check if index and middle fingers are both extended (scroll gesture).
    
    Args:
        landmarks: List of hand landmarks
    
    Returns:
        True if both index and middle fingers are up, False otherwise
    """
    index_up = is_finger_up(landmarks, 8, 6)  # Index tip: 8, Index PIP: 6
    middle_up = is_finger_up(landmarks, 12, 10)  # Middle tip: 12, Middle PIP: 10
    
    return index_up and middle_up


def map_to_screen(frame_width, frame_height, landmark_x, landmark_y):
    """
    Map normalized landmark coordinates to screen coordinates.
    
    Args:
        frame_width: Width of the webcam frame
        frame_height: Height of the webcam frame
        landmark_x: Normalized x coordinate (0.0 to 1.0)
        landmark_y: Normalized y coordinate (0.0 to 1.0)
    
    Returns:
        Tuple of (screen_x, screen_y) pixel coordinates
    """
    screen_width, screen_height = pyautogui.size()
    
    # Map normalized coordinates to screen coordinates
    screen_x = int(landmark_x * screen_width)
    screen_y = int(landmark_y * screen_height)
    
    return screen_x, screen_y


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    # Get screen resolution
    screen_width, screen_height = pyautogui.size()
    print(f"Screen resolution: {screen_width}x{screen_height}")
    
    # State management variables
    last_click_time = 0
    last_scroll_y = None
    last_scroll_time = 0
    last_cursor_pos = None
    last_swipe_time = 0
    scroll_initial_x = None  # Track initial finger position when scroll gesture starts
    
    # Disable PyAutoGUI failsafe (optional, can be enabled for safety)
    pyautogui.FAILSAFE = False
    
    print("Hand Cursor Control started. Press 'q' to quit.")
    print("Gestures:")
    print("  - Index finger up: Move cursor")
    print("  - Index + Thumb pinch: Left-click")
    print("  - Index + Middle fingers up: Scroll")
    
    try:
        while True:
            # Read frame from webcam
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from webcam.")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB (MediaPipe requires RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe
            results = hands.process(rgb_frame)
            
            # Draw hand landmarks on frame
            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(
                    results.multi_hand_landmarks, 
                    results.multi_handedness
                ):
                    # Only process right hand
                    if handedness.classification[0].label == "Right":
                        # Draw landmarks and connections
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style()
                        )
                        
                        # Extract landmarks
                        landmarks = hand_landmarks.landmark
                        
                        # Get key landmark positions
                        thumb_tip = landmarks[4]
                        index_tip = landmarks[8]
                        index_pip = landmarks[6]
                        middle_tip = landmarks[12]
                        middle_pip = landmarks[10]
                        
                        # Check finger states
                        index_up = is_finger_up(landmarks, 8, 6)
                        middle_up = is_finger_up(landmarks, 12, 10)
                        pinch = is_pinch(landmarks)
                        
                        # Visual feedback: Draw circle on index fingertip
                        frame_height, frame_width = frame.shape[:2]
                        index_x = int(index_tip.x * frame_width)
                        index_y = int(index_tip.y * frame_height)
                        cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), 2)
                        
                        # Gesture: Scroll (Index + Middle fingers up)
                        if is_scroll_gesture(landmarks):
                            # Initialize scroll tracking position if not set
                            if scroll_initial_x is None:
                                scroll_initial_x = index_tip.x
                            
                            # Show "Scrolling active" message when gesture is detected
                            cv2.putText(
                                frame, 
                                "Scrolling active", 
                                (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1, 
                                (0, 255, 255), 
                                2
                            )
                            
                            current_time = time.time()
                            
                            # Check for horizontal swipe to the right (browser back gesture)
                            horizontal_delta = index_tip.x - scroll_initial_x
                            
                            if horizontal_delta > SWIPE_THRESHOLD:
                                # Swipe right detected - trigger browser back (Alt + Left Arrow)
                                if current_time - last_swipe_time > SWIPE_DEBOUNCE_TIME:
                                    pyautogui.hotkey('alt', 'left')
                                    last_swipe_time = current_time
                                    scroll_initial_x = index_tip.x  # Reset initial position
                                    
                                    # Visual feedback
                                    cv2.putText(
                                        frame, 
                                        "BROWSER BACK", 
                                        (10, 70), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 
                                        1, 
                                        (255, 255, 0), 
                                        2
                                    )
                            else:
                                # Continuously scroll down while gesture is active (no horizontal swipe)
                                if current_time - last_scroll_time > SCROLL_INTERVAL:
                                    pyautogui.scroll(-SCROLL_SPEED)  # Negative for scrolling down
                                    last_scroll_time = current_time
                        
                        # Gesture: Click (Pinch)
                        elif pinch and index_up:
                            current_time = time.time()
                            
                            if current_time - last_click_time > CLICK_DEBOUNCE_TIME:
                                pyautogui.click()
                                last_click_time = current_time
                                
                                # Visual feedback
                                cv2.putText(
                                    frame, 
                                    "CLICK", 
                                    (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, 
                                    (0, 0, 255), 
                                    2
                                )
                            
                            last_scroll_y = None  # Reset scroll tracking
                            scroll_initial_x = None  # Reset swipe tracking
                        
                        # Gesture: Cursor Movement (Index finger up only)
                        elif index_up and not middle_up:
                            scroll_initial_x = None  # Reset swipe tracking
                            # Map index fingertip to screen coordinates
                            screen_x, screen_y = map_to_screen(
                                frame_width, 
                                frame_height, 
                                index_tip.x, 
                                index_tip.y
                            )
                            
                            # Smooth cursor movement with enhanced smoothing
                            if last_cursor_pos is not None:
                                # Calculate movement delta
                                delta_x = screen_x - last_cursor_pos[0]
                                delta_y = screen_y - last_cursor_pos[1]
                                
                                # Only move if movement exceeds threshold (reduces jitter)
                                if abs(delta_x) > MIN_MOVEMENT_THRESHOLD or abs(delta_y) > MIN_MOVEMENT_THRESHOLD:
                                    # Apply exponential smoothing (higher smoothing factor = smoother)
                                    smoothed_x = int(
                                        CURSOR_SMOOTHING * last_cursor_pos[0] + 
                                        (1 - CURSOR_SMOOTHING) * screen_x
                                    )
                                    smoothed_y = int(
                                        CURSOR_SMOOTHING * last_cursor_pos[1] + 
                                        (1 - CURSOR_SMOOTHING) * screen_y
                                    )
                                    pyautogui.moveTo(smoothed_x, smoothed_y)
                                    last_cursor_pos = (smoothed_x, smoothed_y)
                                # If movement is too small, keep last position (prevents micro-movements)
                            else:
                                pyautogui.moveTo(screen_x, screen_y)
                                last_cursor_pos = (screen_x, screen_y)
                            
                            # Visual feedback
                            cv2.putText(
                                frame, 
                                "CURSOR ACTIVE", 
                                (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1, 
                                (0, 255, 0), 
                                2
                            )
                            
                            last_scroll_y = None  # Reset scroll tracking
                        
                        else:
                            # No active gesture - reset scroll tracking
                            last_scroll_y = None
                            last_cursor_pos = None
                            scroll_initial_x = None  # Reset swipe tracking
                    else:
                        # Left hand detected, ignore
                        cv2.putText(
                            frame, 
                            "Please use RIGHT hand", 
                            (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1, 
                            (0, 0, 255), 
                            2
                        )
            else:
                # No hand detected
                last_scroll_y = None
                last_cursor_pos = None
            
            # Display frame
            cv2.imshow('Hand Cursor Control', frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        print("Application closed.")


if __name__ == "__main__":
    main()

