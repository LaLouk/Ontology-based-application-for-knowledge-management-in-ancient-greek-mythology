import csv
#from Owlready2 import *
from owlready2 import *
from SPARQLWrapper import SPARQLWrapper, JSON


onto_path.append("C:/Users/Aggelos/Desktop/Thesis/forTest")
onto = get_ontology("DragonsEmptyCorrected.owl")
onto.load()

print(list(onto.classes()))

MonstrousTitan = onto.Monster("Monstrous_Titan")
Male = onto.Human("Male")
Female = onto.Human("Female")

#Exceptions
Typhoeus = onto.Creatures("Typhoeus")
Typhoeus.has_Form = [MonstrousTitan]
Typhoeus.has_Name = ["Typhoeus"]

Argus = onto.Creatures("Argus Panoptes")
Argus.has_Form = [MonstrousTitan]
Typhoeus.has_Name = ["Argus Panoptes"]

Gaea = onto.God("Gaea")
Gaea.has_Sex = [Female]
Gaea.has_Name = ["Gaea"]

Phorcys = onto.Creatures("Phorcys")
Phorcys.has_Form = [MonstrousTitan]
Phorcys.has_Name = ["Phorcys"]

Ceto = onto.Dracaenae("Ceto")
Ceto.has_Name = ["Ceto"]

Phorcys = onto.Creatures("Phorcys")
Phorcys.has_Form = [MonstrousTitan]
Phorcys.has_Name = ["Phorcys"]

Heracles = onto.Hero("Heracles")
Heracles.has_Sex = [Male]
Heracles.has_Name = ["Heracles"]

Apollo = onto.God("Apollo")
Apollo.has_Sex = [Male]
Apollo.has_Name = ["Apollo"]

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

