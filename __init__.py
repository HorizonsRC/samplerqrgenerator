import HilltopHost
from .sampler_qr_generator import create_printable_a4_page, generate_qr_code_from_string, create_printable_label_document
import json

class QRGenerator:

    def health_check(self):
        return "Ok"

    def send_preregistration_request(self, preregistration_data):
        HilltopHost.LogInfo("You clicked the Notify Lab button.")
        HilltopHost.LogInfo("These are the samples:")

        run_name = preregistration_data.Run.RunName
        run_date = preregistration_data.Run.RunDate
        tech_name = preregistration_data.Run.TechnicianFirstName

        output_dir = preregistration_data.GetSectionInfo("Sampler")["LabelOutputDir"]

        file_prefix = f"{output_dir}{run_name}_{run_date}_{tech_name}"

        payload_list = []
        image_list = []
    
        for sample in preregistration_data.Samples:
            HilltopHost.LogInfo(str(sample.SampleID))
            payload_dict = {
                "RunName": run_name,
                "SampleID": sample.SampleID,
                "SiteName": sample.SiteName,
            }
            payload_list += [payload_dict]
            qr_image = generate_qr_code_from_string("json:" + json.dumps(payload_dict))
            HilltopHost.LogInfo(json.dumps(payload_dict))
            image_list += [qr_image]

        create_printable_a4_page(
            qr_images=image_list,
            data_dicts=payload_list,
            output_filename=f"{file_prefix}_qr_sheet"
        )

        create_printable_label_document(
            qr_images=image_list,
            data_dicts=payload_list,
            output_filename=f"{file_prefix}_qr_labels",
            dimensions=(62, 29),
            multiples=10,
        )


        response = HilltopHost.PreregistrationResult()

        return response
