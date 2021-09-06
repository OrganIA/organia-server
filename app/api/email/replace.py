def replace(file, args):
    res = ''
    with open(file) as f:
        newMail = f.readlines()
        for lines in newMail :
            res = res+lines       
    f.close()

    for i, arg in enumerate(args):
        res=res.replace(str(i), arg)

    f = open("./mailRes.txt","w+")
    f.write(res)
    f.close()

def getMail(model, args):
    allTemplates = {
        1: "Template/Mail1.tpl",
        2: "Template/Mail2.tpl",
        3: "Template/Mail3.tpl"
    }
    file = allTemplates.get(model, "Invalid month")
    replace(file, args)