import argparse
import logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import qrcode
import textwrap
from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Tuple, Dict, Optional
import re

script_directory = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_directory, "logo.png")

def process_xml(xml_file_path: str) -> Tuple[str, List[Dict[str, str]], List[Image.Image]]:
    """
    Process an XML file containing run and sample data as generated from Sampler.

    Parameters
    ----------
    xml_file_path : str
        Path to the XML file to be processed.

    Returns
    -------
    Tuple[str, List[Dict[str, str]], List[Image.Image]]
        A tuple containing the run ID, a list of dictionaries containing sample data,
        and a list of PIL Image objects generated from the sample data.
    """
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    field_entry = tree.getroot()

    # Initialize lists to store QR codes and sample data dictionaries
    qr_list = []
    data_dicts = []

    # Iterate through each run in the XML
    for run in field_entry:
        run_id = run.attrib['ID']
        run_name = run.find('RunName').text
        logging.debug(f"Processing run: {run_name}")
        run_date = run.find('RunDate').text
        
        # Iterate through each sample in the run
        for sample in run.findall('Sample'):
            sample_id = sample.attrib['ID']

            # Extract sample data
            sample_data = {
                "RunName": run_name,
                "SiteName": sample.find('SiteName').text,
            }

            # Create a new XML element for the sample
            sample_root = ET.Element("Sample")
            sample_root.attrib = {
                'ID': sample_id
            }

            # Populate the sample XML element with data
            for key, value in sample_data.items():
                element = ET.SubElement(sample_root, key)
                element.text = value

            # Convert the sample XML to a prettified string
            xml_string = ET.tostring(sample_root, encoding="utf8", method="xml").decode()
            pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

            # Generate a QR code image from the sample XML
            qr_image = generate_qr_code_from_xml(pretty_xml)

            # Append the QR code and sample data to the respective lists
            qr_list += [qr_image]
            sample_data["SampleID"] = sample_id
            data_dicts += [sample_data]

    return run_id, data_dicts, qr_list

def generate_qr_code_from_string(payload: str) -> Image.Image:
    """
    Generate a QR code image from any string.

    Parameters
    ----------
    payload : str
        The string to be encoded into the QR code.
    filename : str
        The filename to save the generated QR code image.

    Returns
    -------
    Image.Image
        A PIL Image object representing the generated QR code image.
    """
    qr = qrcode.QRCode(
        version=9,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=8
    )

    # Add the string data to the QR code
    qr.add_data(payload)
    qr.make(fit=True)

    # Create an image from the QR code data
    qr_image = qr.make_image(fill_color="black", back_color="white")

    return qr_image


def generate_bar_code_from_string(payload: str) -> Image.Image:
    """
    Generate a QR code image from any string.

    Parameters
    ----------
    payload : str
        The string to be encoded into the QR code.
    filename : str
        The filename to save the generated QR code image.

    Returns
    -------
    Image.Image
        A PIL Image object representing the generated QR code image.
    """
    qr = qrcode.QRCode(
        version=9,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=8
    )

    # Add the string data to the QR code
    qr.add_data(payload)
    qr.make(fit=True)

    # Create an image from the QR code data
    qr_image = qr.make_image(fill_color="black", back_color="white")

    return qr_image


def generate_qr_code_from_xml(xml_string: str) -> Image.Image:
    """
    Generate a QR code image from XML data.

    Parameters
    ----------
    xml_string : str
        The XML data to be encoded into the QR code.
    filename : str
        The filename to save the generated QR code image.

    Returns
    -------
    Image.Image
        A PIL Image object representing the generated QR code image.
    """
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=9,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=8
    )

    # Add the XML data to the QR code
    qr.add_data(xml_string)
    qr.make(fit=True)

    # Create an image from the QR code data
    qr_image = qr.make_image(fill_color="black", back_color="white")

    return qr_image


