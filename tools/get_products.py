"""This script provides functions to retrieve a list of products for a given TopScore site"""

import pathlib, subprocess

# CHANGE THIS
CONFIG_FILENAME = "/home/kevin/bulblytics/pada/config.yml"

def parse_config(config_filename: str) -> dict:
    """Reads configuration file, parses it, and returns a dictionary of string variables

    Args:
        config_filename (str): path to configuration file with parameters for accessing TopScore API

    Returns:
        list: a dictionary of configuration parameters
    """
    config_file = open(config_filename, 'r')
    return {
        'auth_url' : config_file.readline().rstrip(),
        'client_id' : config_file.readline().rstrip(),
        'client_secret' : config_file.readline().rstrip(),
        'username' : config_file.readline().rstrip(),
        'password' : config_file.readline().rstrip(),
    }

def get_products(config: dict) -> list:
    """Retrieves list of products

    Args:
        config (dict): a dictionary of configuration parameters for connecting to TopScore's API

    Returns:
        list: a list of strings representing TopScore product names
    """
    # Change in future to use wrapper function
    api_script = str(pathlib.Path(__file__).parent.absolute()) + "/tools/topscore_api.sh"
    subprocess.check_output(' '.join([api_script, config['auth_url'], config['client_id'],
                                      config['client_secret'], config['username'], config['password'],
                                      'products?site_list_scope=network&per_page=1']), shell = True)

config = parse_config(CONFIG_FILENAME)

system(paste0("bash /home/kevin/dev/pada/topscore_api.sh 'products?site_list_scope=network&per_page=1' > ", productsHeaderFile))
productsData <- fromJSON(productsHeaderFile)
numproducts <- productsData$count
numPages <- ceiling(numproducts / 100)
products <- do.call(rbind, lapply(seq(1,numPages), function(page) {
  json <- paste0("/home/kevin/dev/pada/products/productsPage",page,".json")
  system(paste0("bash /home/kevin/dev/pada/topscore_api.sh 'products?site_list_scope=network&fields=ProductVariations&per_page=100&page=",page,"' > ", json))
  result <- fromJSON(json)$result
  if(!is.data.frame(result$ProductVariations[[1]])) {
    return(result %>%
             rename(product=name,
                    product_id=id) %>%
             mutate(parent_product_id=product_id) %>%
             select(product_id, parent_product_id, product, cost))
  }
  standaloneProductsFilter <- sapply(result$ProductVariations, function(dfrow) { return(nrow(dfrow)==0)})
  standaloneProducts <- result[standaloneProductsFilter, ] %>%
    rename(product=name,
           product_id=id) %>%
    mutate(parent_product_id=product_id) %>%
    select(product_id, parent_product_id, product, cost)
  if(any(!standaloneProductsFilter)) {
    familyProducts <- do.call(rbind, lapply(result$ProductVariations[!standaloneProductsFilter], function(productFamilyDf) {
      return(productFamilyDf %>%
               rename(product=name,
                      product_id=id) %>%
               mutate(parent_product_id=family_product_id) %>%
               select(product_id, parent_product_id, product, cost))
    }))
    return(rbind(standaloneProducts, familyProducts))
  }
  return(standaloneProducts)
  }))

products$year <- sapply(products$product, get_year)

def write_products(products_filename: str):
    """Calls get_products and writes result to output file

    Args:
        products_filename (str): The path to the output file for the product names
    """

write.csv(products, "/home/kevin/dev/pada/products/products.csv", row.names = FALSE)