#!/usr/bin/env python3

import subprocess, re, random, datetime

def statusCheck():
    """
    This function will run a status check on your nordvpn service to see if you are already connected.  You must be disconnected for this program to work. 
    """
    nord_output = subprocess.Popen(["nordvpn", "status"], stdout=subprocess.PIPE)
    status = re.split("[\r \n :]", nord_output.communicate()[0].decode("utf-8"))[-2]

    if status == "Disconnected":
        return True

    else:
        disconnect = input("You are currently connected to NordVPN already.  Would you like to disconnect and continue? [y/n]: ").lower()
        
        if disconnect == "y":
            subprocess.call(["nordvpn", "disconnect"])
            return True
        
        elif disconnect == "n":
            print("You have chosen not to disconnect from your current NordVPN session.  Exiting program...")
            exit()

def getCountries():
    """
    This function will return a list of the current countries with available servers for your nordvpn account.
    """
    nord_output = subprocess.Popen(["nordvpn", "countries"], stdout=subprocess.PIPE)
    countries = re.split("[\t \n]", nord_output.communicate()[0].decode("utf-8"))

    while "" in countries:
        countries.remove("")

    return countries

def chooseRandom(country_list):
    """
    This function will randomly choose a country out of the available countries list.
    """
    return country_list[random.randrange(0, len(country_list))]

def logIn(random_country):
    """
    This function will take the randomly chosen country and attempt to log in to NordVPN using that country.
    """
    print("{} has been selected as the random country.".format(random_country))
    
    subprocess.call(["nordvpn", "c", random_country])

def main():
    try:
        continuous_mode = input("Would you like to have this script continuously run and log in to random servers at random time intervals? [y/n]: ").lower()
        if continuous_mode == "y":
            try:
                randomized_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randrange(1,59))
                while True:
                    if datetime.datetime.now() >= randomized_time:
                        logIn(chooseRandom(getCountries()))
                        randomized_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randrange(1,59))
            
            except Exception as error:
                print("Error: {}".format(str(error)))

        elif continuous_mode == "n":
            print("This script will only run this one time.  If you want to choose another server at random then you will need to run the script again.")        
            
            if statusCheck():
                logIn(chooseRandom(getCountries()))

    except Exception as error:
        print("Error: {}".format(str(error)))

if __name__ == "__main__":
    main()




