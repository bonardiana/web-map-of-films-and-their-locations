# Web-map-of-films-and-their-locations
This is a module for creating web art. The web map displays information about the places in which films were made depending on the year. The user specifies the year of the movie card which he wants to build and as a result he receives an HTML file with the map. The map consists of three layers: the locations of the films, the country in which the films were made and number of them and  third, the layer of the world map colored by population
# General structure
1. main.py -- Application runable file.
2. world.json -- File with information about countries .
3. README.md - file with descriptive information.
4. screenshots -- screenshots of web-maps.
5. locations.list.txt -- file with films and their locations.
# HTML structure
```<!DOCTYPE> ```	Defines the document type
```<head>```	Defines information about the document
```<title>```	Defines a title for the document
```<body>	```Defines the document's body
```<div>``` Sets separate partition of a document.
```<link>``` Establishes the connection with external document or webpage.
```<style>```	Defines style information for a document
```<script>```	Defines a client-side script
# Summary
## Layers
This web-map has three layers. Each of them you can view in screenshots
**Films** All the locations of films made in the marked year
**Countries** Countries in which those films were made colored by the number of films had been made there. 0-5 red, 5-10 orange, 10-20 yellow, 20-50 green, 50-100 blue, 100 and more - purpl.
**Population** Countries colored by their population. Less than 10000000 - green. 10000000-20000000 orange and more than 20000000 red. 
## Conclusion
Exploring this program you can lear a lot about the most popular places for film makinkg(NY, London). And about the most unpopular(Africa, Antarctida). Also you can learn that main locations doesn't change and stay popular. And the interesting fact is that there are a lot of film were made in a see or ocean.

