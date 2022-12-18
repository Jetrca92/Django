# Wiki site project

As a part of a **CS50W** programm, I had to build a wiki webapp using Django framework and Markdown. 
I designed a Wikipedia-like online encyclopedia, which is a web application that allows users to browse, search, create, edit, and view random encyclopedia entries.

## The index page
The index page of the encyclopedia has been updated to include links to each entry page, rather than just a list of entry names. This allows users to click on any 
entry name to be taken directly to that entry page. The encyclopedia also includes a search feature, which allows users to type a query into a search box in the 
sidebar to search for an encyclopedia entry. If the query matches the name of an entry, the user is redirected to that entry's page. If the query does not match the 
name of an entry, the user is taken to a search results page that displays a list of all entries that have the query as a substring.

## The entry page 
The entry pageof the encyclopedia can be accessed by visiting the URL /wiki/TITLE, where TITLE is the title of an encyclopedia entry. 
The view function for this page gets the content of the entry by calling the appropriate util function, and renders a page that displays the content of the entry, along with the title of the page. If the requested entry does not exist, the user is presented with an error page indicating that the requested page was not found.



Users can also create new encyclopedia entries by clicking the "Create New Page" link in the sidebar, which takes them to a page with a form for creating a new entry. The form includes fields for the entry title and Markdown content, and a button to save the new entry. If an entry with the same title already exists, the user is presented with an error message. Otherwise, the new entry is saved to disk and the user is taken to the new entry's page.

On each entry page, there is a link that takes the user to a page where they can edit the entry's Markdown content. The textarea on this page is pre-populated with the existing content of the entry, and the user can click a button to save the changes made to the entry. Once the changes are saved, the user is redirected back to the entry's page.

The encyclopedia also includes a "Random Page" feature, which allows users to click a link in the sidebar to be taken to a random encyclopedia entry.

Finally, the encyclopedia converts any Markdown content in the entry files to HTML before displaying it to the user. This conversion is performed using the python-markdown2 library, which can be installed using the pip3 install markdown2 command. Alternatively, I implemented the conversion myself using regular expressions to match and replace the Markdown syntax with the corresponding HTML tags.

Overall, I believe I have successfully implemented all the required features for my Wiki encyclopedia, and it is now a fully functional web application.

## Index page

![Index page](active_listings.jpg)



## Create listing page

![Create listing page](create_listing.jpg)



## Entry page

![Entry page](entry_page.jpg)

I have completed the implementation of my Wiki encyclopedia, which is a web application that allows users to browse, search, create, edit, and view random encyclopedia entries.

The entry page of the encyclopedia can be accessed by visiting the URL /wiki/TITLE, where TITLE is the title of an encyclopedia entry. The view function for this page gets the content of the entry by calling the appropriate util function, and renders a page that displays the content of the entry, along with the title of the page. If the requested entry does not exist, the user is presented with an error page indicating that the requested page was not found.

The index page of the encyclopedia has been updated to include links to each entry page, rather than just a list of entry names. This allows users to click on any entry name to be taken directly to that entry page.

The encyclopedia also includes a search feature, which allows users to type a query into a search box in the sidebar to search for an encyclopedia entry. If the query matches the name of an entry, the user is redirected to that entry's page. If the query does not match the name of an entry, the user is taken to a search results page that displays a list of all entries that have the query as a substring.

Users can also create new encyclopedia entries by clicking the "Create New Page" link in the sidebar, which takes them to a page with a form for creating a new entry. The form includes fields for the entry title and Markdown content, and a button to save the new entry. If an entry with the same title already exists, the user is presented with an error message. Otherwise, the new entry is saved to disk and the user is taken to the new entry's page.

On each entry page, there is a link that takes the user to a page where they can edit the entry's Markdown content. The textarea on this page is pre-populated with the existing content of the entry, and the user can click a button to save the changes made to the entry. Once the changes are saved, the user is redirected back to the entry's page.

The encyclopedia also includes a "Random Page" feature, which allows users to click a link in the sidebar to be taken to a random encyclopedia entry.

Finally, the encyclopedia converts any Markdown content in the entry files to HTML before displaying it to the user. This conversion is performed using the python-markdown2 library, which can be installed using the pip3 install markdown2 command. Alternatively, I implemented the conversion myself using regular expressions to match and replace the Markdown syntax with the corresponding HTML tags.

Overall, I believe I have successfully implemented all the required features for my Wiki encyclopedia, and it is now a fully functional web application.
