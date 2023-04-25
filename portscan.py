import socket
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as tkst
import pyperclip

class PortScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title('Port Scanner')

        # Create IP address label and text box
        ip_label = tk.Label(master, text='IP Address:')
        ip_label.grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = tk.Entry(master, width=50)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create output label and text box
        output_label = tk.Label(master, text='Open Ports:')
        output_label.grid(row=1, column=0, padx=5, pady=5)
        self.output_text = tkst.ScrolledText(master, height=1, width=50)
        self.output_text.grid(row=1, column=1, padx=5, pady=5)
        self.output_text.config(state=tk.DISABLED)

        # Create button frame
        button_frame = tk.Frame(master)
        button_frame.grid(row=2, column=0, sticky='w', padx=5, pady=5)

        # Create run button
        run_button = tk.Button(button_frame, text='Run', command=self.run_scan)
        run_button.pack(side='left', padx=5, pady=5)

        # Create copy button
        copy_button = tk.Button(button_frame, text='Copy', command=self.copy_to_clipboard)
        copy_button.pack(side='left', padx=5, pady=5)

        # Create clear button
        clear_button = tk.Button(button_frame, text='Clear', command=self.clear_output)
        clear_button.pack(side='left', padx=5, pady=5)

    def scan_ports(self, host):
        open_ports = []
        for port in range(1, 65536):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except socket.error:
                pass
        return open_ports

    def run_scan(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        ip_address = self.ip_entry.get()
        try:
            open_ports = self.scan_ports(ip_address)
            if open_ports:
                self.output_text.config(height=len(open_ports), width=50)
                self.output_text.insert(tk.END, f'Open ports on {ip_address}:\n')
                for port in open_ports:
                    self.output_text.insert(tk.END, f'{port}\n')
            else:
                self.output_text.insert(tk.END, f'No open ports found on {ip_address}\n')
        except socket.gaierror:
            self.output_text.insert(tk.END, f'Unable to resolve hostname: {ip_address}\n')

        # Resize the output text box to match the size of the input text box
        self.output_text.config(height=1)

        self.output_text.config(state=tk.DISABLED)

    def copy_to_clipboard(self):
        ip_address = self.ip_entry.get()
        output = self.output_text.get('1.0', tk.END)
        text_to_copy = f'IP Address: {ip_address}\n\n{output}'
        pyperclip.copy(text_to_copy)

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(height=1)
        self.output_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    gui = PortScannerGUI(root)
    root.mainloop()
