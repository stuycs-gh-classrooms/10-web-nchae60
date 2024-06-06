#! /usr/bin/python
print('Content-type: text/html\n')
import cgitb #
#cgitb.enable()
import matplotlib.pyplot as plt
import io
import base64
import cgi
import math
import pprint

def make_image_element():
    #create buffer to store the graph image
    buffer = io.BytesIO()
    #save graph image to buffer
    plt.savefig(buffer, format='png')
    #reset buffer to the start of the image data
    buffer.seek(0)
    #encode the image data in buffer to base64, thench
    #translate that to utf-8
    image_code = base64.b64encode(buffer.read()).decode('utf-8')
    src = "data:image/png;base64,"
    src+= image_code
    html = '<img src="' + src
    html+= '">'
    return html

def returnpopulation(country, year, request):
    data = open('popdata.csv').read()
    storagedict = {}
    splitdata = data.split('\n')[1:]
    for line in splitdata:
        listed = line.split(',') #list of lists, ['string', 'stringnums'...]
        numberlist = []
        for stringnum in listed[1:]:
            numberlist.append(int(stringnum) / 100000)
        storagedict[listed[0]] = numberlist #dictionary, 'string' : ['stringnums'...]
    if request == 'yearpop':
        valueindex = int(year) - 1960
        return storagedict[country][valueindex]
    elif request == 'popdict':
        return storagedict
    elif request == 'countrydata':
        return storagedict[country]
        

def generateyears():
    n = []
    current = 1960
    while current < 2023:
        n.append(current)
        current += 1
    return list(n)

#-=-=-=-=-= HTML -==-=-=-=-=-=-=

def html(body):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
    <meta charset="utf-8">
    <title> Country Stats </title></head>
    """
    html += '<body>' + body + '</body>'
    html += '</body></html>'
    return html

def body(img, form):
    body = """
    <h1> Test Header </h1>
    <p> Input one of the following country names to generate a graph of its population from 1960 to 2022. <br>
    Note that 
    """
    body += img + '</p>'
    body += '<p> a form'
    body += form + '</p>'
    return body


#form setup
def form():
    html = """
    <form action="populationpage.py" method="GET">
      <input type="text" id="country" name="countryname" value=""><br>
      <input type="submit" value="Submit">
    </form> 
    """
    return html
form_input = cgi.FieldStorage()
# img setup
country = form_input.getvalue('countryname')
xname = 'Year'
yname = 'Population of ' + str(country) + 'in hundreds of thousands'
if ('countryname' in form_input):
    xdata = generateyears()
    ydata = returnpopulation(country, '', 'countrydata')
    plt.plot(xdata, ydata)
    plt.xlabel(xname)
    plt.ylabel(yname)
img = make_image_element()
form = form()
body = body(img, form)
html = html(body)
print(html)
