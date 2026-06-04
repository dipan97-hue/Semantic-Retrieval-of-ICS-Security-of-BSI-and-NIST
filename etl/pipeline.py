from etl.bsi_extract import extract_bsi_chunks
from etl.nist_extract import extract_nist_chunks    
from etl.save_json import save_json


def run_etl():

    bsi_data = extract_bsi_chunks(r'D:\exercises\Thesis\Data\bsi-standard-2001.pdf')

    nist_data = extract_nist_chunks(r'D:\exercises\Thesis\Data\NIST.SP.800-82r3.pdf')

    json_data_bsi = save_json(bsi_data, r'D:\exercises\Thesis\Json Files\bsi_standard.json')

    json_data_nist = save_json(nist_data, r'D:\exercises\Thesis\Json Files\Nist_Standard.json')    

    
    print(f"BSI chunks extracted: {len(bsi_data)}")
    print(f"NIST chunks extracted: {len(nist_data)}")