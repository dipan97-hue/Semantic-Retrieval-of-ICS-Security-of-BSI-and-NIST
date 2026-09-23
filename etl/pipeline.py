from etl.bsi_extract import extract_bsi_chunks
from etl.nist_extract import extract_nist_chunks  
from etl.iso_extract import extract_iso_chunks  
from etl.save_json import save_json


def run_etl():

    # bsi_data = extract_bsi_chunks(r'D:\exercises\Thesis\Data\bsi-standard-2001.pdf')

    # nist_data = extract_nist_chunks(r'D:\exercises\Thesis\Data\NIST.SP.800-82r3.pdf')
    # nist_data = extract_nist_chunks(r'D:\exercises\Thesis\Data\NIST.SP.800-82r3.pdf')
    #json_data_bsi = save_json(bsi_data, r'D:\exercises\Thesis\Json Files\bsi_standard.json')
    
    #json_data_nist = save_json(nist_data, r'D:\exercises\Thesis\Json Files\Nist_Standard.json')    
    
    
    #print(f"BSI chunks extracted: {len(bsi_data)}")
    #print(f"NIST chunks extracted: {len(nist_data)}")
    
    #print(f"ISO chunks extracted: {len(iso_data)}")
    iso_data = extract_iso_chunks(r'D:\exercises\Thesis\Data\ISO_SAE_21434_2021.pdf')
    json_data_iso = save_json(iso_data, r'D:\exercises\Thesis\Json Files\ISO_SAE_21434_2021.json')

    