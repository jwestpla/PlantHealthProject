import API
import webScraping
import extractFromPdfs
import createJSON

def main():
    print("Running API script...")
    API.run()

    print("Running Web Scraping script...")
    webScraping.run()

    print("Running Extract From PDFs script...")
    extractFromPdfs.run()

    print("Running Create JSON script...")
    createJSON.run()
    
if __name__ == '__main__':
    main()