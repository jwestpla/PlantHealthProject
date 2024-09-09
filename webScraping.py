import requests
import json
import os
from tqdm import tqdm

def run():
    """
    This script extracts all etikett numbers, adds it to the relevant url and downloads all the pdfs
    for each product and saves it in the folder "final_labels"
    """
    # Base URL without the addon
    base_url = "https://plvm.mattilsynet.no/plantevernmidler/etiketter/"

    # Load the JSON data
    with open('/Users/joepwestplate/Library/CloudStorage/OneDrive-NorwegianUniversityofLifeSciences/ Prosjekter/plantevern/godkjente_plantevernmidler_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract all unique registreringsnummer, skipping None values
    registreringsnummer_list = list({product['registreringsnummer'] for product in data['preparater'] if product['registreringsnummer']})

    # Print the number of registreringsnummer being processed
    print(f"Processing {len(registreringsnummer_list)} registreringsnummer.")

    # Create the final_labels directory if it doesn't exist
    output_directory = 'final_labels'
    os.makedirs(output_directory, exist_ok=True)

    # Loop through each registreringsnummer, construct the download URL, and save the PDF
    for registreringsnummer in tqdm(registreringsnummer_list, desc="Downloading PDFs", unit="file"):
        if registreringsnummer:  # Ensure registreringsnummer is not None
            # Convert registreringsnummer to the format used in the file names
            addon = registreringsnummer.replace(".", "_") + ".pdf"
            
            # Construct the full URL
            full_url = base_url + addon
            
            # Download the PDF
            response = requests.get(full_url)
            
            # Save the PDF in the final_labels directory
            pdf_filename = addon.replace("_", ".")
            pdf_path = os.path.join(output_directory, pdf_filename)
            
            with open(pdf_path, "wb") as file:
                file.write(response.content)
            
            #print(f"PDF downloaded and saved as {pdf_path}")
            
if __name__ == "__main__":
    run()