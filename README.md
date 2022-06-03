# Analysis-of-the-location-of-abstract-spatial-figures
This repository contains a term paper on the topic "Analysis of the location of abstract spatial figures", the algorithm of which is based on Persistent homology. A piece of useless code is designed as a plug-in to the QGIS program.

Главный файл расположен в "serch for layer points.py"
Для его работы необходимы следующе файлы
1) "point_search.py"
2) "persistents_diagram.py"

Для работы персистентной гомологии необходимо установить на python(встроенный в qgis python) 
библиотеку gtda (ссылка на библиотеку https://github.com/giotto-ai/giotto-tda)

Также необходимо создание 2 слоев на карте persistents_lines и persistents_points. Эти слои промежуточные и при навыках владения поиска в программе
возможно переименование слоев.

Слои и результаты программы приведены в отдельных папках
