#------------------------------------------#
# Title: IO Classes
# Desc: A Module for IO Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# DOranski, 2020-Mar-22, Completed TODO items
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to run by itself')

import csv
import DataClasses as DC
import ProcessingClasses as PC

class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_name, lst_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)
        make_files(file_name): -> (creates csv files in current directory)

    """
    @staticmethod
    def save_inventory(file_name: list, lst_Inventory: list) -> None:
        """


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.
            lst_Inventory (list): list of CD objects.

        Returns:
            None.

        """
        file_name_CD = file_name[0]
        file_name_Tracks = file_name[1]
        try:
            with open(file_name_CD, 'w', newline = '') as csvfile:
                filewriter = csv.writer(csvfile, delimiter = ',')
                for disc in lst_Inventory:
                    row = [disc.cd_id, disc.cd_title, disc.cd_artist]
                    filewriter.writerow(row)
            with open(file_name_Tracks, 'w', newline = '') as csvfile:
                filewriter = csv.writer(csvfile, delimiter = ',')            
                for disc in lst_Inventory:
                    tracks = disc.cd_tracks
                    disc_id = disc.cd_id
                    for trk in tracks:
                        row = [disc_id, trk.track_id, trk.track_title, trk.track_length]
                        filewriter.writerow(row)
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def load_inventory(file_name: list) -> list:
        """


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.

        Returns:
            list: list of CD objects.

        """
        file_name_CD = file_name[0]
        file_name_Tracks = file_name[1]
        lst_Inventory = []
        cd = []
        try:
            with open(file_name_CD, 'r') as csvfile:
                invReader = csv.reader(csvfile, delimiter = ',')
                for row in invReader:
                    data = (','.join(row))
                    line = data.strip().split(',')
                    part = DC.CD(line[0], line[1], line[2])
                    lst_Inventory.append(part)
            with open(file_name_Tracks, 'r') as csvfile:
                trackReader = csv.reader(csvfile, delimiter = ',')
                for row in trackReader:
                    data = (','.join(row))
                    line = data.strip().split(',')
                    cd = PC.DataProcessor.select_cd(lst_Inventory, int(line[0]))
                    track = DC.Track(int(line[1]), line[2], line[3])
                    cd.add_track(track)
        except Exception as e:
            print()
            print("The file(s)", file_name[0], "and/or", file_name[1], "could not be loaded.")
            print("Either verify the file directory or use the main menu option \'m\' to create the files if they do not exist.")
        return lst_Inventory
        return cd
        
    @staticmethod
    def make_files(file_name: list):
        """
        
        
        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.
            
        Returns:
            None.
        
        """
        file_name_CD = file_name[0]
        file_name_Tracks = file_name[1]
        print()
        try:
            with open(file_name_CD, 'a') as csvfile:
                csv.writer(csvfile)
                print(file_name[0], "created successfully.")
            with open(file_name_Tracks, 'a') as csvfile:
                csv.writer(csvfile)
                print(file_name[1], "created successfully.")
        except Exception as e:
            print()
            print("The file(s)", file_name[0], "and/or", file_name[1], "could not be created.")
            print("Verify permissions on the current directory.")
            
            
class ScreenIO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nMain Menu\n\n[l] Load Inventory from File\n[a] Add CD / Album\n[d] Display Current Inventory')
        print('[c] Choose CD / Album\n[s] Save Inventory to File\n[m] Make Inventory Files\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, d, c, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'd', 'c', 's', 'm', 'x']:
            choice = input('Which operation would you like to perform? [l, a, d, c, s, m or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def print_CD_menu():
        """Displays a sub menu of choices for CD / Album to the user

        Args:
            None.

        Returns:
            None.
        """

        print('CD Sub Menu\n\n[a] Add Track\n[d] Display CD / Album Details\n[r] Remove Track\n[x] Exit to Main Menu')

    @staticmethod
    def menu_CD_choice():
        """Gets user input for CD sub menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices a, d, r or x

        """
        choice = ' '
        while choice not in ['a', 'd', 'r', 'x']:
            choice = input('Which operation would you like to perform? [a, d, r or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print(row)
        print('======================================')
        print()

    @staticmethod
    def show_tracks(cd):
        """Displays the Tracks on a CD / Album

        Args:
            cd (CD): CD object.

        Returns:
            None.

        """
        print('====== Current CD / Album: ======')
        print(cd)
        print('=================================')
        print(cd.get_tracks())
        print('=================================')
        print()

    @staticmethod
    def get_CD_info():
        """function to request CD information from User to add CD to inventory


        Returns:
            cdId (string): Holds the ID of the CD dataset.
            cdTitle (string): Holds the title of the CD.
            cdArtist (string): Holds the artist of the CD.

        """
        # Checks for an integer input
        while True:
            try:
                cd_id = int(input('Enter ID: ').strip())
                break
            except Exception as e:
                print(e)

        # Checks for a non-empty input
        while True:
            try:
                cd_title = input('What is the CD\'s title? ').strip()
                break
            except Exception as e:
                print(e)

        # Checks for a non-empty input
        while True:
            try:
                cd_artist = input('What is the Artist\'s name? ').strip()
                break
            except Exception as e:
                print(e)
        return cd_id, cd_title, cd_artist

    @staticmethod
    def get_track_info():
        """function to request Track information from User to add Track to CD / Album


        Returns:
            tracknum (string): Holds the ID of the Track dataset.
            tracktitle (string): Holds the title of the Track.
            tracklen (string): Holds the length (time) of the Track.

        """
        tracknum = input('What is the Track Number?: ').strip()
        tracktitle = input('What is the Track\'s title? ').strip()
        tracklen = input('What is the Track\'s length? ').strip()
        return tracknum, tracktitle, tracklen