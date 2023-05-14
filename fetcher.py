import re
import openpyxl
import requests
from openpyxl.styles import Font
import argparse

pattern = r'\[Server thread/INFO\]: (\w+)\[/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+\] logged'

# CLI Arguments
parser = argparse.ArgumentParser(description='Extract log information.')
parser.add_argument('--file', '-f', help='Specify the log file name')
parser.add_argument('--vpn', '-v', action='store_true', help='Enable VPN finding')
parser.add_argument('--geolocation', '-g', action='store_true', help='Enable IP geolocation')
args = parser.parse_args()

# Log File Error
if not args.file:
    print("Error: Log file name not specified. Please provide the log file using --file or -f.")
    exit()

# VPN, Geolocation error
if args.vpn and args.geolocation:
    access_key = 'YOUR_ACCESS_KEY'
elif args.vpn or args.geolocation:
    print("Error: Both VPN and geolocation options need to be specified. Please provide both or neither.")
    exit()
else:
    access_key = None

# Validate the provided access key
if access_key:
    response = requests.get(f'https://ipapi.com/{access_key}')
    if response.status_code != 200:
        print("Error: Invalid access key. Please provide a valid access key from https://ipapi.com/")
        exit()


workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'] = 'IP'
sheet['B1'] = 'Names'
sheet['C1'] = 'VPN'
sheet['D1'] = 'Geolocation'
sheet.column_dimensions['A'].width = 17
sheet.column_dimensions['B'].width = 40
sheet.column_dimensions['C'].width = 10
sheet.column_dimensions['D'].width = 50
bold_font = Font(bold=True)
sheet['A1'].font = bold_font
sheet['B1'].font = bold_font
sheet['C1'].font = bold_font
sheet['D1'].font = bold_font


try:
    with open(args.file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
except IOError:
    print(f"Error: Unable to open the file '{args.file}'")
    exit()

row = 2 

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
            ip_data[ip] = {'names': [name], 'is_vpn': None, 'geolocation': None}


if args.geolocation:
    for ip, data in ip_data.items():
        response = requests.get(f'https://ipapi.com/{ip}?access_key={access_key}')
        if response.status_code == 200:
            result = response.json()
            data['geolocation'] = result.get('country_name', '') + ', ' + result.get('city', '')


if args.vpn:
    for ip, data in ip_data.items():
        response = requests.get(f'https://ipapi.com/{ip}?access_key={access_key}')
        if response.status_code == 200:
            result = response.json()
            data['is_vpn'] = result.get('security', {}).get('is_vpn')

# Write everything to the sheet
for ip, data in ip_data.items():
    sheet.cell(row=row, column=1).value = ip
    sheet.cell(row=row, column=2).value = ', '.join(data['names'])
    sheet.cell(row=row, column=3).value = 'Yes' if data['is_vpn'] else 'No' if args.vpn else '-'
    sheet.cell(row=row, column=4).value = data['geolocation'] if args.geolocation else '-'
    row += 1


try:
    workbook.save('output.xlsx')
    print("Extraction completed. The data has been saved to 'output.xlsx'.")
except PermissionError:
    print("Error: Unable to save the Excel file. Please make sure the file is not open in another program.")
