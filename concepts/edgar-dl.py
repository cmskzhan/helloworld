from edgar import Edgar
edgar = Edgar()
possible_companies = edgar.find_company_name("microsoft corp")
print(possible_companies)
# edgar.download_index("/home/sroot/kaizha/temp/", 2020, skip_all_present_except_last=Tr
print(edgar.get_company_name_by_cik("0000789019"))