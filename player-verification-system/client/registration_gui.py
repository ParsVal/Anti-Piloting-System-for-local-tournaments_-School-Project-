"""
Player Registration Client - GUI Application
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import requests
import uuid

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

from verification import FaceVerification
from utils.device_fingerprint import get_machine_guid, get_device_info

class RegistrationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Registration - Anti-Cheating System")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.face_verifier = FaceVerification()
        self.facial_encoding = None
        self.machine_guid = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2E75B6', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Player Registration System",
            font=('Arial', 20, 'bold'),
            bg='#2E75B6',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main content
        content_frame = tk.Frame(self.root, padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Instructions
        instructions = tk.Label(
            content_frame,
            text="Welcome to the Player Verification System\n\n"
                 "This system uses facial recognition and device fingerprinting\n"
                 "to prevent unauthorized players from competing in tournaments.\n\n"
                 "Your facial data and device ID will be securely stored.",
            font=('Arial', 10),
            justify='left',
            wraplength=500
        )
        instructions.pack(pady=10)
        
        # Consent checkbox
        self.consent_var = tk.BooleanVar()
        consent_check = tk.Checkbutton(
            content_frame,
            text="I consent to the collection and storage of my facial data and device ID",
            variable=self.consent_var,
            font=('Arial', 9),
            wraplength=500
        )
        consent_check.pack(pady=10)
        
        # Separator
        ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Player Information
        info_label = tk.Label(
            content_frame,
            text="Player Information",
            font=('Arial', 12, 'bold')
        )
        info_label.pack(pady=5)
        
        # Name
        name_frame = tk.Frame(content_frame)
        name_frame.pack(fill='x', pady=5)
        tk.Label(name_frame, text="Full Name:", width=15, anchor='w').pack(side='left')
        self.name_entry = tk.Entry(name_frame, width=40)
        self.name_entry.pack(side='left', padx=5)
        
        # Student ID
        student_frame = tk.Frame(content_frame)
        student_frame.pack(fill='x', pady=5)
        tk.Label(student_frame, text="Student ID:", width=15, anchor='w').pack(side='left')
        self.student_entry = tk.Entry(student_frame, width=40)
        self.student_entry.pack(side='left', padx=5)
        
        # Server URL
        server_frame = tk.Frame(content_frame)
        server_frame.pack(fill='x', pady=5)
        tk.Label(server_frame, text="Server URL:", width=15, anchor='w').pack(side='left')
        self.server_entry = tk.Entry(server_frame, width=40)
        self.server_entry.insert(0, "http://localhost:5000")
        self.server_entry.pack(side='left', padx=5)
        
        # Separator
        ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Capture face button
        self.capture_btn = tk.Button(
            content_frame,
            text="1. Capture Facial Data (5 photos)",
            command=self.capture_faces,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            height=2,
            width=40
        )
        self.capture_btn.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            content_frame,
            text="",
            font=('Arial', 9),
            fg='blue'
        )
        self.status_label.pack(pady=5)
        
        # Get device ID button
        self.device_btn = tk.Button(
            content_frame,
            text="2. Get Device Fingerprint",
            command=self.get_device_fingerprint,
            bg='#2196F3',
            fg='white',
            font=('Arial', 11, 'bold'),
            height=2,
            width=40
        )
        self.device_btn.pack(pady=10)
        
        # Device info label
        self.device_label = tk.Label(
            content_frame,
            text="",
            font=('Arial', 9),
            fg='blue'
        )
        self.device_label.pack(pady=5)
        
        # Register button
        self.register_btn = tk.Button(
            content_frame,
            text="3. Complete Registration",
            command=self.register_player,
            bg='#FF9800',
            fg='white',
            font=('Arial', 11, 'bold'),
            height=2,
            width=40,
            state='disabled'
        )
        self.register_btn.pack(pady=10)
    
    def capture_faces(self):
        """Capture facial data"""
        if not self.consent_var.get():
            messagebox.showerror("Error", "Please provide consent before proceeding")
            return
        
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return
        
        self.status_label.config(text="Starting face capture... Follow on-screen instructions")
        self.root.update()
        
        # Capture multiple faces
        encoding = self.face_verifier.capture_multiple_faces(count=5)
        
        if encoding is not None:
            self.facial_encoding = encoding
            self.status_label.config(
                text="✓ Facial data captured successfully!",
                fg='green'
            )
            messagebox.showinfo("Success", "Facial data captured successfully!")
            self.check_registration_ready()
        else:
            self.status_label.config(
                text="✗ Failed to capture facial data",
                fg='red'
            )
            messagebox.showerror("Error", "Failed to capture facial data. Please try again.")
    
    def get_device_fingerprint(self):
        """Get device fingerprint"""
        if not self.consent_var.get():
            messagebox.showerror("Error", "Please provide consent before proceeding")
            return
        
        self.machine_guid = get_machine_guid()
        device_info = get_device_info()
        
        self.device_label.config(
            text=f"✓ Device ID: {self.machine_guid[:20]}...\n"
                 f"Platform: {device_info['platform']} {device_info['platform_release']}",
            fg='green'
        )
        
        messagebox.showinfo(
            "Device Fingerprint",
            f"Device ID obtained successfully!\n\n"
            f"Platform: {device_info['platform']}\n"
            f"Device ID: {self.machine_guid}"
        )
        
        self.check_registration_ready()
    
    def check_registration_ready(self):
        """Check if all requirements met for registration"""
        if self.facial_encoding is not None and self.machine_guid is not None:
            self.register_btn.config(state='normal')
    
    def register_player(self):
        """Register player with server"""
        name = self.name_entry.get().strip()
        student_id = self.student_entry.get().strip()
        server_url = self.server_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return
        
        if not self.facial_encoding is not None:
            messagebox.showerror("Error", "Please capture facial data first")
            return
        
        if not self.machine_guid:
            messagebox.showerror("Error", "Please get device fingerprint first")
            return
        
        # Generate player ID
        player_id = f"PLAYER_{uuid.uuid4().hex[:8].upper()}"
        
        # Prepare data
        data = {
            'player_id': player_id,
            'name': name,
            'student_id': student_id,
            'facial_encoding': self.facial_encoding.tolist(),
            'machine_guid': self.machine_guid
        }
        
        try:
            # Send to server
            response = requests.post(
                f"{server_url}/api/register",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                messagebox.showinfo(
                    "Registration Successful",
                    f"Registration completed successfully!\n\n"
                    f"Player ID: {player_id}\n"
                    f"Name: {name}\n\n"
                    f"Please save your Player ID for verification."
                )
                
                # Save player ID to file
                with open('player_credentials.txt', 'w') as f:
                    f.write(f"Player ID: {player_id}\n")
                    f.write(f"Name: {name}\n")
                    f.write(f"Student ID: {student_id}\n")
                    f.write(f"Registered: {uuid.uuid1().time}\n")
                
                self.root.destroy()
            else:
                error = response.json().get('error', 'Unknown error')
                messagebox.showerror("Registration Failed", f"Error: {error}")
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror(
                "Connection Error",
                f"Failed to connect to server.\n\n"
                f"Please check:\n"
                f"1. Server is running\n"
                f"2. Server URL is correct\n\n"
                f"Error: {str(e)}"
            )

def main():
    root = tk.Tk()
    app = RegistrationGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
