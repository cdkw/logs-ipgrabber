import re
import openpyxl
import requests
from openpyxl.styles import Font
import argparse

# Pattern
pattern = r'\[Server thread/INFO\]: (\w+)\[/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+\] logged'

# Arguments
parser = argparse.ArgumentParser(description='Extract log information.')
parser.add_argument('--file', '-f', help='Specify the log file name')
parser.add_argument('--vpn', action='store_true', help='Enable VPN finding')
args = parser.parse_args()

if not args.file:
    print("Error: Log file name not specified. Please provide the log file using --file or -f.")
    exit()

# Workbook
workbook = openpyxl.Workbook()
sheet = workbook.active

# Headers
sheet['A1'] = 'IP'
sheet['B1'] = 'Names'
sheet['C1'] = 'VPN'
sheet.column_dimensions['A'].width = 17
sheet.column_dimensions['B'].width = 40
sheet.column_dimensions['C'].width = 10
bold_font = Font(bold=True)
sheet['A1'].font = bold_font
sheet['B1'].font = bold_font
sheet['C1'].font = bold_font

# Open text file
try:
    with open(args.file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
except IOError:
    print(f"Error: Unable to open the file '{args.file}'")
    exit()

row = 2 

# Dictionary
ip_data = {}

for line in lines:
    match = re.search(pattern, line)

    if match:
        name = match.group(1)
        ip = match.group(2)

        if ip in ip_data:
            if name not in ip_data[ip]['names']:
                ip_data[ip]['names'].append(name)
        else:
            ip_data[ip] = {'names': [name], 'is_vpn': None}

# Please change YOUR_ACCESS_KEY with yours
if args.vpn:
    for ip, data in ip_data.items():
        response = requests.get(f'https://ipapi.com/{ip}?access_key=YOUR_ACCESS_KEY')
        if response.status_code == 200:
            result = response.json()
            data['is_vpn'] = result.get('security', {}).get('is_vpn')


for ip, data in ip_data.items():
    sheet.cell(row=row, column=1).value = ip
    sheet.cell(row=row, column=2).value = ', '.join(data['names'])
    sheet.cell(row=row, column=3).value = 'Yes' if data['is_vpn'] else 'No' if args.vpn else '-'
    row += 1


try:
    workbook.save('output.xlsx')
    print("Extraction completed. The data has been saved to 'output.xlsx'.")
except PermissionError:
    print("Error: Unable to save the Excel file. Please make sure the file is not open in another program.")
