import os
import pandas as pd
from bs4 import BeautifulSoup


def extract_high_school_from_html(html_content):
    try:
        # Extract high school name using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Search for the section element
        education_section = soup.find('section', {'id': 'education-section'})

        if education_section:
            education_entries = education_section.find_all('div', class_='education-entry')
            for entry in education_entries:
                school_name = entry.find('h3', class_='school-name')
                if school_name and 'high school' in school_name.text.lower():
                    return school_name.text.strip()

        return "High School not found"

    except Exception as e:
        return f"Error processing file: {str(e)}"


def process_linkedin_profiles(input_csv, output_csv):
    try:
        # Read input CSV and do error handling
        profiles_df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: The input CSV file '{input_csv}' was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The input CSV file '{input_csv}' is empty.")
        return
    except pd.errors.ParserError:
        print(f"Error: There was a problem parsing the CSV file '{input_csv}'.")
        return

    high_school_data = []

    for index, row in profiles_df.iterrows():
        # Get html files
        linkedin_url = row['LinkedIn URL']
        html_file = f"{linkedin_url.split('/')[-2]}.html"
        html_path = "./linkedin_profiles_html/" + html_file

        if os.path.exists(html_path):
            try:
                with open(html_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                # Do extraction
                high_school = extract_high_school_from_html(html_content)
            except FileNotFoundError:
                high_school = "HTML file not found"
            except Exception as e:
                high_school = f"Error reading file: {str(e)}"
        else:
            high_school = "HTML file not found"

        high_school_data.append({
            'LinkedIn URL': linkedin_url,
            'High School': high_school
        })

    # Create a DataFrame for output
    output_df = pd.DataFrame(high_school_data)

    try:
        # Save to CSV
        output_df.to_csv(output_csv, index=False)
        print(f"Output saved to '{output_csv}'.")
    except Exception as e:
        print(f"Error saving output CSV: {str(e)}")


if __name__ == "__main__":
    input_csv = 'input_linkedin_profiles.csv'
    output_csv = 'output_high_schools.csv'
    process_linkedin_profiles(input_csv, output_csv)
