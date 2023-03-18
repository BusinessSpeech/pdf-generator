from configparser import ConfigParser

bs_config = ConfigParser()
bs_config.read('configs/bs_config.txt')

sales_config = ConfigParser()
sales_config.read('configs/sales_config.txt')


def select_config(template):
    if template == 'Business Speech':
        return bs_config
    elif template == 'TheSales':
        return sales_config
    return None
