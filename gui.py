import sys
from sorter import MediaSorter
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class Gui(qtw.QDialog):
    def __init__(self):
        super().__init__()

        ##############
        # SETTING UI #
        ##############

        self.setWindowTitle("Photosort")
        grid_layout = qtw.QGridLayout()
        self.setLayout(grid_layout)

        icon = qtg.QIcon(":/icon/icon.jpeg")
        self.setWindowIcon(icon)

        ###########
        # BUTTONS #
        ###########

        self.from_path_btn = qtw.QPushButton("Välj sökväg")
        self.to_path_btn = qtw.QPushButton("Välj sökväg")
        self.run_btn = qtw.QPushButton("Kör!")
        self.run_btn.setDisabled(True)
        self.more_infoBtn = qtw.QPushButton("Mer information")
        self.more_infoBtn.setDisabled(True)

        #########
        # LABEL #
        #########

        # Choose path to sort media from
        self.from_description = qtw.QLabel("1. Välj sökväg att sortera från!")
        self.from_path_label = qtw.QLabel()
        self.from_path_label.setText("Sorterar från sökväg")
        self.from_path_label.setFixedSize(400, 15)
        self.count_images_label = qtw.QLabel("Antal bilder som hittades: ")
        self.count_images_amnt = qtw.QLabel()
        self.count_videos_label = qtw.QLabel("Antal videos som hittades: ")
        self.count_videos_amnt = qtw.QLabel()

        # Choose path to sort media to
        self.to_description = qtw.QLabel("2. Välj sökväg att sortera till!")
        self.to_path_label = qtw.QLabel()
        self.to_path_label.setText("Sorterar till sökväg")

        # Sorted photos and media
        self.sorted_images_label = qtw.QLabel("Antal bilder som sorterades: ")
        self.sorted_images_amnt = qtw.QLabel()
        self.sorted_videos_label = qtw.QLabel("Antal videos som sorterades: ")
        self.sorted_videos_amnt = qtw.QLabel()    

        #################
        # ADD TO LAYOUT #
        ################

        # Information label describing what to do (sort from)
        grid_layout.addWidget(self.from_description, 0, 1)
        # Choose path to search from button, and label
        grid_layout.addWidget(self.from_path_btn, 1, 1)
        grid_layout.addWidget(self.from_path_label, 1, 2)

        # Information label describing what to do (sort too)
        #grid_layout.addWidget(qtw.QLabel(), 2, 1)  # blank for padding
        grid_layout.addWidget(self.to_description, 2, 1)

        # Enter path to sort photos and media to
        grid_layout.addWidget(self.to_path_btn, 3, 1)
        grid_layout.addWidget(self.to_path_label, 3, 2)

        # Information displaying how many images was found in path
        grid_layout.addWidget(self.count_images_label, 4, 1)
        grid_layout.addWidget(self.count_images_amnt, 4, 2)

        # Information displaying how many videos was found in path
        grid_layout.addWidget(self.count_videos_label, 5, 1)
        grid_layout.addWidget(self.count_videos_amnt, 5, 2)

        
        # Run button for executing
        grid_layout.addWidget(self.run_btn, 7, 1)

        # Displaying amount of sorted photos and videos
        grid_layout.addWidget(self.sorted_images_label, 8, 1)
        grid_layout.addWidget(self.sorted_images_amnt, 8, 2)
        grid_layout.addWidget(self.sorted_videos_label, 9, 1)
        grid_layout.addWidget(self.sorted_videos_amnt, 9, 2)

        # Blank
        grid_layout.addWidget(qtw.QLabel(), 10, 1)

        # Infobutton 
        grid_layout.addWidget(self.more_infoBtn, 13, 1)
        
        
        ###########
        # ACTIONS #
        ###########
        # If path buttons was clicked
        self.from_path_btn.clicked.connect(self.set_from_path_label)
        self.to_path_btn.clicked.connect(self.set_to_path_label)

        # If run btn is clicked
        self.run_btn.clicked.connect(lambda: self.media_sorter_functions("run"))
        # if more info btn is clicked
        self.more_infoBtn.clicked.connect(self.more_info)

        ###########
        # EXECUTE #
        ###########

        self.show()

        ##############################
        # ATTRIBUTES FOR MEDIASORTER #
        ##############################
        self.media_src = ""
        self.media_dst = ""
        # Data with dictionary with files and folders to create
        #self.data = ""

    def set_from_path_label(self):
        path = qtw.QFileDialog.getExistingDirectory()
        if path:
            self.from_path_label.setText(path)
            # Initiate the MediaSorter class with src path
            # Populates count labels with amount of photos / videos
            self.count_images_populate()
            self.count_videos_populate()
            self.media_src = path
            
    def set_to_path_label(self):
        path = qtw.QFileDialog.getExistingDirectory()
        if path:
            self.to_path_label.setText(path)
            self.media_dst = path
            # Starts the sorting function to display amount of images and photos in src and dst
            self.media_sorter_functions()
    
    def open_src_path(self):
        """Opens the src path"""
        dialog = qtw.QFileDialog()
        nav_to_dialog = dialog.getExistingDirectory(directory=self.media_src)

            

    def count_images_populate(self):
        pass

    def count_videos_populate(self):
        pass

    def more_info(self):
        """Displays a new window with information
        about why some media did not get sorted."""
        # window
        win = qtw.QDialog()
        # layout
        win_layout = qtw.QVBoxLayout()
        win.setLayout(win_layout)

        # information
        win_label = qtw.QTextEdit()
        win_label.setReadOnly(True)
        win_label.setText(
            """Foton och bilder som inte sorterats saknar de attribut som behövs för att
skapa en sortering (ursprungsdatum). Dessa filer ligger därför kvar i den sökväg du valde att sortera ifrån.""")
        

        # Button
        # If pressed, opens the self.src provided path
        src_btn = qtw.QPushButton("Se media")

        # Add widget to window
        win_layout.addWidget(win_label)
        win_layout.addWidget(src_btn)

        src_btn.clicked.connect(self.open_src_path)

        win.exec()

    def media_sorter_functions(self, *run):
        """Initiates Mediasorter class and sorting function"""
        run_obj = MediaSorter(src=self.media_src, dst=self.media_dst)
        data = run_obj.get_photo_vid_md()
        # Loads the data to be sorted to the self.data attribute
        self.data = data[0]
    
        # Sets the amount of found images and videos
        self.count_images_amnt.setText(str(data[1]))
        self.count_videos_amnt.setText(str(data[2]))

        # Some files were not moved because of missing datetime attrib.
        # Actually moved files is below
        moved_photos = data[3]
        moved_videos = data[4]
        
        # Enables the run button
        self.run_btn.setDisabled(False)

        # Only creates dirrs and moves files to corr dirr if 
        # run command is provided
        if run:
            run_obj.create_dirrs_and_move_files(self.data)
            self.sorted_images_amnt.setText(str(moved_photos))
            self.sorted_videos_amnt.setText(str(moved_videos))

            # Enables more info button
            self.more_infoBtn.setEnabled(True)



if __name__ == "__main__":
    app = qtw.QApplication([sys.argv])
    gui = Gui()
    sys.exit(app.exec())
