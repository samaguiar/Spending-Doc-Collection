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



# link = "https://columbusschools.spending.socrata.com/#!/year/2025/explore/1/vendorname"


# # Initialize the WebDriver
# driver = webdriver.Chrome()

# # Open the target URL
# url = link  # Replace with your target URL
# driver.get(url)

# # Create an explicit wait for elements to load
# wait = WebDriverWait(driver, 30)

# # Step 1: Click the dropdown to open it
# dropdown_button = driver.find_element(By.CSS_SELECTOR, '.dropdown-toggle')
# dropdown_button.click()

# # Step 2: Wait for the dropdown options to load and select the desired year
# year_to_select = '2025'  # Replace with the year you want to select
# year_option = WebDriverWait(driver, 10).until(
#     EC.visibility_of_element_located((By.XPATH, f"//a[text()='{year_to_select}']"))
# )
# year_option.click()

# # Step 3: Wait for the download button to update with the new year
# download_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.download-btn'))
# )

# # Step 4: Click the download button
# download_button.click()

# # Wait a few seconds to ensure the download starts (adjust as necessary)
# time.sleep(5)

# # Close the WebDriver
# driver.quit()

today_date = datetime.today().strftime('%Y-%m-%d')
print(today_date)

df = pd.read_csv(f"/Users/samaguiar/Downloads/checkbook_data_{today_date}.csv")
df_select_columns = df[['Project', 'Segment3', 'Department', 'Check Date', 'Description', 'Vendor', 'Check #', 'Amount']]
print(df_select_columns.head())
print(df_select_columns.columns)
df_select_columns.to_csv("output.csv", index = False)

# # Convert DataFrame to a list of lists (for the table)
# data = [df_select_columns.columns.tolist()] + df_select_columns.values.tolist()

# # Set up the PDF document
# pdf = SimpleDocTemplate(
#     "scaled_excel_to_pdf_improved.pdf", 
#     pagesize=landscape(letter)  # Use landscape mode for more width
# )

# # Adjust column widths based on content length
# # You can calculate widths by checking the length of content in each column
# column_widths = []
# total_page_width = landscape(letter)[0] - 2 * 20  # Page width minus margins

# # Define a minimum and maximum width
# min_width = 50
# max_width = total_page_width / len(df.columns)

# # Calculate proportional widths based on content
# for col in df.columns:
#     max_content_length = max(df[col].astype(str).apply(len).max(), len(str(col)))
#     proportional_width = min(max(min_width, max_content_length * 6), max_width)
#     column_widths.append(proportional_width)

# # Adjust page scaling if the total width exceeds the page size
# if sum(column_widths) > total_page_width:
#     scale_factor = total_page_width / sum(column_widths)
#     column_widths = [w * scale_factor for w in column_widths]

# # Create the table with adjusted column widths
# table = Table(data, colWidths=column_widths)

# # Style the table
# table.setStyle(TableStyle([
#     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('FONTSIZE', (0, 0), (-1, -1), 10),  # Increase font size to 10
#     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
# ]))

# # Split the table into multiple pages if it exceeds the page height
# elements = []
# rows_per_page = 25  # Adjust this number based on your data and font size
# for start in range(0, len(data), rows_per_page):
#     table_chunk = Table(data[start:start + rows_per_page], colWidths=column_widths)
#     elements.append(table_chunk)
#     elements.append(PageBreak())  # Add a page break after each chunk

# # Build the PDF
# pdf.build(elements)

# print("Improved PDF saved: 'scaled_excel_to_pdf_improved.pdf'.")