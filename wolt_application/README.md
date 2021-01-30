# Wolt Wummer 2021 Internships Backend assigment
## Created by Daniel Mottershead

I wrote my code in Python using a package called aiohttp, that allows developers to create asynchronous clients and servers in python.

Running the code is very straight forward. All you need to do is navigate to the folder and run the program app.py from the commandline.

e.g. Linux: `$ python3 app.py`

After this open up your browser and type in the url: *http://localhost:8080/discovery?lat=x&lon=y*
where x and y are the latitude and longitude coordinates where the user supposedly is.

I'm sorry that there are no unit tests included, but below I have listed x and y values that should prove that the application works as intended.

* (24.931684, 60.159661): Location of restaurant "Tomato Paste". This is the ideal case where there is 10 online restaurants in the area. The first restaurant based on distance is "Tomato Paste" because this is its location.
* (24.945411, 60.158344) Location of the restaurant "Heavenly Taco Palace". It is not open and as such is not on the list of closest restaurants.
* (5, 6) Random coordinates with no restaurants around.
* (Hello, World!) If the request parameters are not of type float or int the location defaults to (0,0). 

Thank you for reading and if any questions about my code arise I would be happy to answer them via my email: daniel.mottershead@aalto.fi

Any and all feedback on my code is greatly appreciated!
