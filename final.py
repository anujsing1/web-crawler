import requests
from bs4 import BeautifulSoup
import csv

def extract_span_values(html_content,zip_code):
    soup = BeautifulSoup(html_content, 'lxml')
    # Find all divs with the class 'f-provider-card__main'
    lis = soup.find_all('li', class_='l-providers-list__item js-provider-list-item')
    values = []
    # Print the extracted divs
    for li in lis:
        span_values = []
        sp = li.find_all('span', class_='f-provider-card__provider-name')
        span_values.append(f"{zip_code}")
        for s in sp:
            span_values.append(s.text.strip())
        strngs = li.find_all('strong', class_='f-provider-card__plans-price')
        for strng in strngs:
            span_values.append(strng.text.strip())
        cardSpeeds = li.find_all('strong', class_='f-provider-card__speeds-value')
        for cardSpeed in cardSpeeds:
            span_values.append(cardSpeed.text.strip())

        cardConnections = li.find_all('span', class_='f-provider-card__connection-value')
        for cardConnection in cardConnections:
            span_values.append(cardConnection.text.strip())
        print(span_values)
        values.append(span_values)
    return values

def get_html_for_zip(zip_code, endpoint_url):
    response = requests.get(f"{endpoint_url}?zip={zip_code}")
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve data for zip code {zip_code} and response code {response.status_code}")
        return None
    
def process_zipcodes(file_path, endpoint_url):
    with open(file_path, 'r') as file:
        zip_codes = [line.strip() for line in file.readlines()]
    
    for zip_code in zip_codes:
        html_content = get_html_for_zip(zip_code, endpoint_url)
        if html_content:
            span_values = extract_span_values(html_content,zip_code)
            print(f"extracting for zip code {zip_code}")
            # Define the fields that will be used as column headers in the CSV file
            fields = ['zip_code', 'provider', 'start_at','speed','connection_type','availablity']
            # Open a file called 'EmployeeData.csv' in write mode ('w') and use it as a context manager
            # The 'with' statement ensures that the file is automatically closed when the block of code is finished
            with open('output.csv', 'w') as f:
                # Create a CSV writer object that will write to the file 'f'
                csv_writer = csv.writer(f)
                
                # Write the field names (column headers) to the first row of the CSV file
                csv_writer.writerow(fields)
                
                # Write all of the rows of data to the CSV file
                csv_writer.writerows(span_values)
            print(f"values for zip code {zip_code} extracted")

if __name__ == "__main__":
    # Path to your HTML file
    zipcodes_file_path = 'C:\\Users\\Administrator\\Downloads\\web-crawler-master\\web-crawler-master\\zip.txt'
    endpoint_url = 'https://broadbandnow.com/New-Jersey/Edison'
    process_zipcodes(zipcodes_file_path, endpoint_url)
    print(f"Work Completed!!!")
