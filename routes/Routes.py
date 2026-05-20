
class Routes:
    BASE_URL="https://fakestoreapi.com" #base url

    #product
    GET_ALL_PRODUCTS = "/products" #endpoints
    GET_PRODUCT_BY_ID = "/products/{id}"
    GET_PRODUCTS_WITH_LIMIT = "/products?limit={limit}"
    GET_PRODUCTS_SORTED = "/products?sort={order}"
    GET_ALL_CATEGORIES = "/products/categories"
    GET_PRODUCTS_BY_CATEGORY = "/products/category/{category}"
    CREATE_PRODUCT = "/products"
    UPDATE_PRODUCT = "/products/{id}"
    DELETE_PRODUCT = "/products/{id}"
    #cart

    #Auth