with open('DragonsUpdatedWithInfo.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0


    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            for i in range(12):
                if row[i]=='null':
                    row[i] = None

            DragonInstance = row[0]
            DragonCat = row[1]
            DragonName = row[2]
            DragonSum = row[3]
            DragonParent = row[4]
            DragonForm = row[5]
            DragonHome = row[6]
            DragonSlayer = row[7]
#    ->     DragonSymbol = row[8]
#    ->     DragonPlant = row[9]
#    ->     DragonGodOf = row[10]
            DragonInfo = row[11]

            if(DragonInstance=='Ceto'):
                Ceto.lives_In = [onto.Location(DragonHome)]
                Ceto.has_Summary = [DragonSum]
                Ceto.has_Info = [DragonInfo]
                Ceto.has_Name = [DragonName]
                if ('Typhoeus' in str(DragonParent)):
                    Dragon.has_Parent = [Typhoeus]
                if ('Gaea' in str(DragonParent)):
                    Dragon.has_Parent = [Gaea]
                if ('Ceto' in str(DragonParent)):
                        Dragon.has_Parent = [Ceto]
                if ('Phorcys' in str(DragonParent)):
                    Dragon.has_Parent = [Phorcys]
                break

            line_count += 1

            #Class of the Dragon
            if DragonCat == "DRACONES MYTHICAL":
                Dragon = onto.Dracones_Mythical(DragonInstance)
            elif DragonCat == "DRACAENAE":
                Dragon = onto.Dracaenae(DragonInstance)
            elif DragonCat == "DRACONES LEGENDARY":
                Dragon = onto.Dracones_Legendary(DragonInstance)
            elif DragonCat == "CETEA MYTHICAL":
                Dragon = onto.Cetea_Mythical(DragonInstance)
            elif DragonCat == "CETEA LEGENDARY":
                Dragon = onto.Cetea_Legendary(DragonInstance)
            else :
                Dragon = onto.Chimaera(DragonInstance)

            #Dragon's Sum and Information
            Dragon.has_Summary = [DragonSum]
            Dragon.has_Info = [DragonInfo]

            #Dragon's Name
            if (DragonName != None):
                Dragon.has_Name = [DragonName]
                print (Dragon.has_Name)

            # Handling Exception

            if (DragonSlayer == 'Apollo'):
                Dragon.is_Killed_By = [Apollo]
                DragonSlayer = None
            elif(DragonSlayer == 'Heracles'):
                Dragon.is_Killed_By = [Heracles]
                DragonSlayer = None

            if('and' in str(DragonParent)):
                if ('Typhoeus' in str(DragonParent)):
                    Dragon.has_Parent = [Typhoeus]
                if ('Gaea' in str(DragonParent)):
                    Dragon.has_Parent = [Gaea]
                if ('Ceto' in str(DragonParent)):
                        Dragon.has_Parent = [Ceto]
                if ('Phorcys' in str(DragonParent)):
                    Dragon.has_Parent = [Phorcys]
            else:
                if ('Typhoeus' in str(DragonParent)):
                    Dragon.has_Parent = [Typhoeus]
                    DragonParent = None
                if ('Gaea' in str(DragonParent)):
                    Dragon.has_Parent = [Gaea]
                    DragonParent = None
                if ('Ceto' in str(DragonParent)):
                    Dragon.has_Parent = [Ceto]
                    DragonParent = None
                if ('Phorcys' in str(DragonParent)):
                    Dragon.has_Parent = [Phorcys]
                    DragonParent = None

            #Dragon's Parent
            if DragonParent != None:
                parent = DragonParent
                if ("and" in DragonParent):
                    parents = DragonParent.split(" and ")
                    for par in parents:
                        if((par == 'Typhoeus') | (par == 'Ceto' )|(par == 'Phorcys') | (par == 'Gaea')):
                            continue

                        sparql.setQuery("""
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT ?label
                            WHERE { <http://dbpedia.org/resource/""" + par + """> rdf:type ?label }
                        """)
                        sparql.setReturnFormat(JSON)
                        results = sparql.query()
                        # results.print_results()
                        result = results.convert()
                        # print (str(result))
                        if ('Goddess' in str(result)):
                            Parent = onto.God(par)
                            Parent.has_Sex = [Female]
                            Parent.has_Name = [par]
                            Dragon.has_Parent = [Parent]
                        elif (('God' in str(result)) | ('Deities' in str(result))):
                            Parent = onto.God(par)
                            Parent.has_Sex = [Male]
                            Parent.has_Name = [par]
                            Dragon.has_Parent = [Parent]
                        elif ('Person' in str(result)):
                            Parent = onto.Hero(par)
                            if ('Female' in str(result)):
                                Parent.has_Sex = [Female]
                            else:
                                Parent.has_Sex = [Male]
                            Parent.has_Name = [par]
                            Dragon.has_Parent = [Parent]
                        else:
                            Parent = onto.Creatures(par)
                            Parent.has_Form = [MonstrousTitan]
                            Parent.has_Name = [par]
                            Dragon.has_Parent = [Parent]
                else:
                    sparql.setQuery("""
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        SELECT ?label
                        WHERE { <http://dbpedia.org/resource/""" + DragonParent + """> rdf:type ?label }
                    """)
                    sparql.setReturnFormat(JSON)
                    results = sparql.query()
                    # results.print_results()
                    result = results.convert()
                    # print (str(result))
                    if ('Goddess' in str(result)):
                        Parent = onto.God(DragonParent)
                        Parent.has_Sex = [Female]
                        Parent.has_Name = [DragonParent]
                        Dragon.has_Parent = [Parent]
                    elif (('God' in str(result)) | ('Deities' in str(result))):
                        Parent = onto.God(DragonParent)
                        Parent.has_Sex = [Male]
                        Parent.has_Name = [DragonParent]
                        Dragon.has_Parent = [Parent]
                    elif ('Person' in str(result)):
                        Parent = onto.Hero(DragonParent)
                        if ('Female' in str(result)):
                            Parent.has_Sex = [Female]
                        else:
                            Parent.has_Sex = [Male]
                        Parent.has_Name = [DragonParent]
                        Dragon.has_Parent = [Parent]
                    else:
                        Parent = onto.Creatures(DragonParent)
                        Parent.has_Form = [MonstrousTitan]
                        Parent.has_Name = [DragonParent]
                        Dragon.has_Parent = [Parent]

            #Dragon's Form
            if (("lion" in str(DragonForm)) | ("goat" in str(DragonForm))):
                Dragon.has_Form = [onto.Hybrid(DragonForm)]
            elif (("fish" in str(DragonForm)) | ("sea" in str(DragonForm))):
                Dragon.has_Form = [onto.Sea_Monster(DragonForm)]
            elif ("serpent" in str(DragonForm)):
                Dragon.has_Form = [onto.Serpent(DragonForm)]
            else:
                Dragon.has_Form = [onto.Monster(DragonForm)]


            #Location of the Dragon
            Dragon.lives_In = [onto.Location(DragonHome)]


            #Slayer of the Dragon
            if DragonSlayer != None:
                #name = DragonSlayer
                if ("and" in DragonSlayer):
                    slayers = DragonSlayer.split(" and ")
                    for name in slayers:
                        sparql.setQuery("""
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT ?label
                            WHERE { <http://dbpedia.org/resource/""" + name + """> rdf:type ?label }
                        """)
                        sparql.setReturnFormat(JSON)
                        results = sparql.query()
                        # results.print_results()
                        result = results.convert()
                        # print (str(result))
                        if ('Goddess' in str(result)):
                            Slayer = onto.God(name)
                            Slayer.has_Sex = [Female]
                            Slayer.has_Name = [name]
                            Dragon.is_Killed_By = [Slayer]
                        elif (('God' in str(result)) | ('Deities' in str(result))):
                            Slayer = onto.God(name)
                            Slayer.has_Sex = [Male]
                            Slayer.has_Name = [name]
                            Dragon.is_Killed_By = [Slayer]
                        elif ('Person' in str(result)):
                            Slayer = onto.Hero(name)
                            if ('Female' in str(result)):
                                Slayer.has_Sex = [Female]
                            else:
                                Slayer.has_Sex = [Male]
                            Slayer.has_Name = [name]
                            Dragon.is_Killed_By = [Slayer]
                        else:
                            Slayer = onto.Creatures(name)
                            Slayer.has_Form = [MonstrousTitan]
                            Slayer.has_Name = [name]
                            Dragon.is_Killed_By = [Slayer]
                        # print(True)
                        # else:
                        # print(False)
                elif (DragonSlayer == 'Argus Panoptes'):
                    Dragon.is_Killed_By = [Argus]
                else:
                    sparql.setQuery("""
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        SELECT ?label
                        WHERE { <http://dbpedia.org/resource/""" +DragonSlayer+"""> rdf:type ?label }
                    """)
                    sparql.setReturnFormat(JSON)
                    results = sparql.query()
                    #results.print_results()
                    result = results.convert()
                    #print (str(result))
                    if('Goddess' in str(result)):
                        Slayer = onto.God(DragonSlayer)
                        Slayer.has_Sex = [Female]
                        Slayer.has_Name = [DragonSlayer]
                        Dragon.is_Killed_By = [Slayer]
                    elif(('God' in str(result)) | ('Deities' in str(result))):
                        Slayer = onto.God(DragonSlayer)
                        Slayer.has_Sex = [Male]
                        Slayer.has_Name = [DragonSlayer]
                        Dragon.is_Killed_By = [Slayer]
                    elif('Person' in str(result)):
                        Slayer = onto.Hero(DragonSlayer)
                        if ('Female' in str(result)):
                            Slayer.has_Sex = [Female]
                        else:
                            Slayer.has_Sex = [Male]
                        Slayer.has_Name = [DragonSlayer]
                        Dragon.is_Killed_By = [Slayer]
                    else:
                        Slayer = onto.Creatures(DragonSlayer)
                        Slayer.has_Form = [MonstrousTitan]
                        Slayer.has_Name = [DragonSlayer]
                        Dragon.is_Killed_By = [Slayer]

onto.save()