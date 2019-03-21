i = -1
result = []
template = """
    def toJson():
        result = {}"""
with open("models.py", "r") as f :
    ls = f.readlines() 
    for l in ls :
        print(l)
        if "class" in l :
            i = i + 1
            result.append(template)
            if i != 0 :
                result[i-1] = result[i-1] + "\n        return result"
        if " = models." in l :
            result[i] =   result[i] + "\n        result[\"" + l.split(" = ")[0].strip() +"\"] = self."+ l.split(" = ")[0].strip()


result[i] = result[i] + "\n        return result"
print(result)            
with open('result.txt', 'w') as f:
    for item in result:
        f.write("%s\n" % item)