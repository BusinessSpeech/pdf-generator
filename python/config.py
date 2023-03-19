from configparser import ConfigParser

bs_config = ConfigParser()
bs_config.read('configs/bs_config.txt')

sales_config = ConfigParser()
sales_config.read('configs/sales_config.txt')

sct_config = ConfigParser()
sct_config.read('configs/sct_config.txt')


def select_config(template):
    if template == 'Business Speech':
        return bs_config
    elif template == 'TheSales':
        return sales_config
    elif template == 'SCT':
        return sct_config
    return None
