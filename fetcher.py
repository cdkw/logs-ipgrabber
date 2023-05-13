import re
import openpyxl
import requests
from openpyxl.styles import Font

# Define the pattern using regular expression
pattern = r'\[Server thread/INFO\]: (\w+)\[/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+\] logged'

# Create a workbook and select the active sheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# Set the column headers
sheet['A1'] = 'IP'
sheet['B1'] = 'Names'
sheet['C1'] = 'VPN'

# Set the width of columns A, B, and C
sheet.column_dimensions['A'].width = 17
sheet.column_dimensions['B'].width = 40
sheet.column_dimensions['C'].width = 10

# Make the headers bold
bold_font = Font(bold=True)
sheet['A1'].font = bold_font
sheet['B1'].font = bold_font
sheet['C1'].font = bold_font

# Open the text file for reading
try:
    with open('logfile.txt', 'r') as file:
        lines = file.readlines()
except IOError:
    print("Error: Unable to open the file 'logfile.txt'")
    exit()

row = 2  # Start from row 2

# Maintain a dictionary to store IP addresses, names, and VPN status
ip_data = {}

# Iterate through each line in the file
for line in lines:
    # Search for the pattern in each line
    match = re.search(pattern, line)

    if match:
        # Extract the name and IP address from the line
        name = match.group(1)
        ip = match.group(2)

        # Check if the IP address is already in the dictionary
        if ip in ip_data:
            # Check if the name is already associated with the IP address
            if name not in ip_data[ip]['names']:
                # Append the name to the existing list of names for that IP
                ip_data[ip]['names'].append(name)
        else:
            # Create a new entry for the IP address in the dictionary
            ip_data[ip] = {'names': [name], 'is_vpn': None}

# Query the IP geolocation service for VPN information
for ip, data in ip_data.items():
    response = requests.get(f'https://ipapi.com/{ip}?access_key=YOUR_ACCESS_KEY')
    if response.status_code == 200:
        result = response.json()
        data['is_vpn'] = result.get('security', {}).get('is_vpn')

# Write the IP addresses, corresponding names, and VPN status to the spreadsheet
for ip, data in ip_data.items():
    sheet.cell(row=row, column=1).value = ip
    sheet.cell(row=row, column=2).value = ', '.join(data['names'])
    sheet.cell(row=row, column=3).value = 'Yes' if data['is_vpn'] else 'No'
    row += 1

# Save the workbook
try:
    workbook.save('output.xlsx')
    print("Extraction completed. The data has been saved to 'output.xlsx'.")
except PermissionError:
    print("Error: Unable to save the Excel file. Please make sure the file is not open in another program.")