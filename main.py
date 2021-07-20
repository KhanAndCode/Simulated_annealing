import random
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import FormatStrFormatter

AMOUNT_OF_CITIES =40
TEMPERATURE_MIN = 0.01
TEMPERATURE_MAX = 8000
FOR_GRAPHICS = TEMPERATURE_MAX*5/100
ITERATIONS = TEMPERATURE_MAX*10


class City:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number

    def __str__(self):
        return "%s - (%s,%s)" % (self.number, self.x, self.y)


def swap(candidate):
    cities_swap = random.sample(candidate, k=2)
    candidate[cities_swap[0]], candidate[cities_swap[1]] = candidate[cities_swap[1]], candidate[cities_swap[0]]
    return candidate


def swap_new(candidate):
    cities_swap = random.sample(candidate, k=2)
    maximum_random = max(cities_swap[0], cities_swap[1])
    minimum_random = min(cities_swap[0], cities_swap[1])
    candidate2 = candidate[minimum_random:maximum_random]
    candidate2.reverse()
    candidate = candidate[:minimum_random] + candidate2 + candidate[maximum_random:]
    return candidate


def calculate_probability(T, energy_new, energy):
    delta_energy = energy_new - energy
    p = math.exp(-1 * delta_energy / T)
    return p


def is_take(probability):
    random_number = random.random()
    if random_number <= probability:
        return True
    else:
        return False


def change_temp_Bolcman(temperature, i):
    return temperature / (math.log(1 + i))


def change_temp_Koshi(temperature, i):
    return temperature / i


def calculate_energy(candidate):
    energy = 0.0
    for i in range(len(candidate)):
        if i == len(candidate) - 1:
            if candidate[0] < candidate[i]:
                distance = "%s - %s" % (candidate[0], candidate[i])
            else:
                distance = "%s - %s" % (candidate[i], candidate[0])
        elif candidate[i] < candidate[i + 1]:
            distance = "%s - %s" % (candidate[i], candidate[i + 1])
        else:
            distance = "%s - %s" % (candidate[i + 1], candidate[i])
        energy = energy + DISTANCES.get(distance)
    return energy


# Create cities
cities = []
# with open("coordinates.txt") as file_handler:
#     AMOUNT_OF_CITIES = int(file_handler.readline().rstrip())
#     for i in range(AMOUNT_OF_CITIES):
#         line = file_handler.readline()
#         line = line.rstrip()
#         arr = line.split(" ")
#         x = int(arr[0])
#         y = int(arr[1])
#         city = City(x, y, i)
#         cities.append(city)
with open("coordinates.txt", 'w') as file_handler:
    file_handler.write(str(AMOUNT_OF_CITIES)+"\n")
    for i in range(AMOUNT_OF_CITIES):
        x = random.randint(10, 100)
        y = random.randint(10, 100)
        city = City(x, y, i)
        coordinates = "%s %s\n" % (x, y)
        file_handler.write(coordinates)
        cities.append(city)

# Get distances
DISTANCES = {}
for i in range(len(cities)):
    for j in range(i + 1, len(cities)):
        key = "%s - %s" % (cities[i].number, cities[j].number)
        value = (math.sqrt((cities[i].x - cities[j].x) ** 2 + (cities[i].y - cities[j].y) ** 2))
        DISTANCES[key] = value

candidate = [i for i in range(AMOUNT_OF_CITIES)]
random.shuffle(candidate)
energy = calculate_energy(candidate)
print(candidate)
print(energy)

fig, (ax1, ax2, ax3) = plt.subplots(3)
point_x_for_axes3 = []
point_y_for_axes3 = []
array_x_old = []
array_y_old = []
ax1.axis([0, 110, 0, 110])
ax2.axis([0, 110, 0, 110])
ax3.axis([FOR_GRAPHICS, TEMPERATURE_MIN, 0, energy * 2])
for i in range(-1, len(candidate)):
    array_x_old.append(cities[candidate[i]].x)
    array_y_old.append(cities[candidate[i]].y)

current_temperature = TEMPERATURE_MAX
for i in range(1, ITERATIONS):
    # while current_temperature >= TEMPERATURE_MIN:
    if current_temperature <= TEMPERATURE_MIN:
        print("break")
        break
    new_candidate = swap_new(candidate)
    energy_new_candidate = calculate_energy(new_candidate)
    if energy >= energy_new_candidate:
        energy = energy_new_candidate
        candidate = new_candidate
    else:
        probability = calculate_probability(current_temperature, energy_new_candidate, energy)
        if is_take(probability):
            energy = energy_new_candidate
            candidate = new_candidate
    current_temperature = change_temp_Koshi(TEMPERATURE_MAX, i)
    point_x_for_axes3.append(current_temperature)
    point_y_for_axes3.append(energy)

print(candidate)
print(energy)

array_x = []
array_y = []
for i in range(-1, len(candidate)):
    if i == 0:
        ax1.plot(cities[candidate[i]].x, cities[candidate[i]].y, 'ro', color="red")
        ax2.plot(cities[candidate[i]].x, cities[candidate[i]].y, 'ro', color="red")
    elif i == AMOUNT_OF_CITIES - 1:
        ax1.plot(cities[candidate[i]].x, cities[candidate[i]].y, 'ro', color="yellow")
        ax2.plot(cities[candidate[i]].x, cities[candidate[i]].y, 'ro', color="yellow")
    else:
        ax1.plot(cities[candidate[i]].x, cities[candidate[i]].y, 'ro', color="blue")
        ax2.plot(cities[candidate[i]].x, cities[candidate[i]].y, 'ro', color="blue")
    array_x.append(cities[candidate[i]].x)
    array_y.append(cities[candidate[i]].y)
ax3.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax3.plot(point_x_for_axes3, point_y_for_axes3)
ax1.set_title(" Расстояние между %s городами: %s. Tmin = %s, Tmax = %s" % (
    AMOUNT_OF_CITIES, energy, TEMPERATURE_MIN, TEMPERATURE_MAX))
ax2.plot(array_x, array_y)
ax1.plot(array_x_old, array_y_old)
plt.show()
