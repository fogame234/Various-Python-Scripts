import requests
import json
import tkinter as tk
import tkinter.scrolledtext as st

def is_valid_email(email, api_key):
    """
    Validate if an email is valid using the hunter.io API.
    Returns the full JSON response from the API.
    """
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to verify email: " + response.text)

def verify_email():
    email = email_input.get()
    result = is_valid_email(email, api_key)
    if 'data' in result and 'result' in result['data']:
        del result['data']['result']
    if 'data' in result and '_deprecation_notice' in result['data']:
        del result['data']['_deprecation_notice']

    
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, json.dumps(result, indent=4))
    output_box.config(state=tk.DISABLED)

def copy_output():
    output_text = output_box.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(output_text)

def clear_fields():
    email_input.delete(0, tk.END)
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.config(state=tk.DISABLED)

# Set up the GUI
root = tk.Tk()
root.title("Email Verification")
root.geometry("600x500")

# Create the email input field and label
email_frame = tk.Frame(root)
email_frame.pack(pady=5)
email_label = tk.Label(email_frame, text="Email Verification")
email_label.pack(side=tk.LEFT, padx=5)
email_input = tk.Entry(email_frame, width=50)
email_input.pack(side=tk.LEFT)

# Create the output box and label
output_label = tk.Label(root, text="Output", anchor=tk.W, padx=5)
output_label.pack(pady=5)
output_box = st.ScrolledText(root, wrap=tk.WORD, height=25)
output_box.pack(padx=10)
output_box.config(state=tk.DISABLED)

# Create the button frame and buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=5)
run_button = tk.Button(button_frame, text="Run", command=verify_email, padx=5)
run_button.pack(side=tk.LEFT)
copy_button = tk.Button(button_frame, text="Copy", command=copy_output, padx=5)
copy_button.pack(side=tk.LEFT)
clear_button = tk.Button(button_frame, text="Clear", command=clear_fields, padx=5)
clear_button.pack(side=tk.LEFT)

# Set the API key
api_key = '<API KEY>'

# Run the GUI loop
root.mainloop()
