## TO DO: 
## - Need to get first page printed and saved in PDF folder
## - Need to output file to correct folder for EK
## - Need to delete contents of pdf folder after finsihed with document
## - Need to loop through links similiar to this

## Example Site: East Baton Rouge Parish on google sheet -- https://docs.google.com/spreadsheets/d/1maq9oEaDHRBlzO2gzRfo58v-1MG_dYfmFsJ7fiyTGRU/edit?gid=0#gid=0

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from fpdf import FPDF
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors
import requests
#import chromedriver_binary  # Adds chromedriver binary to path
#from selenium.webdriver.common.keys import Keys  # For simulating pressing 'Enter'
import os
import re
import PyPDF2
import pyautogui

# Function to download a file from a URL and save it to the local directory
def download_file(url, folder_path):
    # Get the filename from the URL
    filename = os.path.basename(url)
    file_path = os.path.join(folder_path, filename)
    
    # Send a GET request to the file URL
    response = requests.get(url)
    
    # If the request was successful, save the file to the folder
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

import os
import re
from PyPDF2 import PdfReader, PdfWriter

# Define a function to determine the priority of a file
def priority_key(filename):
    # Check if the filename matches the pattern: long string of digits + underscores
    match = re.match(r'^\d+(_[^_]+){3}', filename)
    return (0, filename.lower()) if match else (1, filename.lower())

def find_all_pdfs(folder_path, output_file):
    # Get all PDF names
    pdfFiles = [filename for filename in os.listdir(folder_path) if filename.endswith('.pdf')]
    pdfFiles.sort()  # Replace `priority_key` if you have a specific sorting function
    print(pdfFiles)

    pdfWriter = PdfWriter()

    for filename in pdfFiles:
        pdfFileObj = None  # Initialize pdfFileObj to avoid UnboundLocalError
        try:
            file_path = os.path.join(folder_path, filename)  # Ensure correct path
            pdfFileObj = open(file_path, 'rb')
            pdfReader = PdfReader(pdfFileObj)

            # Iterate through pages and add to writer
            for pageNum in range(len(pdfReader.pages)):
                try:
                    pageObj = pdfReader.pages[pageNum]
                    pdfWriter.add_page(pageObj)
                except Exception as e:
                    print(f"Skipping a page in {filename} due to an error: {e}")

        except Exception as e:
            print(f"Skipping {filename} due to an error: {e}")
        finally:
            if pdfFileObj:  # Only close if the file was successfully opened
                pdfFileObj.close()

    # Write the combined PDF
    output_path = os.path.join(os.getcwd(), output_file)
    with open(output_path, 'wb') as pdfOutput:
        pdfWriter.write(pdfOutput)
    print(f"Combined PDF saved as {output_path}")
    return pdfFiles

def convert_to_datenumber(meeting_date):
    # Parse the date using the format 'MMM d, YYYY'
    parsed_date = datetime.strptime(meeting_date, '%b %d, %Y')
    
    # Format the date to 'YYYYMMDD'
    datenumber = parsed_date.strftime('%Y%m%d')
    
    return datenumber

# Function to automate the workflow
def automate_print_to_pdf(driver, url):
    print("Attempting to print first page..")
    #driver.save_screenshot('screenshot.png')
    try:
        wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
        print_button = driver.find_element(By.XPATH, '//button[@class="print" and @data-original-title="Print"]')
        print_button.click()
        print("Print button found")
        time.sleep(5)  # Wait for the popup to load

        # Step 3: In the popup, click the Print button
        print("Looking for Second Print Button...")
        popup_print_button = driver.find_element(By.XPATH, '//button[text()="Print"]')
        popup_print_button.click()
        print("Second print button found")

    except Exception as e:
        print(f"An error occurred during the web interaction: {e}")
        driver.quit()
        return

    # Step 4: Using PyAutoGUI to interact with the MacOS interface
    time.sleep(5)  # Wait for the Print dialog to open (adjust the timing if necessary)
    print('Starting to move around screen...')
    # im = pyautogui.screenshot('screenshot.png')
    # print(im)
    # Move cursor to the "Save" button coordinates (you may need to find the exact coordinates on your system)
    pyautogui.moveTo(856, 255)  # Adjust coordinates for your specific setup
    pyautogui.click()  # Click the Save button
    time.sleep(2)  # Wait for the Save dialog to appear

    # Step 5: In the Save As dialog, set the file name
    pyautogui.write('1.pdf')  # Write the filename as 1.pdf
    pyautogui.press('tab', presses=2)  # Navigate to the folder selection field

    # Step 6: Navigate to the target folder and save
    pyautogui.write('jcps dresscode scraper')  # Enter the target folder name
    pyautogui.press('enter')  # Open the folder
    time.sleep(1)  # Wait for navigation
    pyautogui.press('enter')  # Confirm Save

    # Closing the WebDriver
    driver.quit()

