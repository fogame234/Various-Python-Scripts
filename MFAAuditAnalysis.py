import csv
import re
import tkinter as tk
from tkinter import filedialog, scrolledtext
import datetime
import os

class MFAReport:
    def __init__(self, file_path):
        self.file_path = file_path

    def run(self, output):
    # Filter strings
        displayname_strings = [    
                    'hr', 'mfa', 'help', 'mailbox', 'ipam', 'notification', 'abca', 'vendor', 'savers', 'ldap',    
                    'service', 'team', 'office', 'conf', 'ops', 'project', 'procurement', 'pto', 'pts', 'qa',    
                    'recylcing', 'sapl', 'sccm', 'section', 'fife', 'schedule', 'inbox', 'sms', 'sourcing', 'sql',    
                    'srv', 'rapid', 'sharepoint', 'solarwinds', 'premises', 'tdx', 'system', 'tx', 'uat', 'support',    
                    'unique', 'value village', 'vcom', 'training', 'webmaster', 'webs', '2a', 'gd', 'cpt', 'customer',    
                    'check', 'ddf', 'dev', 'donation', 'dra', 'driver', 'email', 'enterprise', 'entrevue', 'epoc',    
                    'vault', 'exchange', 'meeting', 'jobvite', 'launch', 'intune', 'inventory', 'mkg', 'mom', 'reply',    
                    'o365', 'payroll', 'phish', 'pie', 'estate', 'reactions', 'rightfax', 'root', 'rsg', 'raa',    
                    'security', 'server', 'signup', 'splunk', 'stories', 'store', 'tc', 'test', 'traxx', 'leave',    
                    'village', 'client', 'welcome', 'monitor', 'outreach', 'fundrive', 'svc_', 'apogee', 'calendar', 'ameans',    
                    'stage', 'charity', 'covid', 'covid', 'crm', 'communautaire', 'automation', 'card', 'lead', 'travel',    
                    'ims', 'tkt', 'cpc', 'influence', 'fax', 'frx', 'entry', 'renton', 'iddc', 'boise',    
                    'meridian', 'bellevue', 'SSC', 'urgent', 'greendrop', 'i3', 'accounts', 'aus', 'canada', 'australia',    
                    'engineering', 'acsad', 'abm', 'safety', 'impact','cic', 'adm', 'report', 'search', 'slc',    
                    'orion', 'Intelecom', 'teletrol', 'valvan','Handbook']
        user_strings = ['apogeeretail', 'onmicrosoft', 'fundrive', 'svc_']
        okta_strings = ['bjacoby', 'rtanner', 'MWeiks', 'dvandyke']
        aliases_strings = ['outreach']

        mfa_count = 0
        disabled_list = []
        total_count = 0
        storerelated_count = 0

        # Process file
        with open(self.file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_count += 1
                if row['MFAState'].lower() in ['enabled', 'enforced']:
                    mfa_count += 1
                elif row['MFAState'].lower() == 'disabled':
                    upn = row['UserPrincipalName']
                    if ('$' in upn 
                        or any(x.lower() in upn.lower() for x in user_strings + okta_strings)
                        or any(x.lower() in row['Aliases'].lower() for x in aliases_strings)
                        or any(x.lower() in row['DisplayName'].lower() for x in displayname_strings)):
                        continue  # Skip this row
                    if len(re.findall(r'\d', upn)) == 4:
                        if 'STR' in upn or 'MGR' in upn:
                            storerelated_count += 1
                        continue  # Skip this row
                    disabled_list.append(row['DisplayName'])

        # Filter disabled_list
        disabled_list = [name for name in disabled_list if not any(c.isdigit() for c in name)]

        disabled_count = len(disabled_list)

        total_count_all = storerelated_count + mfa_count + disabled_count

        # Print results to output
        output.insert('end', f"MFA report statistics:\n")
        output.insert('end', f"Total number of relevant accounts: {total_count_all}\n")
        output.insert('end', f"Total number of STR/MGR accounts with disabled MFA states: {storerelated_count}\n")
        output.insert('end', f"Total number of user accounts with enabled MFA states: {mfa_count}\n")
        output.insert('end', f"Total number of user accounts with disabled MFA states: {disabled_count}\n\n")
        output.insert('end', "Disabled user accounts:\n")
        for name in disabled_list:
            output.insert('end', f"{name}\n")
        output.insert('end', f"\n")


class EmailCounter:
    def __init__(self, filename):
        self.filename = filename

    def run(self, output):
        try:
            # Read the CSV file
            rows = self.read_csv_file(self.filename)

            # Extract the email counts from the CSV file
            email_counts = self.extract_email_counts(rows)

            # Print the email counts
            output.insert('end', f"Enable/Disable statistics:\n")
            for email_address in email_counts.keys():
                enable_count_for_email = email_counts[email_address]['enable']
                disable_count_for_email = email_counts[email_address]['disable']
                output.insert('end', f"{email_address}: {enable_count_for_email} enables, {disable_count_for_email} disables\n")

        except Exception as e:
            output.insert('end', f"An error occurred: {e}\n")

    @staticmethod
    def read_csv_file(filename):
        # Open the CSV file for reading
        with open(filename, newline='') as csvfile:
            # Create a CSV reader object
            reader = csv.DictReader(csvfile)

            # Make the column headers case insensitive
            reader.fieldnames = [header.lower() for header in reader.fieldnames]

            # Loop through each row in the CSV file
            for row in reader:
                yield row

    @staticmethod
    def extract_email_counts(rows):
        # Define counters for enable and disable operations
        email_counts = {}

        # Loop through each row in the CSV file
        for row in rows:
            # Get the value of the 'initiatedby' and 'operationname' columns for the current row
            initiated_by = row['initiatedby']
            operation_name = row['operationname']

            # Use a regular expression to extract the email address from the 'initiatedby' value
            match = re.search(r'\b([A-Za-z0-9._%+-]+)@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', initiated_by)
            if match:
                email_address = match.group(1)

                # Modify operation_name if it is 'Enable Strong Authentication' or 'Disable Strong Authentication'
                if operation_name == 'Enable Strong Authentication':
                    operation_name = 'Enable'
                elif operation_name == 'Disable Strong Authentication':
                    operation_name = 'Disable'

                # Increment the appropriate counter based on the operation name
                if email_address not in email_counts:
                    email_counts[email_address] = {'enable': 0, 'disable': 0}

                email_counts[email_address][operation_name.lower()] += 1

        return email_counts

class MFAReportAndEmailCounterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MFA Report and Email Counter")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create button frame for file selection
        select_button_frame = tk.Frame(self.frame)
        select_button_frame.pack(side=tk.TOP, padx=5, pady=5)

        # Create select file buttons
        self.mfa_select_file_button = tk.Button(select_button_frame, text="Select MFA Report", command=self.select_mfa_file)
        self.email_select_file_button = tk.Button(select_button_frame, text="Select Email Log", command=self.select_email_file)
        self.mfa_select_file_button.pack(side=tk.LEFT, padx=5)
        self.email_select_file_button.pack(side=tk.LEFT, padx=5)

        # Create button frame for copy and close buttons
        button_frame = tk.Frame(self.frame)
        button_frame.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create copy button
        self.copy_button = tk.Button(button_frame, text="Copy Output", command=self.copy_output)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        # Create close button
        self.close_button = tk.Button(button_frame, text="Close", command=self.close_window)
        self.close_button.pack(side=tk.LEFT, padx=5)

        # Create output text box
        self.output = scrolledtext.ScrolledText(self.frame, width=80, height=20)
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.set_current_date()

        self.root.mainloop()

    def set_current_date(self):
        # Get the current date and time
        current_date = datetime.datetime.now()

        # Format the current date and time as a string
        current_date_str = current_date.strftime("Report generated on %m/%d/%Y at %I:%M %p\n\n")

        # Insert the current date and time at the beginning of the output textbox
        self.output.insert('1.0', current_date_str)

    def select_mfa_file(self):
        self.mfa_filename = filedialog.askopenfilename()
        if self.mfa_filename:
            report = MFAReport(self.mfa_filename)
            report.run(self.output)

    def select_email_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            counter = EmailCounter(filename)
            counter.run(self.output)

    def copy_output(self):
        # Copy the contents of the output text box to the clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output.get('1.0', tk.END))

    def close_window(self):
        # Rename the file with the current date and time
        if hasattr(self, 'mfa_filename'):
            current_date_str = datetime.datetime.now().strftime("_%Y%m%d")
            output_filename = os.path.splitext(self.mfa_filename)[0] + current_date_str + ".csv"
            os.rename(self.mfa_filename, output_filename)
            with open(output_filename, 'w') as f:
                f.write(self.output.get('1.0', tk.END))

        # Close the GUI window
        self.root.destroy()




if __name__ == '__main__':
    # root = tk.Tk()
    gui = MFAReportAndEmailCounterGUI()
    # root.mainloop()