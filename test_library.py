import asyncio
from web.scrap import read_url
from web.search import search
from web.utils import pdf_stream

pdf = pdf_stream("https://www.groupe-sncf.com/medias-publics/2025-04/Fitch-rating-sncf-group-april-2025.pdf")
print(pdf)