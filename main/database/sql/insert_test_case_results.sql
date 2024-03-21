INSERT OR IGNORE INTO repository (id,name,url,number_of_followers,size,number_of_stars,number_of_contributors) VALUES
(26554,"reddit","https://api.github.com/repos/reddit-archive/reddit",16742,40093,16742,3),
(46939,"django-debug-toolbar","https://api.github.com/repos/jazzband/django-debug-toolbar",7853,7696,7853,3),
(54383,"gmate","https://api.github.com/repos/lexrupy/gmate",185,701,185,3),
(57419,"webpy","https://api.github.com/repos/webpy/webpy",5866,1752,5866,3),
(71978,"django-tagging-ng","https://api.github.com/repos/svetlyak40wt/django-tagging-ng",139,224,139,3),
(79012,"tdaemon","https://api.github.com/repos/brunobord/tdaemon",139,340,139,3),
(100428,"juno","https://api.github.com/repos/breily/juno",251,362,251,3),
(107258,"autojump","https://api.github.com/repos/wting/autojump",15850,801,15850,3),
(114508,"django-mediasync","https://api.github.com/repos/sunlightlabs/django-mediasync",173,1041,173,3),
(119609,"paramiko","https://api.github.com/repos/paramiko/paramiko",8749,8288,8749,3),
(143580,"django-cms","https://api.github.com/repos/django-cms/django-cms",9772,105063,9772,3);

INSERT or IGNORE INTO search (id,date,language,min_number_of_followers,max_number_of_followers,min_size,max_size,min_number_of_stars,max_number_of_stars,min_number_of_contributors,max_number_of_contributors) VALUES
(99999,"2024-03-12",2,2,null,100,null,30000,null,2,null);

INSERT OR IGNORE INTO search_repository (search, repository) VALUES 
(99999,26554),
(99999,46939),
(99999,54383),
(99999,57419),
(99999,71978),
(99999,79012),
(99999,100428),
(99999,107258),
(99999,114508),
(99999,119609),
(99999,143580);

INSERT OR IGNORE into result (id,search,repository,sqliv,number_of_followers,size,number_of_stars,number_of_contributors) VALUES
(10001,99999,26554,1,16742,40093,16742,3),
(10002,99999,46939,1,7853,7696,7853,3),
(10003,99999,54383,0,185,701,185,3),
(10004,99999,57419,0,5866,1752,5866,3),
(10005,99999,71978,0,139,224,139,3),
(10006,99999,79012,0,139,340,139,3),
(10007,99999,100428,0,251,362,251,3),
(10008,99999,107258,0,15850,801,15850,3);

INSERT OR IGNORE INTO sqliv_type (result,file_relative_repo,location) VALUES
(10001,"main/c1.py","10,1,10,5"),
(10001,"main/c2.py","10,1,10,5"),
(10002,"main/c3.py","10,1,10,5");


