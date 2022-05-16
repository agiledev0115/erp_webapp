import io
import csv

# function to read and convert CSV data
def csvread(request,form_handle:str):
    # print(self.request.FILES['file'])
    # get files from request
    file = request.FILES[form_handle]
    # open and read csv data and decode
    csv_data = file.read().decode('UTF-8')
    # create a text stream with io
    io_string = io.StringIO(csv_data)
    # use csv reader to read 
    reader = csv.reader(io_string, delimiter=',', quotechar='|')
    
    return reader