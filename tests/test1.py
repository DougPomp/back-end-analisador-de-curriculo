

import pymupdf

# Abrindo o arquivo pdf 
pdf = pymupdf.open(r'C:\Users\peter\Documents\MeusProjetos\back-end-analisador-de-curriculo\tests\curriculo_test.pdf')

for item in range(pdf.page_count):

    pagina = pdf.load_page(item)
