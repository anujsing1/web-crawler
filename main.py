from bs4 import BeautifulSoup
import csv

def extract_divs(file_path):
    # Load the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')

    # Find all divs with the class 'f-provider-card__main'
    lis = soup.find_all('li', class_='l-providers-list__item js-provider-list-item')
    # Define the fields that will be used as column headers in the CSV file
    fields = ['zip_code', 'provider', 'start_at','speed','connection_type','availablity']
    rows = []
    # Print the extracted divs
    # with open('output_file.txt', 'a', encoding='utf-8') as file:
    for li in lis:
        sp = li.find_all('span', class_='f-provider-card__provider-name')
        span_values = []
        span_values.append('08820')
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
        rows.append(span_values)
            # file.write(f"{span_values}\n")
    print(rows)
    # Open a file called 'EmployeeData.csv' in write mode ('w') and use it as a context manager
    # The 'with' statement ensures that the file is automatically closed when the block of code is finished
    with open('output.csv', 'w') as f:
        
        # Create a CSV writer object that will write to the file 'f'
        csv_writer = csv.writer(f)
        
        # Write the field names (column headers) to the first row of the CSV file
        csv_writer.writerow(fields)
        
        # Write all of the rows of data to the CSV file
        csv_writer.writerows(rows)
        
if __name__ == "__main__":
    # Path to your HTML file
    html_file_path = '/Users/anujsingh/Desktop/web-crawler/2.html'
    extract_divs(html_file_path)
