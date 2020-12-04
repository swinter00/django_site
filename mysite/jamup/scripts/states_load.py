from jamup.models import State, City

def run():
    f_handler = open('jamup/populous_cities.txt', 'r')

    State.objects.all().delete()
    City.objects.all().delete()

    for line in f_handler.readlines():
        split_line = line.split(",")
        s, created = State.objects.get_or_create(name = split_line[2])
        c = split_line[1]

        city = City(name = c, state = s)

        city.save()

# Data pulled from here: https://gist.github.com/Miserlou/11500b2345d3fe850c92
