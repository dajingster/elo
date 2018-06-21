# ImmortalElo

A web application hosted on heroku that users can use to create and maintain their own elo rating system for any 1 vs 1 activity, such as ping-pong, FIFA, or heads-up poker. As a chess player, this was inspired by the chess elo system and the algorithm behind it is virtually the same albeit less complicated regarding provisional players who just enter the system. 

## Getting Started

Register for an account at https://immortal-elo.herokuapp.com/. 

### Description

For every player in the system, the two basic statistics are their elo (or rating) and their consistency. Elo follows the traditional system and is a measurement of a player's skill - the higher the elo the better they are. For a more in-depth description of elo, visit https://en.wikipedia.org/wiki/Elo_rating_system. The one place where the algorithms used differ from traditional elo systems is in provisional elo - the elo when a player has just been entered into the system and has played few games. Traditional systems treat provisional elo differently, having it change wildly since their initial skill level is unknown. Immortal Elo removes this layer of complexity. 

A player's "consistency" is also measured, a metric that is not usually present in elo. Consistency is intended to be a measurement of how much a player deviates from their elo. It ranges from 0 (most inconsistent) to 1 (100% consisntent), and is calculated over the previous 5 games by averaging the difference between a player's actual performance and their expected performance and subtracting that from 1. If a player always performs precisely at what their elo indicates, they have a consistency close to 1, and if a player always performs either much better or worse, they have a consistency closer to 0. 

Finally, the total games played by each player is also kept track of. 

### Usage

The home page contains a table displaying every player, their rating, consistency, games played, and rank (by rating). The total number of players is shown in the player tab, and the averages for the three metrics are shown in their respective tabs as well. Clicking on those tabs reorders the players from highest to lowest by that metric, i.e. clicking on the consistency tab displays the players from highest to lowest by consistency. The search bar allows you to search for players by name. 

The result tab is where results are entered. Only one result can be entered at a time, and (currently) the system only allows for wins, losses, or draws (1, 0, 0.5). Enter it from the perspective of the first player. 

The player tab allows you to add and remove players from the system. Make sure no names are repeated. When removing players, remove only one at a time and simply enter their name. When adding players, add them by writing their name, :, initial rating. For example, the following "John: 1200". You can also enter multiple players by repeating the above format with commas to separate each player. 

The prediction tab allows you to enter two players and will give you a history of encounters between those two players and their probabilities for winning. 

The analysis tab allows you to analyze a specific player and see information about their playing statistics, rating history, and consistency history. 

The history tab has a full running history of all games played with the most recent at the top. The search bar allows you to search by name to see all games involving a certain player. The result is always from the perspective of player one. The in-depth box, when checked, allows you to see more information for every game. 

Finally, if you would like to change the password for your account, go to the change password tab. 

## Contribute

If you find issues, or simply want to contribute improvements, please feel free to clone, modify, test and send pull requests. You may also report issues in the issues tab of the repository on github. Since there are a lot of tabs and features, any feedback is greatly appreciated on any part of the application. 

### Potential Features
  1. Allowing users to choose their own K-factor for elo calculations.
  2. Have up and down arrows on the index page to see how recent results have impacted rankings.
  3. Introduce the option to remove a user account if desired. 
  
  
### Future Ideas

The implementation of the system on this website is intended to allow users to create their own easily manageable and easily usable elo system amongst a group of friends or acquitances. However, it is extremely limited in that the activity must be 1 vs 1 and the result can only be a win, loss or draw. Their are many possible routes to expand on this system, such as introducing other results that can occur, having a system for non zero-sum games like Hanabi, or activities that involve more than 2 players at a time such as any popular board game. Another idea would be a system for team activities where both individual and team ratings can exist, and where factors that introduce more complexity such as team chemistry may come into play. 
