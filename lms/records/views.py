from django.shortcuts import render, redirect
from . import models
from django.views import generic
from . import forms
from django.views import View
from django.views.generic.edit import FormView
import csv
import codecs
from django.http import HttpResponseRedirect
from . import myfun
########## imports ################


###### objects for Thing and Item models so that dynamic query can be performed from given list of IDs as done at line 68-87##################
class Table_things:

    def __init__(self, code, description, date, stat_one, stat_two):
        self.code = code
        self.description = description
        self.date = date
        self.stat_one = stat_one
        self.stat_two = stat_two


class Table_item:
    def __init__(self, thing, name, rating, score):
        self.thing = thing
        self.name = name
        self.rating = rating
        self.score = score

# #####  Getting file input #################

def create_view(request):

    form = forms.TsvFileForm()
    validate_list = []
    update = []
    if request.method == "POST":

        form = forms.TsvFileForm(request.POST, request.FILES)
        files = request.FILES['tsv_file']
        
        if form.is_valid():
            
            main_ls = []

############# converting TSV files into 2-d list format where each row represents a single entry#####
            for f in files:
                ls = f.decode("utf-8")
                x = ls.split("\t")
          
                main_ls.append(x)   ###### getting tsv data in list format seperated by tab

   

            
            validate_list = myfun.validate_data(request,main_ls)  ##### validation fuction, to validate all the data in a single row. 
                                                                  #if the (validate_list) is empty then there are no errors
            create_lst = []
            create_lst2 = []
            update_lst = []
            update_lst2 = []


            if not validate_list:                        ########## checking if all fields are valid
                data = myfun.create_row(main_ls)         ######### function to insert data into database##########


############# Getting new data in create_lst (model 1) and create_list2 (model2)
                if len(data[0]) != 0:
                    create = set(data[0])
                    for cr in create:
                        obj = models.Thing.objects.get(code = cr)
                        tabl = Table_things(obj.code, obj.description, obj.date, obj.stat_one, obj.stat_two)
                        create_lst.append(tabl)
                        tabl2 = models.Item.objects.get(thing = obj)
                        create_lst2.append(tabl2)

  ############# Getting updated data  in update_lst (model 1) and update_list2 (model2)              
                if len(data[1]) != 0:
                    update = set(data[1])
                    for up in update:
                        obj = models.Thing.objects.get(code = up)
                        tabl = Table_things(obj.code, obj.description, obj.date, obj.stat_one, obj.stat_two)
                        update_lst.append(tabl)

                        tabl2 = models.Item.objects.get(thing = obj)
                        update_lst2.append(tabl2)


                print(create_lst)
                print(update_lst)



                context = {'form': form, 'create': create_lst, 'create2':create_lst2, 'update': update_lst, 'update2':update_lst2}

            else:
                # print(validate_list)
                context = {'form':form, 'validate':validate_list}
            

         
            return render(request, 'file_input.html', context)
    
        # print("-------------------")
    
    context = {'form': form, 'validate':validate_list}
    return render(request, 'file_input.html', context)




