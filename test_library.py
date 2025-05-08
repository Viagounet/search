import os
from web.scrap import read_url
from web.search import search
from web.utils import pdf_stream, pdf_to_base64_images

pdf = pdf_stream(
    "https://www.groupe-sncf.com/medias-publics/2025-04/Fitch-rating-sncf-group-april-2025.pdf"
)
images = pdf_to_base64_images(pdf.read())

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [{"type": "input_text", "text": "De quoi parle ce document?"}]
            + [
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image}",
                }
                for image in images[:10]
            ],
        }
    ],
)

print(response.output_text)
