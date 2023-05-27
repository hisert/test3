
start_bit = "("
stop_bit = ")"
def flagAdd(flagVal,flag):
    process = flagVal | flag
    return process

def flagErase(flagVal,flag):
    process = flagVal & ~flag
    return process

def flagIsHave(flagVal,flag):
    if(flagVal & flag):
         return 1;
    return 0;

def string_erase_first_char(data):
    newdata = ""
    for x in range(len(data)):
        if(x != 0):
            newdata = newdata + data[x]
    return newdata

def string_erase_last_char(data):
    newdata = ""
    for x in range(len(data) -1):
        newdata = newdata + data[x]
    return newdata

def split_data(data):
    words = data.split(stop_bit)
    if((len(words)-1) > 0):
            newdata = ""
            if(words[0][0] == start_bit):
                words[0] = words[0]
                newdata = string_erase_first_char(words[0])
            else:
                findflag = 0
                newdata = ""
                for x in words[0]:
                    if(findflag > 0):
                         newdata = newdata + x
                    else:
                         if(x == start_bit):
                             findflag = 1
            return newdata
    else:
          return ""
