import os
import pdfplumber

# Directorios de entrada y salida
input_directory = "./data/pdfs/"
output_directory = "./data/md/"

# Crear el directorio de salida si no existe
os.makedirs(output_directory, exist_ok=True)


def convert_pdf_to_md():
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(".pdf"):  # Verificar extensión PDF
            input_path = os.path.join(input_directory, filename)
            output_filename = os.path.splitext(filename)[0] + ".md"
            output_path = os.path.join(output_directory, output_filename)

            try:
                # Leer el contenido del PDF
                with pdfplumber.open(input_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += (
                            page.extract_text() + "\n\n"
                        )  # Agregar salto de línea entre páginas

                # Guardar el texto extraído en un archivo Markdown
                with open(output_path, "w", encoding="utf-8") as md_file:
                    md_file.write(text)

                print(f"Archivo convertido y guardado: {output_path}")

            except Exception as e:
                # Manejo de errores
                print(f"Error al procesar {filename}: {e}")


if __name__ == "__main__":
    convert_pdf_to_md()
