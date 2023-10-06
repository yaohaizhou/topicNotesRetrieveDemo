import requests
from lxml import html
import csv

# Attention!!
# TODO: Note that this file needs modifying because it only output [URL,Topic Notes]
# The csv file still needs Summary column
# Note that demo.csv in this folder is created manually

class Crawler(object):
    def __init__(self,csv_save_path:str,basicURL:str) -> None:
        self.csv_save_path = csv_save_path
        self.basicURL = basicURL
    
    def extractCourseChapters(self,url:str):
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        hrefDirs = []

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using lxml
            page_content = html.fromstring(response.text)

            # Use the initial XPath expression to select the 'course-chapters' element
            course_chapters = page_content.xpath("//*[@id='course-chapters']")

            # Check if the 'course-chapters' element was found
            if course_chapters:
                # Get all the subdirectory elements under 'course-chapters'
                subdirectories = course_chapters[0].xpath(".//li/ol/li")

                # Iterate through the subdirectories
                for sub_directory in subdirectories:
                    # Get the 'href' attribute of the element
                    href = sub_directory.xpath(".//@href")

                    # Check if the 'href' attribute was found
                    if href:
                        # Print the 'href' attribute value
                        href_value = url + '/' + str(href[0]).split('/')[-1]
                        hrefDirs.append(href_value)
                        # print("Href Attribute:", href_value)

                    else:
                        print("Href attribute not found in the element content.")
            else:
                print("Element 'course-chapters' not found with the specified XPath.")
        else:
            print("Failed to retrieve the web page. Status code:", response.status_code)

        print("extractCourseChapters Done")
        return hrefDirs
    
    def extractTopicNotes(self,url:str)->str:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using lxml
            page_content = html.fromstring(response.text)

            # Use the XPath expression to select the element you want
            element = page_content.xpath("//*[@id='topic-basics']")

            # Check if the element was found
            if element:
                # Extract all the h2 subheadings and their associated content
                h2_elements = element[0].xpath(".//h2")
                subdirectories = []

                # Iterate through the h2 elements and organize the content into subdirectories
                for h2_element in h2_elements:
                    # Extract the h2 heading text
                    heading_text = h2_element.text_content().strip()

                    # Extract the content associated with the current h2 heading
                    content = []
                    next_element = h2_element.getnext()
                    while next_element is not None and next_element.tag != 'h2':
                        content.append(next_element.text_content())
                        next_element = next_element.getnext()

                    # Store the heading and content in a subdirectory dictionary
                    subdirectory = {
                        'heading': heading_text,
                        'content': content
                    }
                    subdirectories.append(subdirectory)
                if subdirectories == []:
                    # no any sub h2 header
                    return [element[0].text_content()]
                else:
                    # Print or process the subdirectories as needed
                    res = []
                    for subdir in subdirectories:
                        contentString = ""
                        contentString += subdir['heading'] + " "
                        # print("Heading:", subdir['heading'])
                        # print("Content:")
                        for paragraph in subdir['content']:
                            # print(paragraph)
                            contentString += paragraph
                        res.append(contentString)
                    
                    return res
            else:
                print("Element not found with the specified XPath.")
                return ""

        else:
            print("Failed to retrieve the web page. Status code:", response.status_code)
            return ""
        
    def exportCSVFile(self):

        # Create or open a CSV file for writing
        with open(self.csv_save_path, mode='w', newline='') as csv_file:
            # Create a CSV writer
            csv_writer = csv.writer(csv_file)

            # Write data rows to the CSV file
            csv_writer.writerow(['URL', 'Topic Notes'])

            for url in self.extractCourseChapters(self.basicURL):
                for topic_note in self.extractTopicNotes(url):
                    csv_writer.writerow([url, topic_note])
        
        print("exportCSVFile Done")

if __name__ == '__main__':
    csv_save_path = "example.csv"
    basicURL = "https://www.studypug.com/ap-calculus-bc"

    crawler = Crawler(csv_save_path,basicURL)
    crawler.exportCSVFile()