from PIL import Image
import win32com.client
import json
import fitz
import os
import time

def apply_changes(sheet, changes):
    for key, value in changes.items():
        if ":" in key:
            # Plage détectée
            cells = sheet.Range(key).Cells
            for i in range(1, cells.Count + 1):
                cells.Item(i).Value = value
        else:
            # Cellule unique
            sheet.Range(key).Value = value

def export_excel_to_pdf(excel_path, output_folder, scenario_json):
    os.makedirs(output_folder, exist_ok=True)
    # Chargement des scénarios
    with open(scenario_json, "r") as f:
        scenarios = json.load(f)

    # Lancement d'Excel
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    # Ouverture du fichier Excel
    workbook = excel.Workbooks.Open(excel_path)
    sheet = workbook.Sheets(1)  # Modifier ici si tu veux travailler sur une autre feuille

    # Paramètres de mise en page
    sheet.PageSetup.Orientation = 2  # Paysage
    sheet.PageSetup.PaperSize = 8    # A3
    sheet.PageSetup.Zoom = False
    sheet.PageSetup.FitToPagesWide = 1
    sheet.PageSetup.FitToPagesTall = 1

    for scenario in scenarios:
        name = scenario["name"]
        changes = scenario["changes"]

        apply_changes(sheet, changes)

        # Recalculer les formules et mises en forme conditionnelles
        workbook.RefreshAll()
        excel.CalculateFull()

        
        # Définir le chemin de sortie
        pdf_path = os.path.join(output_folder, f"{name}.pdf")
        print(f"Exporting: {pdf_path}")

        # Exporter en PDF
        workbook.ExportAsFixedFormat(0, pdf_path)

    # Fermer sans enregistrer
    workbook.Close(SaveChanges=False)
    excel.Quit()

def crop_pdfs_in_folder(input_folder, output_folder, crop_rect=None):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            doc = fitz.open(input_path)

            for page in doc:
                # Crop rectangle : (x0, y0, x1, y1)
                if crop_rect:
                    page.set_cropbox(fitz.Rect(crop_rect))
                # Sinon, ne rien faire (mais tu peux lister les dimensions ici)

            doc.save(output_path)
            doc.close()
            print(f"Cropped: {output_path}")


def pdfs_to_images(input_folder, overlay_file, output_folder=None, scale=6.0, resize_factor=0.5, overlay_position=(0, 0), image_format="png"):
    if output_folder is None:
        output_folder = input_folder + "_final"
    os.makedirs(output_folder, exist_ok=True)

    overlay = Image.open(overlay_file).convert("RGBA")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            doc = fitz.open(pdf_path)
            base_name = os.path.splitext(filename)[0]

            for page_num, page in enumerate(doc):
                # Rendu haute résolution sans alpha
                matrix = fitz.Matrix(scale, scale)
                pix = page.get_pixmap(matrix=matrix, alpha=False)

                # Convertir en image PIL
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Redimensionner
                new_size = (int(img.width * resize_factor), int(img.height * resize_factor))
                img = img.resize(new_size, Image.LANCZOS)

                img = img.convert("RGBA")
                overlay_resized = overlay.resize(img.size, Image.LANCZOS)

                # Fusion alpha correcte
                combined = Image.alpha_composite(img, overlay_resized)

                # Fusion avec overlay
                #img = img.convert("RGBA")
                #overlay_resized = overlay.resize(img.size) if overlay.size != img.size else overlay
                #img.paste(overlay_resized, overlay_position, overlay_resized)

                # Sauvegarder
                output_path = os.path.join(output_folder, f"{base_name}.{image_format}")
                combined .save(output_path)
                break

            doc.close()
            print(f"✔ {filename} → images fusionnées avec overlay")
            
            


if __name__ == "__main__":
    local_folder = os.path.dirname(os.path.realpath(__file__))
    os.path.join(local_folder, "hotkeymonitor.ahk")
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    temp_folder = os.path.join(local_folder, "temp") 
    temp2_folder = os.path.join(local_folder, "temp_2") 
    output_folder = os.path.join(os.path.dirname(local_folder), "app", "Layers") 
    excel_file = os.path.join(local_folder, "KeybordLayout.xlsx") 
    scenario_file = os.path.join(local_folder, "config.json") 
    overlay_file = os.path.join(local_folder, "overlay.png") 

    print("Exporting Excel Layers")
    export_excel_to_pdf(excel_file, temp_folder, scenario_file)
    print("Cropping Keybord Area")
    crop_pdfs_in_folder(temp_folder, temp2_folder, (51, 55, 970, 370))
    print("Creating Images")
    pdfs_to_images(temp2_folder, overlay_file, output_folder, scale=6.0, resize_factor=0.4644, overlay_position=(0, 0)) #2560 = 0.4644    3840 = 0.6966
    print("Task Done")