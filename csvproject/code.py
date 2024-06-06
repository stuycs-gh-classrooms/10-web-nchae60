#! /usr/bin/python
print('Content-type: text/html\n')
import cgitb #
#cgitb.enable()
import matplotlib.pyplot as plt
import io
import base64
import cgi
import math
#delete this one
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
            numberlist.append(int(stringnum))
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

def otherdata(country, request):
    data = open('otherdata.csv').read()
    storagedict = {}
    splitdata = data.split('\n')[1:]
    splitnew = []
    for element in splitdata:
        splitnew.append(element.split(','))
    for list in splitnew:
        numberlist = []
        for stringnum in list[3:]:
            if stringnum != '':
                numberlist.append(float(stringnum))
            else:
                numberlist.append('Info Unavailable')
            storagedict[list[0]] = numberlist
    if request == 'dict':
        return storagedict
    elif request == 'countryinfo':
        return storagedict[country]

def infotoindex(whichdata):
    data = open('otherdata.csv').read()
    splitdata = data.split(',')[3:19]
    index = splitdata.index(whichdata)
    return index


#pprint.pprint(otherdata('United States', 'countryinfo'))
#print(returnpopulation('', '', 'popdict'))
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
    <p> paragraph thing
    """
    body += img + '</p>'
    body += '<p> a form'
    body += form + '</p>'
    return body


#form setup
def form():
    html = """
    <form action="code.py" method="GET">
    <label for="country">Official Country Name:</label>
    <input type="text" id="country" name="country" value="United States"><br>
    <input type="submit" value="Submit">
    </form>
    """
form_input = cgi.FieldStorage()
print(form_input)
# img setup
country = form_input.getvalue('country')
xdata = generateyears()
ydata = returnpopulation(country, '', 'countrydata')
xname = 'Year'
yname = 'Population'
plt.plot(xdata, ydata)
plt.xlabel(xname)
plt.ylabel(yname)
img = make_image_element()

html(body(img, form()))
