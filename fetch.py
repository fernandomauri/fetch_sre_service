import requests
import yaml

import logging
import math
import os
import time


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def parse_file(yml_file):
    '''
    Take as input a YML file and parse it for the endpoint data we need.
    The most important information we need here is the HTTP method being used,
    the endpoint URL itself, any necessary headers, and the request body if
    we're using a POST request.
    '''
    with open(yml_file, 'r') as file_to_parse:
        file_data = yaml.safe_load(file_to_parse)

    return file_data


def get_domain(url):
    '''
    We will want to separate availability percentage based on the domains and not the individual endpoints.
    '''
    url = url.strip()
    if url.startswith('https://'):
        url = url.replace('https://', '')
    slash_index = url.index('/')
    domain = url[:slash_index]
    return domain


def fetch_endpoint_health(url, method, headers=None, body=None):
    '''
    Keeps track of each endpoint's health status.
    '''
    start_time = time.time() * 1000
    try:
        if method == 'GET':
            response = requests.get(url=url, headers=headers, data=body)
        elif method == 'POST':
            response = requests.post(url=url, headers=headers, data=body)
    except Exception as e:
        logger.error(f'Unable to make HTTP request to {url}. Error => {e}.')
        raise
    else:
        end_time = time.time() * 1000
        latency = end_time - start_time
        logger.debug(f'Latency for url {url}: {latency} ms.')
        status = response.status_code
        logger.debug('Status code:', status)
        if str(status).startswith('2') and latency < 500:
            health = "UP"
        if latency > 500:
            health = "DOWN"
        if not str(status).startswith('2'):
            health = "DOWN"
        logger.debug(f"Endpoint health: {health}")

    return health


def request_data(file_data):
    '''
    This function takes our parsed YML file data and gather data from each HTTP request in the file.
    We will want to keep track of the amount of successful and unsuccessful requests for each domain, 
    as well as the amount of requests made to each domain.
    '''
    domains = list()
    health_states = list()

    
    for endpoint in file_data:
        method = endpoint['method'] if 'method' in endpoint else 'GET'
        headers = endpoint['headers'] if 'headers' in endpoint else None
        body = endpoint['body'] if 'body' in endpoint else None
        url = endpoint['url']
        domain = get_domain(url)
        endpoint_health = fetch_endpoint_health(url=url, method=method, headers=headers, body=body)
        domains.append(domain.strip())
        health_states.append(endpoint_health.strip())

    endpoint_requests = list(zip(domains, health_states))
    domain_dict = dict()

    for endpoint, health in endpoint_requests:
        if endpoint not in domain_dict.keys():
            domain_dict[endpoint] = dict()
            domain_dict[endpoint]['up_count'] = 0
            domain_dict[endpoint]['down_count'] = 0
            if health == "UP":
                domain_dict[endpoint]['up_count'] = 1
            elif health == "DOWN":
                domain_dict[endpoint]['down_count'] = 1
            domain_dict[endpoint]['request_count'] = 1
        elif endpoint in domain_dict.keys():
            if health == "UP":
                domain_dict[endpoint]['up_count'] += 1
            elif health == "DOWN":
                domain_dict[endpoint]['down_count'] += 1
            domain_dict[endpoint]['request_count'] += 1

    return domain_dict


def calculate_availability_percentage(requests_data):
    '''
    Takes the data we returned from the request_data() function and calculates the availability percentage.
    '''
    availability_rate = dict()
    for domain in requests_data:
        up_count = requests_data[domain]['up_count']
        request_count = requests_data[domain]['request_count']
        percent = math.ceil(100 * (up_count / request_count))
        availability_rate[domain] = percent
        print(f'{domain} has {percent}% availability percentage')


def aggregate_data(domains_data, availability_data):
    '''
    Update our values for the domain_dict returned from requests_data() function.
    '''
    for key in domains_data:
        if key in availability_data:
            availability_data[key]['up_count'] = availability_data[key]['up_count'] + domains_data[key]['up_count']
            availability_data[key]['down_count'] = availability_data[key]['down_count'] + domains_data[key]['down_count']
            availability_data[key]['request_count'] = availability_data[key]['request_count'] + domains_data[key]['request_count']
        elif key not in availability_data:
            availability_data[key] = {'up_count': domains_data[key]['up_count'], 'down_count': domains_data[key]['down_count'], 'request_count': domains_data[key]['request_count']}
    calculate_availability_percentage(availability_data)

    return availability_data


def main():
    '''
    The user inputs the filepath here and the YML file data gets processed.
    '''
    file_path = str(input('Enter filepath for YML file (For example: sample_file.yml) =>  '))
    if file_path == '':
        file_path = '/'

    # Check to see if the file exists, if not prompt for a valid filepath.
    while file_path:
        if os.path.isfile(file_path):
            break
        else:
            file_path = str(input('Filepath doesn\'t exist. Enter filepath for YML file (For example: sample_file.yml) =>  '))
            if file_path == '':
                file_path = '/'

    # Takes the input file and parses it.
    file_data = parse_file(file_path)
    # Retrieves information for each domain listed in file_data. Contains up_count, down_count, and request_count.
    domains_data = request_data(file_data)
    # Makes a dictionary to keep track of future changes to availability data.
    availability_data = dict()

    # Keep running the program until the user quits with KeyboardInterrupt.
    while True:
        try:
            updated_values = aggregate_data(domains_data, availability_data)
            availability_data.update(updated_values)
            time.sleep(15)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
     main()
