import argparse
import logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import qrcode
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
                "FieldTech": params[0].attrib['Value'],
                "CostCode": params[1].attrib['Value'],
                "Project": params[2].attrib['Value'],
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
        version=12,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        # box_size=9,
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

    # Calculate the number of QR codes per row and column
    num_per_row = 4 
    num_per_col = 4

    # Calculate the size of each QR code on the A4 page
    qr_width = a4_width // num_per_row
    qr_height = qr_width

    # Create a new blank A4-sized image
    a4_page = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))

    # Create a font for the text
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20) 
        print(font.getbbox("BEEF"))

    # Paste each QR code into the A4 page
    for i, qr_filename in enumerate(qr_filenames):
        qr_image = Image.open(qr_filename)
        row = i // num_per_row
        col = i % num_per_row

        new_width = int(0.9*qr_width)        
        buffer = (qr_width - new_width) // 2
        qr_image_resized = qr_image.resize((new_width, new_width))
        print(buffer)
        a4_page.paste(qr_image_resized, (buffer + (col * qr_width),
                                        (buffer + (row * qr_width))))

        # Add text above and below the QR code
        draw = ImageDraw.Draw(a4_page)
        text_data = data_dicts[i]
        # text_above = f"{text_data['Run']}\nRun ID: {text_data['RunID']}" 
        text_below = f"{text_data['SiteName']}\nSample ID: {text_data['SampleID']}" 
        # _, _, text_above_width, text_above_height = font.getbbox(text_above)
        _, _, text_below_width, text_below_height = font.getbbox(text_below)

        # print(text_below_width, text_below_height)
        # print(text_above_width, text_above_height)
        # text_pos_x_above = buffer + (col * qr_width + (qr_width - text_above_width) // 2)
        text_pos_x_below = 2*buffer + (col * qr_width)
        # text_pos_y_above = buffer//2 + row * (qr_height)
        # print(text_pos_x_above, text_pos_y_above) 
        text_pos_y_below = (row+1) * qr_height - 2*buffer
        # draw.text((text_pos_x_above, text_pos_y_above),
        #           text_above,
        #           fill=(0, 0, 0),
        #           font=font)
        draw.text((text_pos_x_below, text_pos_y_below),
                  text_below,
                  fill=(0, 0, 0),
                  font=font)
        
    # Save the A4 page as an image file
    a4_page.save(output_filename)
            
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

    page_filename = f"run_{run_id}_printable.png"

    create_printable_a4_page(qr_filenames, data_dicts, page_filename)


if __name__ == "__main__":
    main()