def create_printable_a4_page(qr_images: List[Image.Image], data_dicts: List[Dict[str, str]], output_filename: str) -> None:
    """
    Create a printable A4 page containing QR code images and associated text.
    
    TODO: Build in support for multiple pages if there are too many sites.
    
    Parameters
    ----------
    qr_images : List[Image.Image]
        A list of PIL Image objects representing QR code images.
    data_dicts : List[Dict[str, str]]
        A list of dictionaries containing associated data for each QR code.
    output_filename : str
        The base filename for the output PDF file.

    Returns
    -------
    None
    """
    
    logging.info("Compiling printable A4 page.")
    # Define the size of the A4 page in pixels (at 300 DPI)
    a4_width, a4_height = 2480, 3508
    
    # # Define sizes of whitespace around the page (WS Sticker page)
    # header = 68 # 5.8 mm = 68.5 px @ 300 DPI
    # footer = 17 # 1.43 mm = 16.9 px @ 300 DPI
    # margins = 9 # 0.78 mm = 8.85 pm @ 300 DPI

    # Define sizes of whitespace around the page (arbitrary narrow margins)
    header = 75
    footer = 75
    margins = 75

    # Define number of rows and columns to print
    num_columns = 3
    num_rows = 8
    print_width = a4_width - (margins*2)
    print_height = a4_height - header - footer
    
    # Define the size of each cell
    cell_width = print_width // num_columns
    cell_height = print_height // num_rows
    
    # Calculate the size of each code on the A4 page
    qr_height = int(cell_height * .9)
    qr_width = qr_height
    
    # Calculate the space between qr code and edge of cell
    cell_buffer = (cell_height - qr_height) // 2
    
    # Define font size (could be done more clever i guess)
    font_size = cell_height // 12
    text_block_length = (.85 * cell_width) // font_size

    # Create a new blank A4-sized image
    a4_page = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))

    # Create a font for the text
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size) 

    # Paste each QR code into the A4 page...
    for i, qr_image in enumerate(qr_images):
        text_data = data_dicts[i]
        site_text = f"{text_data['SiteName']}"
        id_text = f"ID: {text_data['SampleID']}" 
        
        # Wrap the text to (hopefully) fit in the cell
        wrapped_text = textwrap.wrap(site_text, width=text_block_length)
        wrapped_text += [id_text]
        final_text = "\n".join(wrapped_text)

        # Calculate row and column
        row = i // num_columns 
        col = i % num_columns
    
        qr_image_resized = qr_image.resize((qr_width, qr_height))
    
        # Paste QR image
        a4_page.paste(qr_image_resized, (margins + cell_buffer + (col * cell_width),
                                    (header + cell_buffer + (row * cell_height))))

        draw = ImageDraw.Draw(a4_page)

        # Add the text block
        text_pos_x = margins + (col * cell_width) + qr_width 
        text_pos_y = header + cell_buffer + (row * cell_height) + cell_buffer
        draw.text((text_pos_x, text_pos_y),
                  final_text,
                  fill=(0, 0, 0),
                  font=font)

        # Draw line borders to visualise cells
        draw.line(
            [
                (margins + (col)*cell_width, header + ((row)*cell_height)), 
                (margins + (col+1)*cell_width, header + ((row)*cell_height))
            ],
            fill=(0, 0, 0),
            width=2
        )
        draw.line(
            [
                (margins + (col)*cell_width, header + ((row+1)*cell_height)), 
                (margins + (col+1)*cell_width, header + ((row+1)*cell_height))
            ],
            fill=(0, 0, 0),
            width=2
        )
        
        draw.line(
            [
                (margins + (col)*cell_width, header + ((row)*cell_height)), 
                (margins + (col)*cell_width, header + ((row+1)*cell_height))
            ],
            fill=(0, 0, 0),
            width=2
        )
        draw.line(
            [
                (margins + (col+1)*cell_width, header + ((row)*cell_height)), 
                (margins + (col+1)*cell_width, header + ((row+1)*cell_height))
            ],
            fill=(0, 0, 0),
            width=2
        )
    
    # Save the A4 page as an image file
    a4_page.convert('RGB').save(f"{output_filename}_a4.pdf", "PDF", resolution=300)
    
