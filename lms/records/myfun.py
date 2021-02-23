from . import views
from . import models
from . import forms
# from urllib import request

######### Validate score #######
def validate_score(score):
    if score == "":
        print("Empty score")
        return False

    scoreint = int(score)

    if scoreint < 0:
        print("invalid score")
        return False
    else:
        return True


############Validate description############

def validate_des(des):
    if des == "":
        return "no description"
    
    else:
        return des


###############validate rating ################
def validate_rating(rating):

    if rating == '':
        return False

    rate = float(rating)

    if rate >= 1.0 and rate <= 5.0:
        return True
    
    else:
        return False

############Validating date##########################
import datetime

def validate_date(date_text):

    format = "%Y-%m-%d"

    if date_text == "":
        # print("-------")
        # print("no value")
        return False



    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        # print("-------")
        # print("wrong value")
        return True

    except ValueError:
        # print("-------")
        # print("wrong value")
        return False

    # date_string = '12-25-2018'

    # format = "%Y-%m-%d"


    # try:

    #     datetime.datetime.strptime(date_string, format)

    #     print("This is the correct date string format.")

    # except ValueError:

    #     print("This is the incorrect date string format. It should be Y")


############ Gets the state value from literals.py ########################
def get_statvalue(str1, str2):
    
    lst = []

    if str1 == '01' or str1 == '02' or str1 == '03' or str1 == '04' or str1 == '11':
        lst.append(str1)
    else:
        lst.append('99')

    if str2 == '1' or str2 == '2' or str2 == '3' or str2 == '9':
        lst.append(str2)

    else:
        lst.append('9')    

    return lst


########### Validation fuctione#####################
def validate_data(request,file):

    length = len(file)
    inner_len = len(file[0])
    val = set()
    final_lst=[]


    for i in range(1, length):
   
        dict_val = {
            "code":"",
            "des":"",
            "stat_one":"",
            "stat_two":"",
            "name":"",
            "rating":"",
            "score":"",        
        }

        dict_val.update({"code": file[i][0]})
        dict_val.update({"des": file[i][1]})
        dict_val.update({"date": file[i][2]})
        dict_val.update({"stat_one": file[i][3]})
        dict_val.update({"stat_two": file[i][4]})
        dict_val.update({"name": file[i][5]})
        dict_val.update({"rating": file[i][6]})
        dict_val.update({"score": file[i][7]})


        ###################check if row already present##############

        if file[i][5] == "":
            val.add("Empty name")
        ###### date validation######
        is_date_valid = validate_date(dict_val.get("date"))

        if is_date_valid == False:
            val.add("Invalid date format")
            # val.append('1')


        ######## name validation#########

        if validate_date(dict_val.get("name")) == "":
            val.add("Invalid name")



        ######## check rating validation###################
        rating_valid = validate_rating(dict_val.get("rating"))

        if rating_valid == False:
            val.add("Invalid rating")


        ######## check score rating #########
        score_valid = validate_score(dict_val.get("score"))

        if score_valid == False:
            val.add("Invalid Score")

    ### return if validation error##########
        if val:
            return val  ##### return if any error found


            
    return val  #####val consists of all the erros which are present. So that if it is empty then validation success otherwise validation error


######## Insert data into db after validation##################################
def create_row(file):
    update = []
    create = []
    final_lst = []
    for i in range(1, len(file)):
        # print(i)
        # print(file[i][0])
        
        des_valid = validate_des(file[i][1])
        stat=[]
        stat = get_statvalue(file[i][3], file[i][4])

        score = int()
        if int(file[i][7]) >= 50:
            score = 50

##### ######## Check if the data already exists in table so that update operation can be performed
        if models.Thing.objects.filter(code=file[i][0]).exists():
            
            obj = models.Thing.objects.get(code=file[i][0])

            if models.Item.objects.filter(thing=obj).exists():
            
                update.append(file[i][0])
                if obj.description !=des_valid or obj.date !=file[i][2] or obj.stat_one != stat[0] or obj.stat_two != stat[1]:
                    temp = obj.code
                    # update.add(obj.code)

                obj2 = models.Item.objects.get(thing=obj)

                if obj2.name != file[i][5] or obj2.rating != file[i][6] or obj2.score != score:
                    temp = obj.code
                    # update.add(obj.code)
                
                obj.description = des_valid
                obj.date = file[i][2]
                obj.stat_one = stat[0]
                obj.stat_two = stat[1]
                obj.save()

                obj2.name = file[i][5]
                obj2.rating = file[i][6]
                obj2.score = score
                obj2.save()


        else:# ############Data is not present in db so new entry is created
            create.append(file[i][0])
            obj1 = models.Thing(code=file[i][0], description= des_valid, date= file[i][2], stat_one= stat[0], stat_two= stat[1])
            obj1.save()

            obj2 = models.Item(thing=obj1, name= file[i][5], rating= file[i][6], score= score)
            obj2.save()

        
    final_lst.append(create)  ############ list of id for newly created row
    final_lst.append(update) ############ list of id for updated row

    return final_lst