'''
Returns total price paid for individual rentals

Logging level set based on input argument, defaults to no logging.
Four logging levels are use: OFF, ERROR, WARNING, DEBUG
'''


import argparse
import json
import datetime
import math
import logging
from functools import wraps

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
LOG_LEVEL = {'0': 'OFF', '1': 'ERROR', '2': 'WARNING', '3': 'DEBUG'}

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def decorator(func, logvalue):

    @wraps(func)
    def wrapper_decorator(*args, **kwargs):

        if logvalue:
            LOGGER.disabled = False
            LOGGER.setLevel("DEBUG")

        try:
            LOGGER.debug(f'Executing {func.__name__} function.')
            value = func(*args, **kwargs)
        except Exception as file_error:
            LOGGER.error(f"Input file error: {type(file_error).__name__}")
            exit(1)
        LOGGER.disabled = True
        return value
    return wrapper_decorator


def parse_cmd_arguments():
    """
    Usage: prog -i,--input INFILE -o,--output OUTFILE -d,-debug LEVEL

    Arguments:
        INFILE  filename for input data file
        OUTFILE filename for output data file
        LEVEL   debug level

    Options:
        -i, --input options for input file
        -o, --output options for output file
        -d, -debug options for debug level
    """

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-log', help='include log to activate logging', required=False, action='store_true')

    return parser.parse_args()

def load_rentals_file(filename):
    """ Read json input file and create data structure """

    with open(filename, 'r') as file:

        newdata = json.load(file)

    return newdata

def calculate_additional_fields(data):
    """ Calculate data using input data """

    logging.debug('Calculating new data.')
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_start > rental_end:
                logging.warning("Rental start date is after rental end date.")
                raise ValueError
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.error(f"Bad data in file. Skipping data: {value}")
            continue
        except KeyError:
            logging.error(f"Missing data in file. Skipping data: {value}")
            continue

    return data


def save_to_json(filename, data):
    """ Save new calculations to file """

    logging.debug(f'Writing calculated data to file: {filename}')
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError as file_error:
        logging.error(f"Failed to open output file: {type(file_error).__name__}")


if __name__ == "__main__":

    DATA = {}
    LOGGER.disabled = True
    ARGS = parse_cmd_arguments()

    load_rentals_file = decorator(load_rentals_file, ARGS.log)
    DATA = load_rentals_file(ARGS.input)

    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
