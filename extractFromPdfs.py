import re
import fitz
import os
from crops_diseases import crops, diseases

def run():
    """
    * Construct functions to extract text from pdf to string, and to look for crops and diseases using RegEx
    in the relevant sections of the pdf (most important algorithm of the project)
    * Creates a new document, called "Extracted_sentences" where each product id is saved, as well as the string
    for finding crops and diseases. This is used for adding crops and diseases, as well as troubleshoot
    * Saves all this information for the final file to update the JSON file
    """

    def extract_text_from_pdf(pdf_path):
        """
        Extract all text from the PDF and return it as a single string.
        """
        text = ""
        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text("text")
        return text


    def extract_first_sentence_after_section(text):
        # First, try to find "Bruksområde" or "BRUKSOMRÅDE"
        match = re.search(r'\b(Bruksområde|BRUKSOMRÅDE)\b\s*\n', text)
        
        # If "Bruksområde" is not found, try to find "Bruksrettledning" or "BRUKSRETTLEDNING"
        if not match:
            match = re.search(r'\b(Bruksrettledning|BRUKSRETTLEDNING)\b\s*\n', text)
        
        # If a match is found, extract the first sentence after the section header
        if match:
            start_pos = match.end()
            following_text = text[start_pos:].strip()
            
            # Extract the first sentence considering full stops outside parentheses
            first_sentence_match = re.match(r'^([^.!?]*\([^)]*\))*[^.!?]*[.!?]', following_text)
            if first_sentence_match:
                return first_sentence_match.group().strip()
        
        # If no relevant section is found, return None
        return "Not found"

    def extract_text_after_virkeomrade(text):
        """
        Extract the text after "Virkeområde" until "Virkemåte" is encountered.
        If "Virkemåte" does not exist, extract until the first full stop.
        """
        # Match the "Virkeområde" section header
        match = re.search(r'\b(Virkeområde|VIRKEOMRÅDE|Virkning|VIRKNING)\b\s*\n', text)
        if match:
            start_pos = match.end()
            # Extract the text after the matched section header
            following_text = text[start_pos:].strip()

            # Look for "Virkemåte"
            virkemate_match = re.search(r'\b(Virkemåte|VIRKEMÅTE|Virkemåde|VIRKEMÅDE)\b', following_text)
            
            if virkemate_match:
                # If "Virkemåte" is found, extract up to this word
                return following_text[:virkemate_match.start()].strip()
            else:
                # If "Virkemåte" is not found, extract up to the first full stop
                first_sentence_match = re.match(r'^([^.!?]*\([^)]*\))*[^.!?]*[.!?]', following_text)
                if first_sentence_match:
                    return first_sentence_match.group().strip()
        return "Not found"

    def extract_crops_from_sentance(sentence, crops):
        found_crops = []
        for crop in crops:
            if re.search(rf'\b{crop}\b', sentence, re.IGNORECASE):
                found_crops.append(crop)
        return found_crops

    def extract_diseases_from_paragraph(paragraph, diseases):
        found_diseases = []
        for disease in diseases:
            if re.search(rf'\b{disease}\b', paragraph, re.IGNORECASE):
                found_diseases.append(disease)
        return found_diseases

    # Directory containing the PDFs
    pdf_directory = '/Users/joepwestplate/Library/CloudStorage/OneDrive-NorwegianUniversityofLifeSciences/ Prosjekter/plantevern/final_labels'
    output_file_path = 'extracted_sentences.txt'

    # Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for filename in os.listdir(pdf_directory):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(pdf_directory, filename)
                try:
                    text = extract_text_from_pdf(pdf_path)
                    first_sentence = extract_first_sentence_after_section(text)
                    found_crops = extract_crops_from_sentance(first_sentence, crops)
                    first_sentance_disease = extract_text_after_virkeomrade(text)
                    found_diseases = extract_diseases_from_paragraph(first_sentance_disease, diseases)
                    
                    if first_sentence:
                        output_file.write(f"File: {filename}\n")
                        output_file.write(f"First Sentence: {first_sentence}\n")
                        output_file.write(f"Crops: {found_crops}\n")
                        output_file.write(f"Diseases paragraph: {first_sentance_disease}\n")
                        output_file.write(f"Diseases: {found_diseases}\n\n")
                    else:
                        output_file.write(f"File: {filename}\n")
                        output_file.write(f"First Sentence: None found\n\n")
                except Exception as e:
                    output_file.write(f"Error processing file {filename}: {e}\n\n")

    print(f"Sentence extraction completed. Results saved to {output_file_path}")
    
if __name__ == "__main__":
    run()