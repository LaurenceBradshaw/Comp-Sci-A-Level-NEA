# Comp-Sci-A-Level-NEA
This was my college NEA project for 2022.
For the documentation that was uploaded as part of the course please see the README.docx file.

The idea behind this project was to create a framework that could be used by other programmers to model their own disease in their own hosts.
This meant that the framework needed to provide a structure for creating hosts and the disease and provide an easy script for running the model. To do this I created some abstract classes to be built upon by the user.

In the example use case of the framework I created, the hosts were in buildings that had different properties depending on the type of building. For example there were houses, offices and schools where during each timestep the hosts would move between them and mingle about spreading the disease.
As for the spacial scale in the example, it modeled cities in the UK. This was achieved by placing the buildings inside a city class that inherited from one of the abstract classes, and placing the cities into a country class that inheritied from the same abstract class. Using this method any users desired spacial scale could be modeled.
The disease in my example followed the SIR model where hosts were succeptible to the disease, then infected, and then removed for a period of time before becoming succeptible again. (Looking back at the code now it appears that the SIR functionality was hardcoded into the abstract class)
