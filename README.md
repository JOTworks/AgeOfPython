<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



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
  <a href="https://ih1.redbubble.net/image.636495678.3338/flat,550x550,075,f.u3.jpg">
    <img src="https://ih1.redbubble.net/image.636495678.3338/flat,550x550,075,f.u3.jpg" alt="Logo" width="80" height="80">
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

CURRENTLY IN PREALPHA ... basicly main branch is not promissed to even be functional. give it a week or 2 and we should be in alpha

writing with aoeScript defrules and using goals and dealing with the 30 character command names can be dificult. 
Exspecialy it can be dificult reading what others have written (that is including your past self in others)

the purpose of this project is mainly to improve redablility so you can write and debug bigger and better AIs
Along with redability are actual improvements like functions, nested if statements, Point structs ect.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started



### Prerequisites

For now you will need python and pip to run the project untill i create builds.

### Installation

_Clone this into the folder C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\ai\ _

1. Clone the repo
   ```sh
   git clone https://github.com/JOTworks/AgeOfPython.git
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To use this project create a .aop file in the AgeOfPython folder. that is your base ai code.
when you run that file it will create the .per and .ai files in the ia\ folder for you.
run it with the python command like so if you are in the AgeOfPython folder
   ```sh
   py src/Main.py yourAiName.aop
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- SUPPORTED PYTHON -->
## Supported Python

#### If statemnts
if statments can only have conditions in them like defrules currently
```
if(command arg)(command arg arg):
  (command)
```
#### Asigning
asignign variables currently only supports 2 in an expression so
```
x = 0
x = 1 + 3
x = y + z
```
but do not use more then 2, or use any parenthesis

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

### Alpha Release

- [ ] Add object types:
    - [ ] Point
    - [ ] State
    - [ ] Const
- [ ] fix curent bugs
- [ ] implement disable-self in if statments


### Beta Release

- [ ] Add backwards compatability
- [ ] Add asserter to tell user if syntax is not supported
- [ ] Add better errors and comments to track user bugs
- [ ] Add test casses:
    - [ ] parser
    - [ ] scanner
    - [ ] asserter
    - [ ] Interpreter
    - [ ] printer


### Full Release

- [ ] Add object types:
    - [ ] Array
- [ ] Add function return values
- [ ] optimize rule usage
- [ ] optimize goal usage
- [ ] add predefined ai numbers

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
