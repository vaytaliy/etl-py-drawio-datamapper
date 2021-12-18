import sys
import getopt

from utils import excel_reader, config_reader, drawio_csv_builder, file_reader


def main(argv):
    try:
        # c- full path to config, e- full path to excel file (opts - option/value pairs)
        opts = getopt.getopt(argv, "c:e:")
        config, excel_path = process_opts(opts)
        prep_diagram_text(config, excel_path)
    except getopt.GetoptError:
        print("something went wrong, check passed arguments")
        sys.exit(2)


"""
processing of user's arguments logic
"""
def process_opts(opts):
    excel_path = get_option_arg('-e', opts)

    if (excel_path is None):
        print("path to excel file must be provided")
        sys.exit(2)

    config_path = get_option_arg('-c', opts)
    config = None

    if (config_path is not None):
        config = config_reader.read_config(config_path)
    else:
        config = config_reader.read_config('config.ini')
    return (config, excel_path)


"""
creates finalized text file 
with csv format needed for pasting to draw.io
"""
def prep_diagram_text(config, excel_path):
    # build csv relying on config data and data in excel
    mapping_data_dict, target_table_name = excel_reader.get_mapping_sheet_data(config, excel_path)
    csv_result = drawio_csv_builder.create_csv(mapping_data_dict, target_table_name)
    file_reader.create_output_txt(csv_result, 'test_mapping')

def get_option_arg(optionName, opts):
    for opt, arg in opts[0]:
        if opt == optionName:
            return arg
    return None

if __name__ == "__main__":
    main(sys.argv[1:])  # start from 1, end to length
