
import win32com.client
import os
import cv2
from glob import glob
from image_converter import convert_to_bytes


def hide_layers(layers):
    for index in range(layers.Count):
        layer = layers[index]
        layer.visible = False


def convert_psd_as_dict(name: str, psd_files: list, export_path: str):
    psApp = win32com.client.Dispatch("Photoshop.Application")

    if isinstance(psd_files, str):
        psd_files = [psd_files]

    byte_data = {}
    for psd_file in psd_files:
        psApp.Open(psd_file)
        doc = psApp.Application.ActiveDocument

        layers = doc.layers

        output_path = os.path.join(export_path, name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
        options.Format = 13   # PNG

        for index in range(layers.Count):
            hide_layers(layers)
            layer = layers[index]
            layer.visible = True

            output_name = os.path.join(output_path, f'{layer.Name}.png')
            doc.Export(ExportIn=output_name, ExportAs=2, Options=options)
            byte_data[layer.Name] = convert_to_bytes(output_name)
            print(output_name)

    with open(os.path.join(output_path, f'fb_{name}.py'), 'w') as file_w:
        file_w.write(f'"""Auto Generated Data File corresponding to PSD {os.path.basename(psd_file)}."""\n\n')
        file_w.write('import framebuf\n')
        file_w.write('from framebuf_ex import FrameBufferEx\n\n\n')
        file_w.write(f'{name.upper()} = {{\n')
        for key, value in byte_data.items():
            file_w.write(f'    "{key}": {value},\n')
        file_w.write('}\n')


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    export_path = os.path.join(current_path, "export")
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    convert_psd_as_dict("numbers", os.path.join(current_path, "psd", "numbers.psd"), export_path)
    convert_psd_as_dict("top_icons", os.path.join(current_path, "psd", "top_icons.psd"), export_path)
    convert_psd_as_dict("vane", os.path.join(current_path, "psd", "vane.psd"), export_path)
    convert_psd_as_dict("fan", os.path.join(current_path, "psd", "fan.psd"), export_path)
    convert_psd_as_dict(
        "bottom_icons",
        [
            os.path.join(current_path, "psd", "auto.psd"),
            os.path.join(current_path, "psd", "degrees.psd"),
            os.path.join(current_path, "psd", "low_battery.psd"),
            os.path.join(current_path, "psd", "mini_Fan.psd"),
            os.path.join(current_path, "psd", "quiet.psd"),
            os.path.join(current_path, "psd", "thermometer.psd")
        ],
        export_path)


if __name__ == '__main__':
    main()