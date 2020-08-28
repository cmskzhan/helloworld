from secedgar.utils import get_cik_map
from secedgar.filings import Filing, FilingType
print(list(get_cik_map().items())[:5])
my_filings = Filing(cik_lookup='aapl',
                    filing_type=FilingType.FILING_10Q,
                    count=1)
my_filings.save('/home/sroot/kaizha/temp')