import pandas as pd
import cricinfo_funcs as cf
import odds_funcs as of

# query parameters
#match_format = 'ODI'
#home_team = 'South Africa'
#away_team = 'Bangladesh'
#home_team_players = ['Q de Kock','JN Malan','T Bavuma','K Verreynne','HE van der Dussen','DA Miller','KA Maharaj','M Jansen','K Rabada','L Ngidi','T Shamsi']
#away_team_players = ['Tamim Iqbal','Liton Das','Shakib Al Hasan','Mushfiqur Rahim','Yasir Ali','Mahmudullah','Afif Hossain','Mehidy Hasan Miraz','Taskin Ahmed','Mustafizur Rahman','Shoriful Islam']

#match_format = 'Test'
#home_team = 'West Indies'
#away_team = 'England'
#home_team_players = ['KC Brathwaite','JD Campbell','NE Bonner','KR Mayers','J Blackwood','JO Holder','J da Silva','AS Joseph','KAJ Roach','V Permaul','JNT Seales']
#away_team_players = ['AZ Lees','Z Crawley','JE Root','DW Lawrence','JM Bairstow','BA Stokes','C Overton','BT Foakes','Saqib Mahmood','CR Woakes','MJ Leach']

match_format = 'ODI'
home_team = 'Pakistan'
away_team = 'Australia'
home_team_players = ['Imam-ul-Haq','Fakhar Zaman','Babar Azam','Mohammad Rizwan','Saud Shakeel','Iftikhar Ahmed','Khushdil Shah','Mohammad Wasim','Shaheen Shah Afridi','Zahid Mahmood','Haris Rauf']
away_team_players = ['AJ Finch','TM Head','BR McDermott','M Labuschagne','MP Stoinis','C Green','AT Carey','SA Abbott','NT Ellis','A Zampa','MJ Swepson']

#home_team = 'India'
#away_team = 'Sri Lanka'
#home_team_players = ['RG Sharma','MA Agarwal','SS Iyer','V Kohli','Shubman Gill','RR Pant','RA Jadeja','R Ashwin','Kuldeep Yadav','Mohammed Siraj','JJ Bumrah'] #,'Mohammed Shami'
#away_team_players = ['FDM Karunaratne','HDRL Thirimanne','P Nissanka','DM de Silva','AD Mathews','LD Chandimal','N Dickwella','RAS Lakmal','L Embuldeniya','MVT Fernando','CBRLS Kumara']

team_names = [home_team, away_team]
players = [home_team_players, away_team_players]
format_dict = {'Test': 'class=1', 'ODI': 'class=2', 'T20I': 'class=3', 'All': 'class=11'}
team_dict = {'England': 'team=1', 'Australia': 'team=2', 'South Africa': 'team=3', 'West Indies': 'team=4', 'New Zealand': 'team=5', 'India': 'team=6', 'Pakistan': 'team=7', 'Sri Lanka': 'team=8', 'Zimbabwe': 'team=9', 'Bangladesh': 'team=25', 'Afghanistan': 'team=40'}
format = format_dict.get(match_format)
teams = [team_dict.get(i)for i in team_names]

# get data
batting_data = cf.get_batting_stats(format, team_names, teams, [i for sublist in players for i in sublist])
bowling_data = cf.get_bowling_stats(format, team_names, teams, [i for sublist in players for i in sublist])


# calculate odds
top_batsman_odds = of.top_batsman_odds(batting_data, team_names)
top_bowler_odds = of.top_bowler_odds(bowling_data, team_names)
if (match_format=='ODI') | (match_format=='T20I'):
    most_sixes_odds = of.most_sixes_odds(batting_data, team_names)
player_runs_odds = of.player_runs_odds(batting_data, team_names)
player_wickets_odds = of.player_wickets_odds(bowling_data, team_names)

# save odds
with pd.ExcelWriter(home_team+'_vs_'+away_team+'_'+match_format+'_Odds.xlsx') as writer:

    top_batsman_odds[0].to_excel(writer, sheet_name=home_team + ' TopBat(1st)', index=False)
    top_batsman_odds[2].to_excel(writer, sheet_name=away_team + ' TopBat(1st)', index=False)
    top_batsman_odds[1].to_excel(writer, sheet_name=home_team + ' TopBat(2nd)', index=False)
    top_batsman_odds[3].to_excel(writer, sheet_name=away_team + ' TopBat(2nd)', index=False)

    top_bowler_odds[0].to_excel(writer, sheet_name=home_team + ' TopBowl(1st)', index=False)
    top_bowler_odds[2].to_excel(writer, sheet_name=away_team + ' TopBowl(1st)', index=False)
    top_bowler_odds[1].to_excel(writer, sheet_name=home_team + ' TopBowl(2nd)', index=False)
    top_bowler_odds[3].to_excel(writer, sheet_name=away_team + ' TopBowl(2nd)', index=False)

    player_runs_odds[0].to_excel(writer, sheet_name=home_team + ' PlyrRuns(1st)', index=False)
    player_runs_odds[2].to_excel(writer, sheet_name=away_team + ' PlyrRuns(1st)', index=False)
    player_runs_odds[1].to_excel(writer, sheet_name=home_team + ' PlyrRuns(2nd)', index=False)
    player_runs_odds[3].to_excel(writer, sheet_name=away_team + ' PlyrRuns(2nd)', index=False)

    player_wickets_odds[0].to_excel(writer, sheet_name=home_team + ' PlyrWkts(1st)', index=False)
    player_wickets_odds[2].to_excel(writer, sheet_name=away_team + ' PlyrWkts(1st)', index=False)
    player_wickets_odds[1].to_excel(writer, sheet_name=home_team + ' PlyrWkts(2nd)', index=False)
    player_wickets_odds[3].to_excel(writer, sheet_name=away_team + ' PlyrWkts(2nd)', index=False)

    if (match_format=='ODI') | (match_format=='T20I'):
        most_sixes_odds[0].to_excel(writer, sheet_name='6s - '+home_team+' batting first', index=False)
        most_sixes_odds[1].to_excel(writer, sheet_name='6s - '+away_team+' batting first', index=False)




