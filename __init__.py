import HilltopHost
from .sampler_qr_generator import create_printable_a4_page, generate_qr_code_from_string, create_printable_label_document
import json

class QRGenerator:

    def health_check(self):
        return "Ok"

    def send_preregistration_request(self, preregistration_data):
        HilltopHost.LogInfo("You clicked the Notify Lab button.")
        HilltopHost.LogInfo("These are the samples:")

        file = open("D:/HilltopDev/testlog.txt", "w")
        file.write("Hi there.\n")

        run_name = preregistration_data.Run.RunName

        file.write(f"Samples in the {run_name} run.\n")
    
        payload_list = []
        image_list = []
    
        for sample in preregistration_data.Samples:
            HilltopHost.LogInfo(str(sample.SampleID))
            file.write(f"SampleID={sample.SampleID}, SiteName={sample.SiteName}\n")
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
            output_filename="a4_test_sheet"
        )

        create_printable_label_document(
            qr_images=image_list,
            data_dicts=payload_list,
            output_filename="label_test_sheet",
            dimensions=(62, 29),
            multiples=10,
        )

        file.close()

        response = HilltopHost.PreregistrationResult()

        return response