# Example usage
if __name__ == "__main__":
    link = "https://go.boarddocs.com/ca/sfusd/Board.nsf/Public"
    meeting_date = "Sep 10, 2024"
    year_drop = "2024"
    title = "Ratification of the attached contracts and amendments to contracts under $114,500 processed between July 27, 2024 – August 24, 2024"
    output_file = '634410_SAN FRANCISCO UNIFIED_08-24-24_CONTRACTS_ATTACHMENTS.pdf'

    folder_path = os.path.join(os.getcwd(), 'pdf')

    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Open the target URL
    url = link  # Replace with your target URL
    driver.get(url)
    
    # Create an explicit wait for elements to load
    wait = WebDriverWait(driver, 30)

    try:
        print(driver.page_source)
        # Wait for the loading overlay to disappear
        wait.until(EC.invisibility_of_element((By.ID, 'loading-boarddocs')))

        # Look for the meeting li element
        li_meeting_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'li-meetings'))
    )
    
        # Scroll the element into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", li_meeting_element)
        time.sleep(1)  # Allow time for the page to adjust`
    
        # Click the element
        li_meeting_element.click()
        print(f"Clicked on Meeting Tab")

        time.sleep(5)

        # open drop down for correct year
        element_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//section[@role='heading']//a[contains(text(), '{year_drop}')]"))
    )
        element_year.click()
        print(f"Clicked on {year_drop}")

        time.sleep(5)
        
        # find correct meeting date 
        datenumber = convert_to_datenumber(meeting_date)
        print(f"Searching for {datenumber} element...")
        element_meeting_date = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@datenumber='{datenumber}']"))
    )
        element_meeting_date.click()
        print(f"Clicked on meeting with {meeting_date}.")

        time.sleep(5)

        # Step 1: Locate the <li> element by ID and click it
        li_element = wait.until(EC.element_to_be_clickable((By.ID, 'li-agenda')))
        driver.execute_script("arguments[0].scrollIntoView(true);", li_element)  # Scroll into view
        li_element.click()
        print(f"Clicked on agenda tab")

        time.sleep(5)

        # Step 2: Wait for the dropdown options to load and select the desired year
        li_element_2 = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(@xtitle, '{title}')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", li_element_2)  # Scroll into view
        li_element_2.click()
        print(f'Clicked on {title} page')

        # save first page
        try:
            # Wait for the print button to be clickable
            print_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "print"))
            )
            
            # Scroll into view and click
            driver.execute_script("arguments[0].scrollIntoView(true);", print_button)
            time.sleep(1)  # Allow for scroll adjustment
            print_button.click()
            print("Clicked on print button.")
            
            # Wait for the print dialog button to appear and click it
            popup_print_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='ui-dialog-buttonset']/button[text()='Print']"))
            )
            popup_print_button.click()
            print("Clicked on print button in popup.")
            
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(30)

    

        # Step 4: Find the parent div by ID
        parent_id = "attachment-public-D8HQKW69BF1D"  # This changes everytime so need a different ID
        parent_div = wait.until(EC.presence_of_element_located((By.ID, parent_id)))  # Wait for the parent div to be present

        # Step 5: Locate all <a> tags with the class 'public-file' within the parent div
        file_links = parent_div.find_elements(By.CSS_SELECTOR, "a.public-file")
        
        print("Finished collecting file links")
        
        # Step 6: Get the current working directory (same folder you're working in)
        folder_path = os.path.join(os.getcwd(), 'pdf')  # Save in a subfolder named 'pdf'

        # Step 7: Download each file
        for link in file_links:
            file_url = link.get_attribute('href')  # Get the URL of the file
            download_file(file_url, folder_path)  # Download the file to the current folder

        print("Finished downloading file links as pdfs")


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()  # Close the browser after the script finishes or an error occu

    # automate_print_to_pdf(driver, url)
    find_all_pdfs(folder_path, output_file)