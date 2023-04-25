import re
import tkinter as tk

class EmailHeaderAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Header Analyzer")
        self.root.resizable(False, False)
        self.root.geometry("500x800")

        # Input text box
        input_label = tk.Label(self.root, text="Input:")
        input_label.pack(side=tk.TOP, padx=10, pady=5, anchor='w')
        self.header_text = tk.Text(self.root, height=10, width=100, wrap="word")
        self.header_text.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Output text box
        output_label = tk.Label(self.root, text="Output:")
        output_label.pack(side=tk.TOP, padx=10, pady=5, anchor='w')
        self.result_text = tk.Text(self.root, height=10, width=100, wrap="word", state="disabled")
        self.result_text.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        self.run_button = tk.Button(button_frame, text="Run", command=self.run)
        self.run_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.copy_button = tk.Button(button_frame, text="Copy", command=self.copy)
        self.copy_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Center the buttons in the button frame
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(4, weight=1)

        
    def run(self):
        header_text = self.header_text.get("1.0", "end-1c")

        # Parse the header data using regular expressions
        from_regex = re.search(r"From: (.+)", header_text)
        to_regex = re.search(r"To: (.+)", header_text)
        reply_to_regex = re.search(r"Reply-To: (.+)", header_text)
        subject_regex = re.search(r"Subject: (.+)", header_text)
        date_regex = re.search(r"Date: (.+)", header_text)
        message_id_regex = re.search(r"Message-ID: (.+)", header_text)
        mime_version_regex = re.search(r"MIME-Version: (.+)", header_text)
        content_type_regex = re.search(r"Content-Type: (.+)", header_text)
        spf_regex = re.search(r"X-Proofpoint-SPF-Result: (.+)", header_text)
        spam_details_regex = re.search(r"X-Proofpoint-Spam-Details: (.+)", header_text)

        # Output the header data
        result = f"From: {from_regex.group(1) if from_regex else 'N/A'}\nTo: {to_regex.group(1) if to_regex else 'N/A'}\nReply-To: {reply_to_regex.group(1) if reply_to_regex else 'N/A'}\nSubject: {subject_regex.group(1) if subject_regex else 'N/A'}\nDate: {date_regex.group(1) if date_regex else 'N/A'}\nMessage-ID: {message_id_regex.group(1) if message_id_regex else 'N/A'}\nMIME-Version: {mime_version_regex.group(1) if mime_version_regex else 'N/A'}\nContent-Type: {content_type_regex.group(1) if content_type_regex else 'N/A'}\nSPF Result: {spf_regex.group(1) if spf_regex else 'N/A'}\nSpam Details: {spam_details_regex.group(1) if spam_details_regex else 'N/A'}"
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result)
        self.result_text.configure(state="disabled")
        
    def clear(self):
        self.header_text.delete("1.0", "end")
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.configure(state="disabled")

    def copy(self):
        output = self.result_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(output)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailHeaderAnalyzer(root)
    root.mainloop()

