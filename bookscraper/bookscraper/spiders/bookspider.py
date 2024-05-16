import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        
        """
        Parse function for the main page.

        Parameters:
        - response: The response object containing the HTML of the main page.

        Processing Steps:
        - Extracts the URLs of individual books from the main page.
        - For each book URL, constructs the absolute URL.
        - Initiates a new request for each book URL, calling the parse_book_page function for detailed scraping.
        - Determines the URL of the next page and follows it if there are more pages.

        Returns:
        - Yields requests for individual book pages.
        """

        books = response.css("article.product_pod")

        #looping through the books variable
        for book in books:
        
            #fetching the individual book url
            relative_url = book.css('h3 a').attrib['href']

            #condition for when the url does not contain 'catalogue/'
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url

            yield scrapy.Request(book_url, callback = self.parse_book_page)

        #declaring the next page variable    
        next_page = response.css('li.next a ::attr(href)').get()

        #condition for no remaining pages
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_book_page(self, response):

        """
        Parse function for individual book pages.

        Parameters:
        - response: The response object containing the HTML of an individual book page.

        Processing Steps:
        - Extracts various details about the book, including title, URL, UPC, product type, prices, tax, availability, number of reviews, star rating, category, description, and price.
        - Utilizes CSS and XPath selectors to locate and extract specific elements from the HTML structure.

        Returns:
        - Yields a dictionary containing the extracted information for each book.
        """

        #defining the book variable for the main product page class
        book = response.css("div.product_main")[0]

        #defining the table row for product information tag
        table_rows = response.css("table tr")

        #instantiating the book_item
        book_item = BookItem()

        #items
        book_item['url'] = response.url
        book_item['title'] = book.css("h1 ::text").get()
        book_item['upc'] = table_rows[0].css("td ::text").get()
        book_item['product_type'] = table_rows[1].css("td ::text").get()
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get()
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get()
        book_item['tax'] = table_rows[4].css("td ::text").get()
        book_item['availability'] = table_rows[5].css("td ::text").get()
        book_item['num_reviews'] = table_rows[6].css("td ::text").get()
        book_item['stars'] = book.css("p.star-rating").attrib['class']
        book_item['category'] = book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['description'] = book.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['price'] = book.css('p.price_color ::text').get()
        
        yield book_item