import argparse
import logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import qrcode
import textwrap
from PIL import Image, ImageDraw, ImageFont

def process_xml(xml_file_path):
    # Your XML processing and QR code generation logic goes here
    tree = ET.parse(xml_file_path)

    field_entry = tree.getroot()
    
    print(field_entry.tag)

    qr_list = []
    data_dicts = []

    for run in field_entry:
        run_id = run.attrib['ID']
        print("==================")
        print(f"Run {run_id}")
        run_name = run.find('RunName').text
        run_date = run.find('RunDate').text
        print(run_name) 
        print(run_date) 
        print("==================")
        for sample in run.findall('Sample'):
            sample_id = sample.attrib['ID'] 
              
            params = sample.findall('Parameter')

            sample_data = {
                "RunName": run_name,
                # "RunID": run_id,
                # "RunDate": run_date,
                "SiteName": sample.find('SiteName').text,
                # "FormFile": sample.find('FormFile').text,
                # "FieldTech": params[0].attrib['Value'],
                # "CostCode": params[1].attrib['Value'],
                # "Project": params[2].attrib['Value'],
                "SampleID": sample_id,
            }
            
            sample_root = ET.Element("Sample")
            sample_root.attrib = {
                'ID': sample_id
            }

            for key, value in sample_data.items():
                element = ET.SubElement(sample_root, key)
                element.text = value
            
            xml_string = ET.tostring(sample_root, encoding="utf8", method="xml").decode()

            pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")
            
            print(pretty_xml)
            with open(f"{sample_id}.xml", "w", encoding="utf8") as file:
                file.write(pretty_xml)
            qr_filename = f"{sample_id}.png"
            generate_qr_code_from_xml(pretty_xml, f"{sample_id}.png")
            
            qr_list += [qr_filename]
            data_dicts += [sample_data]
            
    return run_id, data_dicts, qr_list


def generate_qr_code_from_xml(xml_string, filename):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        # box_size=,
        border=4
    )

    # Add the XML data to the QR code
    qr.add_data(xml_string)
    qr.make(fit=False)

    # Create an image from the QR code data
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a file
    qr_image.save(filename)
    

def create_printable_a4_page(qr_filenames, data_dicts, output_filename):
    # Define the size of the A4 page in pixels (at 300 DPI)
    a4_width, a4_height = 2480, 3508

    # Define the size of each cell in pixels (at 300 DPI)
    cell_width, cell_height = 827, 425
    
    # Calculate the size of each code on the A4 page
    qr_height = int(cell_height * .9)
    qr_width = qr_height
    
    # Calculate the space between qr code and edge of cell
    cell_buffer = (cell_height - qr_height) // 2

    # Create a new blank A4-sized image
    a4_page = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))

    # Define sizes of whitespace around the page
    header = 68 # 5.8 mm = 68.5 px @ 300 DPI
    footer = 17 # 1.43 mm = 16.9 px @ 300 DPI
    margins = 9 # 0.78 mm = 8.85 pm @ 300 DPI
    

    # Create a font for the text
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30) 

    # Paste each QR code into the A4 page...
    for row, qr_filename in enumerate(qr_filenames):
        
        qr_image = Image.open(qr_filename)
        
        text_data = data_dicts[row]
        site_text = f"{text_data['SiteName']}"
        id_text = f"ID: {text_data['SampleID']}" 
        wrapped_text = textwrap.wrap(site_text, width=22)
        wrapped_text += [id_text]
        
        final_text = "\n".join(wrapped_text)
        print(final_text)
        
        # ...in triplicate (3 per row)
        for col in range(3):
            print(f"Cell: {row}, {col}")
        
            qr_image_resized = qr_image.resize((qr_width, qr_height))
        
            a4_page.paste(qr_image_resized, (margins + cell_buffer + (col * cell_width),
                                        (header + cell_buffer + (row * cell_height))))

            draw = ImageDraw.Draw(a4_page)

            text_pos_x = margins + cell_buffer + (col * cell_width) + qr_width + (.2*cell_buffer)
            text_pos_y = header + cell_buffer + (row * cell_height) + cell_buffer
            print(text_pos_x, text_pos_y) 
            
            # # draw.text((text_pos_x_above, text_pos_y_above),
            # #           text_above,
            # #           fill=(0, 0, 0),
            # #           font=font)
            draw.text((text_pos_x, text_pos_y),
                      final_text,
                      fill=(0, 0, 0),
                      font=font)
        
    # Save the A4 page as an image file
    a4_page.convert('RGB').save(output_filename)

def setup_logging(logging_level):
    # Set up logging based on the specified logging level
    logging.basicConfig(level=logging_level.upper(),
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def main():
    parser = argparse.ArgumentParser(description='Process XML and generate QR codes.')
    parser.add_argument('xml_file', type=str, help='Path to the XML file')
    # parser.add_argument('target_datetime', type=str, help='Target datetime in yyyy-mm-dd hh:mm:ss format')
    parser.add_argument('-q', '--quiet', action='store_const', const='CRITICAL', dest='logging_level',
                        default='INFO', help='Show only critical log messages')
    parser.add_argument('-c', '--concise', action='store_const', const='WARNING', dest='logging_level',
                        help='Show concise log messages')
    parser.add_argument('-v','--verbose', action='store_const', const='DEBUG', dest='logging_level',
                        help='Show verbose log messages')


    args = parser.parse_args()

    setup_logging(args.logging_level)

    # Call the function to process XML and generate QR codes
    run_id, data_dicts, qr_filenames = process_xml(args.xml_file)

    page_filename = f"run_{run_id}_printable.pdf"

    create_printable_a4_page(qr_filenames, data_dicts, page_filename)


if __name__ == "__main__":
    main()
