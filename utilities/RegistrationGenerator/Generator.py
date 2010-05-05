from random import choice

NumberToGenerate = 1000
Template = "INSERT INTO checkin_registration (full_name, email, checkedin) VALUES ('%s', '%s', 0);"

FirstNamesFile = "firstnames.txt"
LastNamesFile  = "lastnames.txt"
DomainsFile = "domains.txt"

f = file(FirstNamesFile)
FirstNames = f.readlines()

f = file(LastNamesFile)
LastNames = f.readlines()

f = file(DomainsFile)
Domains = f.readlines()

count = 0
while count < NumberToGenerate:
	name = "%s %s" % (choice(FirstNames).strip().title(), choice(LastNames).strip().title())
	email = "%s@%s" % (name.replace(' ', '.'), choice(Domains).strip())
	print Template % (name, email)
	count += 1
