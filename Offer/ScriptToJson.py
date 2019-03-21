i = -1
j = -1
result = []
fileFinal = []

#to examine 
#https://stackoverflow.com/questions/17388254/django-retrieving-ids-of-manytomany-fields-quickly

template = """
    def toJson():
        result = {}"""
with open("models.py", "r") as f :
    ls = f.readlines() 
    for l in ls :
        j = j + 1
        fileFinal.append(l)

        print(l)
        if "class" in l :
            i = i + 1
            result.append(template)
            if i != 0 :
                result[i-1] = result[i-1] + "\n        return result"
                fileFinal[j-1] = fileFinal[j-1] +"\n" + result[i-1] +"\n\n" 
        if " = models." in l :
            result[i] =   result[i] + "\n        result[\"" + l.split(" = ")[0].strip() +"\"] = self."+ l.split(" = ")[0].strip()


result[i] = result[i] + "\n        return result"
print(result)            
fileFinal[j] = fileFinal[j] +"\n" + result[i]
resultF = ""
with open('models2.py', 'w') as f:
    for item in fileFinal:
        resultF = resultF + item
    item = resultF
    item = item.replace("\n\n\n\n","\n\n")
    item = item.replace("\r\r\r\r","\r\r")
    f.write(item)

