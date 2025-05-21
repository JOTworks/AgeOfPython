<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://raw.githubusercontent.com/JOTworks/AgeOfPython/main/resources/images/AOP%20logo.png">
    <img src="https://raw.githubusercontent.com/JOTworks/AgeOfPython/main/resources/images/AOP%20logo.png" alt="Logo" width="240" height="240">
  </a>

  <h3 align="center">Age Of Python</h3>

  <p align="center">
    Script your AOE2 AI in limited python instead of defrules
    <br />
    <br />
    <a href="https://github.com/JOTworks/AgeOfPython/issues">Report Bug</a>
    ·
    <a href="https://github.com/JOTworks/AgeOfPythone/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#supported-python">Supported Python</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

CURRENTLY IN ALPHA ... Functional, but missing features, and limmited error handling

You can write in Python, and it will compile your code into AOE2Script.
No more defrules, all commands look like normal functions.

the purpose of this project is to improve redablility and reusiblility so you can write and debug bigger and better AIs
It includes functions, loops, nested if statements, Arrays ect.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

For now you will need to know how to code in both python and aoe2script.

### Installation

_Clone this into the folder C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\ai\ _

1. Clone the repo
   ```sh
   git clone https://github.com/JOTworks/AgeOfPython.git
   ```

2. install python and all the dependencies

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Create a .aop file in the AgeOfPython folder. that is your base python ai code.
when you run that file it will create the .per and .ai files in the ia\ folder for you.
Run it with the python command like so if you are in the AgeOfPython folder
   ```sh
   python .\src\Main.py -f yourAiName.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- SUPPORTED PYTHON -->
## Supported Python

### If statemnts
if statments can do basic comparisons and any operators. if there is to complex of an expression, break it out before the if statment
```
if command(arg) and command(arg,arg):
  x = 1
```

### For and While loops
you can do loops! and nest them, it makes readibility ver nice for algerithms
```
#set current_point
for i in range(-1,2):
    for j in range(-1,2):
        temp_point = last_point
        temp_point += (i, J)
        up_get_point_terrain(temp_point, terrain_id)

        if temp_point != last_point and up_point_terrain(temp_terraitemp_pointn_point) == Terrain.terrain_water_beach:
          current_point = temp_point
```

### Asigning
Unlike Python, this is A strongly typed language. Once a varilabe has a type it will raise an error is another is used.
to avoid confussion and the most bugs, use constructors on varaible. (sometimes this works without, but not for returning values of a function for exmaple)
```
x = Integer()
tc_location = Point()
tc_location = State()
my_array = (Point, 12) # (type, length)

```

if you add values into the constructor they will be asigned first pass of the code, and will then be disabled with a disable_self()
Note that all variables (goals) are set to -1 when aoe2 starts
```
x = Integer(10)
tc_location = Point(0,0)
```

asignign variables supports arrays and AOP class attributes
```
x = y + 3 * 2
myArray[i] = 37
my_point.x = 3
my_point = (3,2)
x = y = z = 1
```

However do not add array slices inside array slices, and nest other asignemnts at your own risk
```
my_rray[other_array[r]] = 37
```

### Functions
Functions require strong typeing for their parameter types and return types. you can notate that like in python, but now it is required.
this function bellow takes a buildingId and will try to build that building, returning 1 on success and 0 on failer. (you cannot use function returns in conditionals)
```
def try_build(building:BuildingId) -> Integer:
    if up_can_build(_, building) and up_pending_objects(building) < 1:
        up_build(_,_,building)
        return 1
    return 0
```
<br>
all functions pass by value and all variables in the function are only in their own scope. Note that it is the same variable for every call of the function, so if you do not set the varible it will have the value for the last call. If you need a variable from ouside the funtion you can use global to access it. otherwize it will create a new function scoped veriable.
```
def build_around_tc(building:BuildingId, radius:Integer) -> Integer:
    global tc_location
    place_point = Point()
    if tc_location.x == -1:
        chat_to_all("E: tc_location not set, cannot build_around_tc")
        return -1
    (truncated)
```
<br>
aoe2script Commands now look like functions, as you have seen above. but they are not the same!
if you use an aoe2script command it will work like it does in the original langauge. I have just added things for conveineince bellow.

<br><br>
if the command ends with CompareOp and value, you can pull that outside of the function. (effectivly it is still in the function and can't take complex input)
```
building_type_count_total(BuildingId.house) >= 5
```

g: and c: are removed, as I deal with all of the allocation of memory, so you can ignore that and it will be added in dynamicly
```
up_filter_distance(10, my_max)  #used to look like this -> (up-filter-distance c: 10 g: my_max)
```

Strategic numbers can be asigned in shorthand
```
SN.placement_zone_size = 7 #used to look like this -> (up-modify-sn sn-placement_zone_size c:= 7)
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

### Alpha Release

- [X] Add object types:
    - [X] Point
    - [X] State
    - [X] Const
- [X] fix curent bugs
- [X] implement disable-self in if statments


### Beta Release
- [ ] add loops:
    - [ ] while loop
    - [ ] for loop
- [ ] add functions
- [ ] Add simplified conditional expressions
- [ ] Add better errors and comments to track user bugs
- [ ] Add test casses:
    - [ ] parser
    - [ ] scanner
    - [ ] asserter
    - [ ] Interpreter
    - [ ] printer


### Full Release
- [ ] Robust functions:
    - [ ] Add default values
    - [ ] Add return values
- [ ] optimize rule usage
    - [ ] compine close truesy rules
    - [ ] remove jump rules on flat ifs & loops
    - [ ] refactor out lagging do-nothing rules on ifs
    - [ ] refactor out struct init asignment of +0
- [ ] optimize goal usage
    - [ ] dealocate when out of scope
- [ ] add predefined ai numbers
- [ ] Add printout of rule number and goal useage
- [ ] Add backwards compatability

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/JOTworks/AgeOfPython.svg?style=for-the-badge
[contributors-url]: https://github.com/JOTworks/AgeOfPython/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/JOTworks/AgeOfPython.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/JOTworks/AgeOfPython.svg?style=for-the-badge
[stars-url]: https://github.com/JOTworks/AgeOfPython/stargazers
[issues-shield]: https://img.shields.io/github/issues/JOTworks/AgeOfPython.svg?style=for-the-badge
[issues-url]: https://github.com/JOTworks/AgeOfPython/issues
[license-shield]: https://img.shields.io/github/license/JOTworks/AgeOfPython.svg?style=for-the-badge
[license-url]: https://github.com/JOTworks/AgeOfPython/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jackson-hunt-6a9b72127/
[product-screenshot]: images/screenshot.png