## Player Names ##

# Tests
# ['RJ Burns','DP Sibley','JE Root','Z Crawley','BA Stokes','OJ Pope','JC Buttler','DM Bess','JC Archer','SCJ Broad','JM Anderson']
# ['KC Brathwaite','JD Campbell','SD Hope','SSJ Brooks','RL Chase','J Blackwood','SO Dowrich','JO Holder','AS Joseph','KAJ Roach','ST Gabriel']
# ['Shan Masood', 'Abid Ali', 'Azhar Ali', 'Babar Azam', 'Asad Shafiq', 'Fawad Alam', 'Mohammad Rizwan', 'Yasir Shah', 'Shaheen Shah Afridi', 'Mohammad Abbas', 'Naseem Shah']
# ['TWM Latham','HM Nicholls','LRPL Taylor','WA Young','BJ Watling','TA Blundell','DJ Mitchell','KA Jamieson','TG Southee','TA Boult','N Wagner']
# ['DA Warner','WJ Pucovski','SPD Smith','M Labuschagne','MS Wade','C Green','TD Paine','PJ Cummins','MA Starc','NM Lyon','JR Hazlewood']
# ['RG Sharma','Shubman Gill','CA Pujara','AM Rahane','GH Vihari','RR Pant','RA Jadeja','R Ashwin','NA Saini','Mohammed Siraj','JJ Bumrah']
# ['FDM Karunaratne','MDKJ Perera','BKG Mendis','LD Chandimal','AD Mathews','N Dickwella','MD Shanaka','PWH de Silva','MDK Perera','L Embuldeniya','RAS Lakmal']
# ['JM Bairstow','DP Sibley','JE Root','Z Crawley','SM Curran','DW Lawrence','JC Buttler','DM Bess','MJ Leach','MA Wood','JM Anderson']

# ['Babar Azam','Mohammad Rizwan','Fakhar Zaman','Shadab Khan','Asif Ali','Shoaib Malik','Mohammad Hafeez','Imad Wasim','Hasan Ali','Haris Rauf','Shaheen Shah Afridi']
# ['KS Williamson','TA Boult','MJ Guptill','GD Phillips','DP Conway','TA Boult','DJ Mitchell','JDS Neesham','MJ Santner','TG Southee','IS Sodhi','AF Milne']

# ODIs
# ['JJ Roy','JM Bairstow','JE Root','EJG Morgan','BA Stokes','JC Buttler','CR Woakes','LE Plunkett','JC Archer','AU Rashid','MA Wood']
# ['MJ Guptill','HM Nicholls','DP Conway','KS Williamson','LRPL Taylor','TWM Latham','JDS Neesham','C de Grandhomme','MJ Santner','MJ Henry','TA Boult','DJ Mitchell']
# ['DA Warner','AJ Finch','SPD Smith','M Labuschagne','MR Marsh','AT Carey','AC Agar','PJ Cummins','MA Starc','A Zampa','JR Hazlewood']
# ['S Dhawan','RG Sharma','MA Agarwal','V Kohli','SS Iyer','KL Rahul','HH Pandya','RA Jadeja','SN Thakur','YS Chahal','Mohammed Shami','JJ Bumrah','RR Pant','T Natarajan','B Kumar','R Ashwin', 'VR Iyer']
# ['Q de Kock','JN Malan','AK Markram','T Bavuma','JT Smuts','HE van der Dussen','K Verreynne','WD Parnell','DA Miller','H Klaasen','AL Phehlukwayo','KA Maharaj','L Ngidi','A Nortje','T Shamsi','D Pretorius','RR Hendricks','K Rabada','M Jansen']
# ['JJ Roy','JM Bairstow','JE Root','EJG Morgan','BA Stokes','JC Buttler','MM Ali','SW Billings','CR Woakes','AU Rashid','MA Wood','TK Curran','RJW Topley']
# ['E Lewis','D Bravo','DJ Bravo','SD Hope','J Mohammed','N Pooran','K Pollard','R Shepherd','JO Holder','F Allen','A Hosein','A Joseph']
# ['Tamim Iqbal','Liton Das','Soumya Sarkar','Mushfiqur Rahim','Mohammad Mithun','Mahmudullah','Mehidy Hasan Miraz','Mahedi Hasan','Taskin Ahmed','Mustafizur Rahman','Hasan Mahmud','Mohammad Naim','Mohammad Saifuddin']

