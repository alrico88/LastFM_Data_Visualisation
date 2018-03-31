# LastFM_Data_visualisation
Welcome to Last.fm Data Visualiser!  
  
Before seeing your scrobbles come to life, go ahead and backup your scrobbles
with **LastFM_Backup.py** first. That downloads all the scrobbles from your Last.fm account into a .csv file.
There are a lot of tools to backup scrobbles into .csv, but I made my own because getting information
on the tags in a scrobble is pretty important to me. This is also the reason why the backup takes a lot
longer than other tools. But trust me, it's worthwhile! 
  
1. Go to https://www.last.fm/api/account/create to create an API account. Call the application whatever you want, leave the other boxes blank and click submit. And then, **copy the API key**.
2. Open **LastFM_Backup.py** with Notepad. Search for `YOUR_API_KEY` and replace it with the API KEY you obtained from step one.
3. Open command prompt in this directory and type in the command `pip install -r Requirements.txt`
4. To start the backup, open command prompt and type the command `python LastFM_Backup.py`.  
5. Input your last.fm username and number of pages to fetch per cycle (I suggest 1-4.This is to minimise the number of calls each cycle to prevent crashing.)
6. Be patient and wait for the backup to finish.    
If the program crashes, just restart the LastFM_Backup.py and it will finish off the backup.  

Once backup is done,
1. Type **jupyter notebook** in command prompt and open **data_visualiser.ipynb**.
2. Enter your Last.fm account username in **data_visualiser.ipynb**.
2. Go to https://plot.ly and sign up for an account. This is for plotting the interactive graph in this notebook.
3. Go to your plotly **account settings &rarr; API KEYS** and click **Regererate Key** to get an API KEY.
4. Enter the ploty information in **data_visualiser.ipynb**. 
5. (optional but **highly recommended**) To view an awesome dashboard of this notebook, go to http://jupyter-dashboards-layout.readthedocs.io/en/latest/getting-started.html and follow the installation and enabling instructions.
6. Run the code and change the view to dashboard preview.

The rest is pretty self explanatory. Have fun!
