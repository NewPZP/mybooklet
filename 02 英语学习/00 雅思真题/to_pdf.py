import os
cur_path = os.path.dirname(os.path.abspath(__file__))
def get_files():
    files = os.listdir(cur_path)
    md_files = [f for f in files if f.endswith('.md')]
    md_files = [ f.replace(' ','\ ') for f in files]
    return sorted(md_files)
md_list = get_files()
cmd = "pandoc " + " ".join(md_list[1:-1]) + " -o 雅思part1合集.pdf --pdf-engine=xelatex"
print(cmd)
os.system(f'cd {cur_path}')
os.system(cmd)
# pandoc 01\ Work.md  -o 雅思part1合集.pdf 
# 'pandoc 01\\ Work.md 02\\ Accommodation.md 03\\ Staying\\ at\\ home.md 04\\ Exciting\\ activities.md 05\\ Ask\\ for\\ help.md 06\\ Sharing.md 07\\ Home\\ Town.md 08\\ The\\ area\\ you\\ live\\ in.md 09\\ E-book.md 10\\ Internet.md 11\\ Childhood\\ memory.md 12\\ Classmate.md 13\\ Teacher.md 14\\ language.md 15\\ numbers.md 16\\ pen\\ or\\ pencil.md 17\\ birthday.md 18\\ weather.md 19\\ shopping.md 20\\ morning\\ routines.md 21\\ mobile\\ phone.md 22\\ holidays.md 23\\ sports.md 24\\ daily\\ routine.md 25\\ Science.md 26\\ News.md 27\\ library.md 28\\ keys.md 29\\ jewelry.md 30\\ Life\\ stages.md 31\\ relax.md 32\\ weekends.md 33\\ art.md 34\\ outer\\ space.md 35\\ T-shirts.md 36\\ staying\\ up\\ late.md 37\\ school\\ and\\ workplace.md 38\\ happiness.md 39\\ chocolate.md 40\\ challenges.md 41\\ music.md 42\\ math.md 43\\ flowers.md 44\\ pets\\ and\\ animals.md 45\\ small\\ business.md 46\\ sunglasses.md 47\\ social\\ media.md 48\\ Memory.md 49\\ cake\\ or\\ dessert.md 50\\ video\\ game.md 51\\ color.md 52\\ singing.md 53\\ advertising.md 54\\ feel\\ bored.md 55\\ crowed\\ place.md 56\\ money.md 98\\ Time\\ management.md  -o 雅思part1合集.pdf --pdf-engine=xelatex'

'pandoc 01 Work.md 02 Accommodation.md 03 Staying at home.md 04 Exciting activities.md 05 Ask for help.md 06 Sharing.md 07 Home Town.md 08 The area you live in.md 09 E-book.md 10 Internet.md 11 Childhood memory.md 12 Classmate.md 13 Teacher.md 14 language.md 15 numbers.md 16 pen or pencil.md 17 birthday.md 18 weather.md 19 shopping.md 20 morning routines.md 21 mobile phone.md 22 holidays.md 23 sports.md 24 daily routine.md 25 Science.md 26 News.md 27 library.md 28 keys.md 29 jewelry.md 30 Life stages.md 31 relax.md 32 weekends.md 33 art.md 34 outer space.md 35 T-shirts.md 36 staying up late.md 37 school and workplace.md 38 happiness.md 39 chocolate.md 40 challenges.md 41 music.md 42 math.md 43 flowers.md 44 pets and animals.md 45 small business.md 46 sunglasses.md 47 social media.md 48 Memory.md 49 cake or dessert.md 50 video game.md 51 color.md 52 singing.md 53 advertising.md 54 feel bored.md 55 crowed place.md 56 money.md -o 雅思part1合集.pdf --pdf-engine=xelatex'