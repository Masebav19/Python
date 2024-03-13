
def str2array(string=""):
    if len(string)>0:
        array=[]
        i = 0
        array_str=""
        while(i<len(string)):
            if(string[i]!=','):
                while((string[i]!=',')):
                    array_str = array_str+string[i]
                    if (i < len(string)-1):
                        i=i+1
                    else:
                        break
                array.append(int(array_str))
                array_str=""
                i=i+1   
            else:
                i=i+1  
        return array
    else:
        return None