# Sampler QR Generator and Scanning Scripts
This project contains utilities for a hydrology fieldwork workflow:

## Description
- Sampler is used to generate an xml file called FieldEntry.xml, which is fed into sampler_qr_generator.py.
- sampler_qr_generator.py processes the xml into a separate xml block for each site.
- The xml blocks are then encoded into a QR code for each site.
- The QR codes are collated onto a single page for printing, intended to be printed as stickers. 
- The QR stickers are intended to be placed on a set of sample bottles to be filled at one sampling site.
- The script parse_functions.js is provided to be uploaded and configured into a custom Survey123 form, which provides the ability to automatically fill fields related to the sample site by scanning the corresponding QR code.

