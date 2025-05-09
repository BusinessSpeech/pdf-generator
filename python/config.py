from configparser import ConfigParser

bs_config = ConfigParser()
bs_config.read('configs/bs_config.txt')

sales_config = ConfigParser()
sales_config.read('configs/sales_config.txt')

sct_config = ConfigParser()
sct_config.read('configs/sct_config.txt')

nn_config = ConfigParser()
nn_config.read('configs/nn_config.txt')

bs_sales_config = ConfigParser()
bs_sales_config.read('configs/bs_sales_config.txt')

sales_sct_config = ConfigParser()
sales_sct_config.read('configs/sales_sct_config.txt')

bs_en_config = ConfigParser()
bs_en_config.read('configs/bs_eng_config.txt')


def select_config(template):
    if template == 'Business Speech':
        return bs_config
    elif template == 'TheSales':
        return sales_config
    elif template == 'SCT':
        return sct_config
    elif template == 'NN':
        return nn_config
    elif template == 'BS_Sales':
        return bs_sales_config
    elif template == 'Sales_SCT':
        return sales_sct_config
    elif template == 'Business Speech EN':
        return bs_en_config
    return None
