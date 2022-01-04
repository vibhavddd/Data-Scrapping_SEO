# Data-Scrapping_SEO
Search Engine Optimization
SEO is a technique of using tools to ensure that your website gets a high ranking in the Google Search Engine Results Page (SERP), using data scrapping created a code that takes the input query and  such as “amazon” and using google autocomplete API completes that query and tells us the relevance and the most relevant key that are necessary and needed to optimize the engine,
Libraries used 
Urllib
Json 
Pandaas 
Numpy 
Requests_html 
Code consists of various functions and each of which has its role 
Get_url()
This function creates an HTML_Session and helps us get the relevant information from the provided link by giving back the response in JSON format. Used Try and Except to handle the status_codes other than 200 
Get_result()
This function will take the query and create the desired Url, “urllib.parse.quote_plus(query)” (replace spaces with plus signs, as required for quoting HTML form values when building up a query string to go into a URL.). Furthermore, it converts the response in readable format so that the python compiler can understand it 
query_expansion(query)
this function is used to expand our query so that one would be able to get more keywords that are relevant so that google autocomplete API would show more suggested options, and the client would be able to get more Keywords and their relevance point which would depend on the location recent search and various other parameters.
Finally, a wrapped function was creted.
 
  ![SEO 3](https://user-images.githubusercontent.com/63113653/148100527-a0ec7a5b-86a6-45c4-a5a8-5f1e7525ac1a.png)
  
  ![SEO 2](https://user-images.githubusercontent.com/63113653/148100565-298f8147-6f2d-4f55-b047-f1048372f04b.png)
  
![SEO 4](https://user-images.githubusercontent.com/63113653/148100581-4ac8333a-e73f-4756-a0b0-8918fb370553.png)




 

 

 
