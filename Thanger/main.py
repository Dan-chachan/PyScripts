#from kivy.app import App
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.label import Label
#from kivy.uix.textinput import TextInput
#from kivy.uix.colorpicker import ColorPicker

# TODO add user interface


#---------------------------------------------------------------
file_path = "/usr/share/themes/Numix-dark-master/gtk-2.0/gtkrc"
file = open(file_path, "r")

lines = file.readlines()

# Long string with HEX colors
line = lines[2]


# Start indexes of names colors to edit
nselected = line.find("nselected")
nlink = line.find("nlink")

# Move indexes to start of colors
""" TODO line[nselected:].find("#") """
while line[nselected] != "#":
    nselected += 1
while line[nlink] != "#":
    nlink += 1


def getValidInput():
    validChars = "ABCDEFabcdef1234567890"
    
    valid = False
    while not valid:
        color = input("\nEnter the new color in HEX format:\n\n> ")
        
        # Check the validity of chosen color
        if len(color) < 6:
            print("\nInvalid color\nToo short")
            continue

        valid = True
        start = 1 if (color[0] == "#") else 0  # skip optional hashtag at start
        for char in color[start:]:
            if char not in validChars:
                print("\nInvalid color\nBad chars")
                valid = False
                break
        
    if len(color) < 7 and valid:
        color = "#" + color
    print("\nColor OK")
    return color
        
color = getValidInput()

# Editing the line

firsthalf = line[0:nselected] + color
secondhalf = line[len(firsthalf):nlink] + color
end = line[len(secondhalf):]

newline = firsthalf + secondhalf + end

lines[2] = newline


# Overwriting the old file
file.close()

file = open(file_path, "w")

file.writelines(lines)
file.close()

print("\nDone!")

input(">")