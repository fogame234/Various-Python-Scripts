import tkinter as tk
import requests
import base64
import tkinter.messagebox as msg


api_key = '<API-KEY>'

def analyze_url():
    # Get the API key and the URL to scan from the GUI inputs
    url = url_input.get()

    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    # Set the URL for the VirusTotal API and the headers for the request
    url_api = "https://www.virustotal.com/api/v3/urls/" + url_id
    headers = {"x-apikey": api_key}

    # Send the request to the VirusTotal API
    response = requests.get(url_api, headers=headers)

    # Parse the response as JSON and check if the URL was found
    json_response = response.json()
    if json_response.get("error"):
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: " + json_response.get("error").get("message"))
        output_text.config(state=tk.DISABLED)
        return

    # Get the results from the response
    attributes = json_response.get("data").get("attributes")
    last_analysis_stats = attributes.get("last_analysis_stats")
    last_analysis_results = attributes.get("last_analysis_results")

    # Check if the results are clean
    detections = int(last_analysis_stats['malicious'])
    if detections == 0:
        results_string = f"VirusTotal Check:\n\nURL: {url}\nDetections: {last_analysis_stats['malicious']}/{last_analysis_stats['harmless']}\nDomain is considered not malicious\n\n"
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.config(state=tk.DISABLED)
    else:
        # Format the results as a string
        results_string = f"VirusTotal Check:\n\nURL: {url}\nDetections: {last_analysis_stats['malicious']}/{last_analysis_stats['harmless']}\nResults by scanner:\n\n"
        for scanner, result in last_analysis_results.items():
            if 'malicious' in result.get("category"):
                results_string += f"{scanner}: {result['result']}\n"

    # Format the results as a string and insert it into the output text box
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, results_string)
    output_text.config(state=tk.DISABLED)

def analyze_ip():
    # Get the API key and the IP address to scan from the GUI inputs
    ip = ip_input.get()

    # Send the request to the VirusTotal API
    url_api = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}?include=whois"
    headers = {"x-apikey": api_key}
    response = requests.get(url_api, headers=headers)

    # Parse the response as JSON and check if the IP address was found
    json_response = response.json()
    if json_response.get("error"):
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: " + json_response.get("error").get("message"))
        output_text.config(state=tk.DISABLED)
        return

    # Get the results from the response
    attributes = json_response.get("data").get("attributes")
    last_analysis_stats = attributes.get("last_analysis_stats")
    last_analysis_results = attributes.get("last_analysis_results")
    whois = attributes.get("whois")

    # Get the domain from the Whois data
    domain = "Unknown"
    if whois:
        for record in whois:
            if "domain" in record:
                domain = record["domain"]
                break

    # Check if the results are clean
    detections = int(last_analysis_stats['malicious'])
    if detections == 0:
        results_string = f"VirusTotal Check:\n\nIP address: {ip}\nDomain: {domain}\nDetections: {detections}/{last_analysis_stats['harmless']}\n\n"
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, results_string)
        output_text.insert(tk.END, f"{ip} is clean.")
        output_text.config(state=tk.DISABLED)
    else:
        # Format the results as a string
        results_string = f"VirusTotal Check:\n\nIP address: {ip}\nDomain: {domain}\nDetections: {detections}/{last_analysis_stats['harmless']}\nResults by scanner:\n\n"
        for scanner, result in last_analysis_results.items():
            if 'malicious' in result.get("category"):
                results_string += f"{scanner}: {result['result']}\n"
        
        # Insert results into the output text box
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, results_string)
        output_text.config(state=tk.DISABLED)




def copy_output():
    output = output_text.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(output)

def clear_inputs():
    url_input.delete(0, tk.END)
    ip_input.delete(0, tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

# Create the GUI
root = tk.Tk()
root.title("VirusTotal Scanner")

# Create the URL input label and text box
url_label = tk.Label(root, text="URL:")
url_label.pack(side=tk.TOP, padx=10, pady=5)
url_input = tk.Entry(root, width=50)
url_input.pack(side=tk.TOP, padx=10, pady=5)

# Create the IP input label and text box
ip_label = tk.Label(root, text="IP Address:")
ip_label.pack(side=tk.TOP, padx=10, pady=5)
ip_input = tk.Entry(root, width=50)
ip_input.pack(side=tk.TOP, padx=10, pady=5)

# Create the output label
output_label = tk.Label(root, text="Output:")
output_label.pack(side=tk.TOP, padx=10, pady=5)

# Create the output text box and make it read-only
output_text = tk.Text(root, height=15, width=80, state=tk.DISABLED)
output_text.pack(side=tk.TOP, padx=10, pady=5)

# Create the Analyze and Copy buttons below the output text box
button_frame = tk.Frame(root)
analyze_url_button = tk.Button(button_frame, text="Analyze URL", command=analyze_url)
analyze_url_button.pack(side=tk.LEFT, padx=10, pady=5)
analyze_ip_button = tk.Button(button_frame, text="Analyze IP", command=analyze_ip)
analyze_ip_button.pack(side=tk.LEFT, padx=10, pady=5)
copy_button = tk.Button(button_frame, text="Copy Output", command=copy_output)
copy_button.pack(side=tk.LEFT, padx=10, pady=5)
clear_button = tk.Button(button_frame, text="Clear", command=clear_inputs)
clear_button.pack(side=tk.LEFT, padx=10, pady=5)
button_frame.pack(side=tk.TOP, padx=10, pady=5)

# Start the GUI
root.mainloop()


# Need to add whois function to gather domain name or organization 