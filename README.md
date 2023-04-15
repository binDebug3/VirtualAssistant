<a name="readme-top"></a>

<div align="center">
    <h1 align="center">Lila</h1>
    <p align="center">
        A Language Interpretation and Learning Assistant by Dallin Stewart
    </p>
</div>

<hr>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#welcome">Welcome</a></li>
    <li><a href="#description">Description</a></li>
    <li><a href="#instructions">Instructions for Download</a></li>
    <li><a href="#use">Instructions for Use</a></li>
    <li><a href="#packages">Packages</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- Welcome -->
## Welcome

The Language Interpretation and Learning Assistant (Lila) is a customized virtual assistant inspired by Jarvis from 
Iron Man. Lila's main functionality is to interpret and respond to natural language commands to automate common and 
repetitive tasks. This project is named after <a href="https://www.bergepappassmith.com/obits/lila-jean-bringhurst/">
Lila Bringhurst</a> who was an amazing woman with an <a href="https://bringhurst-fusd-ca.schoolloop.com/">
elementary school</a> dedicated to her name.

<hr>

### Description

Lila has a lot of functionality built into her. She can:
- Greet the user
- Tell the time
- Tell the date
- Describe the weather in any location
- Tell jokes
- Report system status
- Report IP Address
- Open applications
- Answer questions using wikipedia
- Search the web
- Open any website
- Play any video on YouTube
- Use Google Maps
- Perform computations with Wolfram Alpha
- Take screenshots
- Interact with your to-do list using Todoist

Future functionality will include:
- Interacting with your calendar using Google Calendar
- Interacting with your email using Gmail
- Pushing and pulling code
- Running other custom programs
- Report on the news
- Engage in conversation


<hr>

### Instructions for Download
You'll need to start by downloading a few python packages in requirements.txt.

You can then <a href=https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository>
clone this project</a> to your own machine from GitHub and then run the webscraper in any Python development environment.

<p align="right">(<a href="#readme-top">top</a>)</p>

<hr>

### Instructions for Use
1. First clone the repo
2. Edit the config.py file and include the following in it:

   1. email = "<your_email>"
   2. email_password = "<your_email_password>"
   3. wolframalpha_id = "<your_wolframalpha_id>"
   4. todoist_api = "<your_todoist_api>"
3. Make a new python environment. If you are using anaconda just type 
   1. conda create -n jarvis python==3.8.5  in the anaconda prompt
      
4. To activate the environment 
   1. conda activate jarvis
5. Navigate to the directory of your project
6. Install all the requirements by just typing
   1. pip install -r requirements.txt
         
7. Install PyAudio from wheel file by following instructions given here
8. Run main.py

<p align="right">(<a href="#readme-top">top</a>)</p>

<hr>

<p align="right">(<a href="#readme-top">top</a>)</p>


<!-- CONTACT -->
## Contact

Dallin Stewart - dallinpstewart@gmail.com

[![LinkedIn][linkedin-icon]][linkedin-url]
[![GitHub][github-icon]][github-url]
[![Email][email-icon]][email-url]

<p align="right">(<a href="#readme-top">top</a>)</p>

<hr>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* <a href='https://github.com/Gladiator07/JARVIS'>Gladiator07</a> for the starting point for this project

<p align="right">(<a href="#readme-top">top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES for MACHINE LEARNING -->

[PyTorch-icon]: https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white
[PyTorch-url]: https://pytorch.org/


<!-- MARKDOWN LINKS & IMAGES for CONTACT -->

[linkedIn-icon]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedIn-url]: https://www.linkedin.com/in/dallinstewart/

[github-icon]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[github-url]: https://github.com/binDebug3

[Email-icon]: https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white
[Email-url]: mailto:dallinpstewart@gmail.com