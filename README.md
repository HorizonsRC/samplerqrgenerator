# Sampler QR Generator and Scanning Scripts

## Description

This project contains utilities for a hydrology fieldwork workflow:
1. Sampler is used to generate an xml file called FieldEntry.xml, which is fed into sampler_qr_generator.py.
2. sampler_qr_generator.py processes the xml into a separate xml block for each site.
3. The xml blocks are then encoded into a QR code for each site.
4. The QR codes are collated onto a single page for printing, intended to be printed as stickers. 
5. The QR stickers are intended to be placed on a set of sample bottles to be filled at one sampling site.
6. The script parse_functions.js is provided to be uploaded and configured into a custom Survey123 form, which provides the ability to automatically fill fields related to the sample site by scanning the corresponding QR code.



