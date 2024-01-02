import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# List of masses to query - Enter m/z values directly comma separated
masses = [707.400647264]

# Function to perform the search for a single mass
def search_mass(mass):
    driver = webdriver.Chrome()
    driver.get("https://macpepdb.mpc.ruhr-uni-bochum.de/peptides/search?tab=theoretical-mass-search")
    time.sleep(2)
    try:
        mass_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Theoretical mass']")
        mass_input.clear()  # Clear any existing value
        mass_input.send_keys(str(mass))  # Convert mass to string and send
        time.sleep(5)
        mass_input.send_keys(Keys.RETURN)
        #mass_input.submit() #attempt to submit 
        #search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'search')]")
        #search_button.click()
        #wait = WebDriverWait(driver, 10)  # Adjust the time as needed
        #search_button = wdriver.find_element(By.CSS_SELECTOR, "btn btn-primary")))
        #search_button.click()
        time.sleep(30)  # Adjust this wait time as necessary

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        results_div = soup.find('div', class_='peptides')
        data = []

        if results_div:
            for row in results_div.find_all('tr')[1:]:
                header_cell = row.find('th')
                data_cells = row.find_all('td')

                if header_cell and len(data_cells) >= 1:
                    sequence = header_cell.get_text(strip=True)
                    PDB_mass = data_cells[0].get_text(strip=True)
                    data.append((sequence, PDB_mass))
        else:
            print("Results division not found")

    except Exception as e:
        print(f"An error occurred: {e}")
        data = 'Error'
    finally:
        driver.quit()

    return data if data else 'No results found'

# Dictionary to hold the results for each mass
results = {}

# Perform the search for each mass
for mass in masses:
    results[mass] = search_mass(mass)

# Save results to a CSV file
with open('mass_search_results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Mass', 'Result'])

    for mass, result in results.items():
        writer.writerow([mass, result])

print("Results saved to mass_search_results.csv")