# T20Is
# ['Babar Azam','Fakhar Zaman','Shadab Khan','Sarfraz Ahmed','Shoaib Malik','Mohammad Rizwan','Iftikhar Ahmed','Imad Wasim','Mohammad Amir','Abdullah Shafique','Mohammad Wasim','Nauman Ali','Sajid Khan','Wahab Riaz','Shaheen Shah Afridi','Asif Ali','Hasan Ali','Haris Rauf','Mohammad Hafeez','Zahid Mahmood','Khushdil Shah','Saud Shakeel']
# ['TWM Latham','HM Nicholls','KS Williamson','LRPL Taylor','BJ Watling','TA Blundell','KA Jamieson','TL Seifert','MJ Guptill','C de Grandhomme','GD Phillips','TD Astle','DP Conway','WA Young','MJ Henry','TA Boult','N Wagner','MS Chapman','FH Allen','DJ Mitchell','JDS Neesham','MJ Santner','TG Southee','KA Jamieson','LH Ferguson','IS Sodhi','AF Milne']
# ['ADS Fletcher','BA King','N Pooran','R Powell','RL Chase','SO Hetmyer','KA Pollard','SS Cottrell','KR Mayers','OF Smith','HR Walsh','FA Allen','O Thomas','NE Bonner','J da Silva','JNT Seales','V Permaul','KOK Williams','E Lewis','D Bravo','SD Hope','KC Brathwaite','JD Campbell','J Mohammed','R Shepherd','CH Gayle','RL Chase','AD Russell','DJ Bravo','JO Holder','AJ Hosein','R Rampaul']
# ['Q de Kock','T Bavuma','F du Plessis','HE van der Dussen','DA Miller','H Klaasen','AL Phehlukwayo','K Rabada','L Ngidi','A Nortje','T Shamsi','KA Maharaj','WD Parnell']
# ['JJ Roy','JC Buttler','DJ Malan','JM Bairstow','BA Stokes','EJG Morgan','MM Ali','CJ Jordan','AZ Lees','C Overton','BT Foakes','JM Vince','T Banton','PD Salt','Saqib Mahmood','LA Dawson','JC Archer','AU Rashid','MA Wood','TS Mills','LS Livingstone','JE Root','SW Billings','TK Curran','RJW Topley','Z Crawley','SM Curran','DW Lawrence','DM Bess','MJ Leach','JM Anderson','SCJ Broad','OJ Pope','OE Robinson','JR Bracey','DJ Willey','CR Woakes']
# ['MDKJ Perera','P Nissanka','HDRL Thirimanne','MD Shanaka','DM de Silva','KIC Asalanka','WIA Fernando','J Liyanage','PWH de Silva','PBB Rajapaska','C Karunaratne','MVT Fernando','PVD Chameera','M Theekshana','CBRLS Kumara','FDM Karunaratne','MD Gunathilaka','LD Chandimal','KNA Bandara','N Dickwella','MD Shanaka','L Embuldeniya','RAS Lakmal','JDF Vandersay']
# ['MS Wade','AJ Finch','SPD Smith','GJ Maxwell','BR McDermott','JP Inglis','MC Henriques','AT Carey','SA Abbott','NM Lyon','MA Starc','UT Khawaja','TM Head','A Zampa','JR Hazlewood','DA Warner','M Labuschagne','MR Marsh','AT Carey','AC Agar','PJ Cummins','MA Starc','KW Richardson','JA Richardson','DR Sams','WJ Pucovski','C Green','TD Paine','MP Stoinis','MJ Swepson']
# ['Mohammad Naim','Liton Das','Soumya Sarkar','Mushfiqur Rahim','Mohammad Mithun','Mahmudullah','Mehidy Hasan Miraz','Mahedi Hasan','Taskin Ahmed','Mustafizur Rahman','Mohammad Saifuddin','Shakib Al Hasan','Afif Hossain','Shoriful Islam','Shamim Hossain']
# ['S Dhawan','RG Sharma','KL Rahul','Shubman Gill','CA Pujara','V Kohli','AM Rahane','GH Vihari','RR Pant','SS Iyer','SV Samson','DJ Hooda','HH Pandya','Washington Sandar','DL Chahar','AR Patel','YS Chahal','B Kumar','Mohammed Shami','JJ Bumrah','SN Thakur','T Natarajan','RA Jadeja','R Ashwin','I Sharma','Mohammed Siraj','CV Varun','SA Yadav','Ravi Bishnoi','Avesh Khan']