def create_printable_label_document(qr_images: List[Image.Image], data_dicts: List[Dict[str, str]], output_filename: str, dimensions: Optional[List[float]] = None, multiples: int = 1) -> None:
    """
    Create a printable label document containing QR code images, text, and logos.

    Parameters
    ----------
    qr_images : List[Image.Image]
        A list of PIL Image objects representing QR code images.
    data_dicts : List[Dict[str, str]]
        A list of dictionaries containing associated data for each QR code.
    output_filename : str
        The base filename for the output PDF file.
    dimensions : Optional[List[float]], optional
        The dimensions of the label in millimeters [width, height], by default None.
    multiples : int, optional
        The number of times each label is repeated, by default 1.

    Returns
    -------
    None
    """
    logging.info("Compiling printable labels.")
    # Define the size of the label in pixels (at 300 DPI)
    if dimensions:
        px_dim = [dim * 300 / 25.4 for dim in dimensions]
        label_width = int(px_dim[0])
        label_height = int(px_dim[1])
    else:
        # label_width, label_height = 1063, 449 # 90 x 38 mm
        label_width, label_height = 1063, 342 # 90 x 29 mm
        

    logging.debug(f"Compiling label with dimensions px dimensions {label_width}, {label_height} at 300 pdi")
    
    # Calculate the size of each code on the A4 page
    qr_height = int(label_height * 0.95)
    qr_width = qr_height

    font_size = label_height // 10
    logging.debug(f"Font size calculated as {font_size}")
    text_block_length = int((.85 * label_width) // font_size)
    
    # Create a font for the text
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size) 

    qr_buffer = (label_height - qr_height) // 2
    text_buffer = 4*qr_buffer
    logo_buffer = 4*qr_buffer

    pages = []

    logo_image = Image.open(logo_path)

    logo_width = int(0.25*label_height)
    logo_height = int(logo_width * (163/239))

    logo_x = label_width - logo_width
    logo_y = label_height - logo_height

    logo_image_resized = logo_image.resize((logo_width, logo_height))

    # Paste each QR code into the A4 page...
    for site, qr_image in enumerate(qr_images):
        
        # Create a new blank label-sized image
        label_page = Image.new("RGB", (label_width, label_height), (255, 255, 255))
        
        text_data = data_dicts[site]
        site_text = f"{text_data['SiteName']}"
        bar = ["_"]*text_block_length
        bar = "".join(bar)
        id_text = f"{bar}\n\nSample ID: {text_data['SampleID']}" 

        wrapped_text = textwrap.wrap(site_text, width=text_block_length)
        wrapped_text += [id_text]
        final_text = "\n".join(wrapped_text)
        
        qr_image_resized = qr_image.resize((qr_width, qr_height), resample=Image.LANCZOS)
    
        label_page.paste(qr_image_resized, (qr_buffer, qr_buffer))
        label_page.paste(logo_image_resized, (logo_x - logo_buffer, logo_y - logo_buffer), mask=logo_image_resized)
        draw = ImageDraw.Draw(label_page)

        text_pos_x = qr_width
        text_pos_y = text_buffer 
        
        draw.text((text_pos_x, text_pos_y),
                  final_text,
                  fill=(0, 0, 0),
                  font=font)
        # Save the A4 page as an image file
        pages += [label_page]

    multipages = [x for x in pages for _ in range(multiples)]

    logging.debug(f"Generated {len(multipages)} labels ({multiples} for each site).")

    multipages[0].save(f"{output_filename}_labels.pdf", "PDF", resolution=300, save_all=True, append_images=multipages[1:])



def setup_logging(logging_level, logfile):
    # Set up logging based on the specified logging level
    logging.basicConfig(level=logging_level.upper(),
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=None, filemode='w')


def format_argument(value):
    if value.lower() == 'a4':
        return value
    match = re.match(r'(\d+)x(\d+)', value)
    if match:
        dimensions = (int(match.group(1)), int(match.group(2)))
        return dimensions
    raise argparse.ArgumentTypeError("Invalid format value")


def main():
    parser = argparse.ArgumentParser(description='Process XML and generate QR codes.')
    parser.add_argument('xml_file', type=str, help='Path to the XML file')

    parser.add_argument(
        "-f", "--format",
        nargs='+',
        type=format_argument,
        help="Page formats. Accepts 'a4' or AxB, where A and B are dimensions in mm. If multiple formats are specified, a copy of each will be produced."
    )

    parser.add_argument(
        "-m", "--multiples",
        type=int,
        default=1,
        help="Number of duplicates of each site to produce. Only applies to label formats (AxB). Does not apply to a4 copies.",
        dest='multiples'
    )
    
    parser.add_argument(
        "-o", "--out",
        type=str,
        default=".",
        help="directory to which to write the pdf and log files",
        dest='outdir'
    )
    
    parser.add_argument('-q', '--quiet', action='store_const', const='CRITICAL', dest='logging_level',
                        default='INFO', help='Show only critical log messages')
    parser.add_argument('-c', '--concise', action='store_const', const='WARNING', dest='logging_level',
                        help='Show warning log messages')
    parser.add_argument('-d','--debug', action='store_const', const='DEBUG', dest='logging_level',
                        help='Show all log messages')
    parser.add_argument('--logfile', type=str, help="Indicate a file to which to save the logs")

    args = parser.parse_args()

    try:
        setup_logging(args.logging_level, args.logfile)
        logging.info("Starting QR Generator.")
        logging.debug("Parsing Arguments.")
        logging.debug(f"Arguments supplied: {args}")

        # Call the function to process XML and generate QR codes
        logging.info("Parsing XML file.")
        run_id, data_dicts, qr_filenames = process_xml(args.xml_file)
        logging.debug(f"XML file parsed for run {id}.")
        logging.debug(f"Data parsed from XML file: {data_dicts}")

        page_filename = os.path.join(f"{args.outdir}", f"run_{run_id}_printable")

        for pf in args.format:
            if pf == "a4":
                create_printable_a4_page(qr_filenames, data_dicts, page_filename)
            else:
                create_printable_label_document(qr_filenames, data_dicts, page_filename, dimensions=pf, multiples=args.multiples)
    except Exception as e:
        logging.error(e)
        raise 

if __name__ == "__main__":
    main()
