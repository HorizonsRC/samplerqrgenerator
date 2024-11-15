import HilltopHost
from .sampler_qr_generator import (
    create_printable_a4_page,
    generate_qr_code_from_string,
    create_printable_label_document,
)
import json
import os


class QRGenerator:

    def health_check(self):
        return "Ok"

    def send_preregistration_request(self, preregistration_data):
        HilltopHost.PostMessage("====================")
        HilltopHost.PostMessage("You clicked the Notify Lab button.")
        HilltopHost.PostMessage(
            "In addition to notifying the lab, this button also generates QR labels."
        )
        HilltopHost.PostMessage("--------------------")

        run_name = preregistration_data.Run.RunName
        tech_name = preregistration_data.Run.TechnicianFirstName

        HilltopHost.PostMessage(
            f"Generating QR codes for run {run_name} which was set up by {tech_name}."
        )
        HilltopHost.PostMessage("--------------------")
        output_dir = preregistration_data.GetSectionInfo("Sampler")["LabelOutputDir"]

        file_prefix = os.path.join(output_dir, f"{run_name}_[{tech_name}]")

        payload_list = []
        image_list = []

        for sample in preregistration_data.Samples:
            HilltopHost.PostMessage(
                f" - Generating QR code for sample {sample.SampleID}"
                f" at {sample.SiteName}"
            )
            payload_dict = {
                "RunName": run_name,
                "SampleID": sample.SampleID,
                "SiteName": sample.SiteName,
            }
            payload_list += [payload_dict]
            qr_image = generate_qr_code_from_string("json:" + json.dumps(payload_dict))
            image_list += [qr_image]

        HilltopHost.PostMessage("--------------------")
        HilltopHost.PostMessage("Saving QR codes to files:")
        HilltopHost.PostMessage(f" - {file_prefix}_qr_a4_sheet.pdf")
        HilltopHost.PostMessage(f" - {file_prefix}_qr_labels.pdf")
        HilltopHost.PostMessage("--------------------")

        create_printable_a4_page(
            qr_images=image_list,
            data_dicts=payload_list,
            output_filename=f"{file_prefix}_qr_a4_sheet",
        )

        create_printable_label_document(
            qr_images=image_list,
            data_dicts=payload_list,
            output_filename=f"{file_prefix}_qr_labels",
            dimensions=(62, 29),
            multiples=2,
        )

        HilltopHost.PostMessage(f"Done! The QR codes have been saved to {output_dir}.")
        HilltopHost.PostMessage("You may now close this dialog.")

        HilltopHost.PostMessage("====================")
        response = HilltopHost.PreregistrationResult()

        return response
