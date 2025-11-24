Welcome in my Elo Rating Pictures program.Here are the important things you may know before running the program :

1.Dependencies
You need to run the program with an environnement and the requirements.txt installed.

2.Setup before using
You can just drag and drop the pictures you want to use in the pictures folder.
Then, run the dict_build.py file to initialize the Elo score.json file.

3.How to use
You can now run the choose_program.py file. It should open a window where you can directly choose your favorites images.

4.Configure
As you can see in the window, there is a listbox where you can choose the theme you are using. By default there are 4 themes.
You can change their name. You can also change their proprieties by changing the value of "background", "text", or "button".
You can also add your own theme in the "fenetre_theme" key.
You can customize the "elo_rating_coef". That will change the way the program calculates the elo score, and the highest the coefficient will be, the fastest the scores will change.
Finally, you can check all your pictures scores in the Elo scores.json file.

/!\ running the dict_build.py file will reinitialize the Elo score.json file
/!\ also make sure to add at least 3 pictures in the pictures folder or it will return an error when pressin the score button

P.S : the interface is in french
