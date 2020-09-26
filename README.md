To run the server locally, follow the steps below:
	** SETUP
	1. Install conda, create conda environment
		`brew cask install anaconda` (already done for Tae Kyu)
		`conda create --name calcutors_env` (^same)
	1.5. Activate environment (`conda activate caltutors_env`)
	2. run `conda install --file requirements.txt --channel conda-forge`

	** RUN WEBSITE LOCALLY
	3. Run `heroku local`. 
	   Note that your conda environment from (1) should be activated
	4. Terminal will spit out message along the lines of "Listening at: <url>",
	   open the URL at some internet browser!! :)  

Some notes:
	1. To update 'Teams' page, update the following: 
			caltutors/pages/views.py						| add new tutors' info
			caltutors/pages/templates/pages/team.html		| each row has 12 div's. No need to worry about the href, as long as views.py was completed
															| add `height = "150" width = "150"` when sourcing image in teams.html
			caltutors/CalTutors/static/img/team/			| crop picture to square and add to folder

