#Odoo City_Zip_Area

#By Nikkocasa - 2017-2018


This module has been written to expand the functionality of contacts to constrain the zip code and name of cities as linked.
    - By choosing the postal code, you can constrain the list of cities on behalf of the corresponding cities.
    - The reverse functionality: by first selecting the name of the city, the ZIP list will be restricted to the corresponding ZIP codes.
The data model has been designed to take into account correctly the French territorial organization.
We hope that it can be adapted to other models.

Structure
=========

Table structure:

The relationship between cities and ZIP codes is of the 'Many2many' type
    - a city can have several ZIP codes,
    - a ZIP code can correspond to several cities.

A city is in a department (Area) that is in a region or state (state) of the existing core strucutre in Odoo 11 :

    - res.zip <--> res.city <-- res.country.state.area <-- res.country.state <-- res.country

The res.zip, res.city, and res.country.state.area tables contain some additional fields of information.

Configuration
=============

The installation of the module does not require any subsequent configuration.
It adds in the menu 'Localization' ('Localisation') the following menus:
    - Area ('Départements')
    - Cities ('Villes')
    - ZIP ('Code postaux')

Installing the app do not automatically upload data in tables.
    
Procedures for Importing Large Volume Data into City_zip
========================================================
 
A) Preparation of the data:

Since cities and ZIPs are usually large, it is best to cut files by size from approximately 5 to 10,000 records depending on the size of your memory installed on the server.
Imports of more than 30,000 registrations have been made without any problem on a server well equipped with memory and lightly loaded.

The module contains the following data in the data directory:

    - res.country.state.csv:    French regions (new organization 2015)
    - res.country.state.area:   French departments (linked to their new region)
    - res.zip.csv:              French postal codes (2016)
    - res.city.csv:             French cities (including overseas)
    
B) Loading data:

It is therefore ESSENTIALLY necessary to load the data in the following order:
- res.country: country (if there are new countries to add)
- res.country.state: states include a link to res.country
- res.country.state.area: Departments include a link to res.country.state
- res.zip: ZIP codes MUST BE loaded BEFORE CITIES (They are loaded without link information to the city table)
- res.city: you have to load the data last, which updates the Many2many link to the zip codes.

TODOs
=====
Next todo :

    - Add management of the address of the companies of the base
    - Cancel the function 'Create and modify' at the bottom of the drop-down list of the choice of postal rates of cities
    - Show the found items by filtering on the other list (city <==> ZIP)
    - Make better group filtering on access to the menu configuration
    - Add a 'country' list to the first input position to filter on the country

Bugs
====

https://github.com/nikkocasa/city_zip_constrains

