from datetime import datetime

def create_output_txt(text_str, filename, save_locaiton = None):
    date_now = datetime.now()
    date_str = date_now.strftime("%d%m%Y-%H%M%S")
    full_out_name = f'{filename}_{date_str}'
    
    out_file = open(f'outputs/{full_out_name}.txt', 'w+')
    out_file.write(text_str)
    out_file.close()