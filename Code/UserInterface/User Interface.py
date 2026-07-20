# Imports all the necessary libraries
import pygame
import cv2
import numpy as np
import base64
import random
import os
os.environ['INSIGHTFACE_DISABLE_DOWNLOAD'] = '1'
os.environ["INSIGHTFACE_DISABLE_LOG"] = "1"
import insightface
from insightface.app import FaceAnalysis
import requests
import base64
import json
import face_recognition
import serial
import time

# Gets the module to initialize all of the necessary variables
pygame.init()

# Sets the title for the user interface
pygame.display.set_caption("Emergency Medical Assistant")

# Creates the screen of the user interface
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#disable logs
os.environ["INSIGHTFACE_DISABLE_LOG"] = "1"

# Timing variables
FPS = 35
fpsClock = pygame.time.Clock()

# Variables for blink animation
blinkTimer = 0
blinkVar = random.randint(30, 75) # Random intervals for blinking

# Stores screen dimensions 
sX, sY = screen.get_size()
screen = pygame.display.set_mode((sX, sY))

# Colour variables
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREEN = [36, 119, 119]
LIGHT_GREEN = [63, 163, 162]
DARK_GREEN = [28, 96, 96]
LIGHT_ORANGE = [243, 176, 135]
DARK_ORANGE = [234, 153, 103]

# Path to UI file
path = str("/home/sam/Desktop/PatientInformation") # Path for the folder

# Imports images 
eye = pygame.image.load("./Eyes.png")
smile = pygame.image.load("./Smile.png")
errorBox = pygame.image.load("./Error.png")
authErrorBox = pygame.image.load("./AuthError.png")
backButton = pygame.image.load("./BackButton.png")
great = pygame.image.load("./Great.png")
good = pygame.image.load("./Good.png")
meh = pygame.image.load("./Meh.png")
bad = pygame.image.load("./Bad.png")
terrible = pygame.image.load("./Terrible.png")
urineAnalysis = pygame.image.load("./UrineAnalysis.png")

# Program variables
screenColour = WHITE
displayScreen = 0
info = [] # Array that stores all of the patient's information to send to file
currentInput = '' # Stores the patient's input for the current question 
questionStatus = False
yesNoStatus = False
rateStatus = False
timeStatus = False
backBtnStatus = False
yesNoQuestions = "" # Stores the questions that are asked for the YES and NO function
question = "" # Stores the questions that are asked for the questions function

# Opens the video capture streams for the cameras
faceCapture = cv2.VideoCapture(2)
cap = cv2.VideoCapture(0)

# Sets up face identification
face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Draws the background rectangle
backBtnRect = pygame.Rect((50, 49.5), (50, 50))
pygame.draw.rect(screen, LIGHT_ORANGE, backBtnRect, border_radius=10)

FILENAME = "data.txt"
PORT = '/dev/ttyACM0' ##Arduino port on raspberry pi is: /dev/ttyACM0
BAUD = 115200
print(serial.__file__)
print(dir(serial))
arduino = serial.Serial(PORT, BAUD, timeout=1)

# Send message to the arduino
def send(text):
    with open(FILENAME, "w") as f:
        f.write(text)

# Idle function for when the robot is not assisting a patient
def idle():
    global blinkTimer
    global blinkVar

    if (blinkTimer%blinkVar) == 0:
        eyeType = pygame.transform.scale(eye,(200,25)) # Blink animation for the eyes 
        blinkVar = random.randint(30, 75)
        blinkTimer = 0
    else: 
        eyeType = pygame.transform.scale(eye,(200,225)) # Sets the size of the eye

    eyeRect = eyeType.get_rect()
    eyeRect.center = (sX/2-150,sY/2-75) # Positioning of the left eye
    screen.blit(eyeType,eyeRect)
    eyeRect.center = (sX/2+150,sY/2-75) # Positioning of the right eye
    screen.blit(eyeType,eyeRect)
    smileType = pygame.transform.scale(smile,(150,225)) # Sets the size of the mouth
    smileRect = smileType.get_rect()
    smileRect.center = (sX/2+5,sY/2+75) # Positioning of the smile
    screen.blit(smileType, smileRect)
    
# Function for color detection
def findcolor(high,low,color,imageFrame):
    # Convert BGR to HSV colorspace
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color 
    red_lower = np.array(low, np.uint8)
    red_upper = np.array(high, np.uint8)
    
    # Defines the mask for the colour detection
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Used to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # Sets the red colour
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 600):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),(int((high[0]+low[0])/2), int((high[1]+low[1])/2), int((high[2]+low[2])/2)), 2)
            cv2.putText(imageFrame, str(color), (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(int((high[0]+low[0])/2), int((high[1]+low[1])/2), int((high[2]+low[2])/2)))
    
    # Displays the frames 
    frames = np.rot90(imageFrame) # Rotate the frame
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
    display = pygame.surfarray.make_surface(frames)
    display = pygame.transform.flip(display,True,False)
    display = pygame.transform.scale(display,(sX,sY))
    rect = display.get_rect()
    rect.center = (sX/2 , sY/2)
    screen.blit(display,rect)
    
    # Render text
    camTextSurface = font.render("Press the Spacebar When Ready", True, WHITE)
    camTextRect = camTextSurface.get_rect()
    camTextRect.center = (sX/2,sY/4*3) # Positions the text
    screen.blit(camTextSurface,camTextRect)

# Initialize FaceAnalysis model
app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))

# Function to get face embedding
def get_embedding(frame):
    if frame is None:
        raise ValueError("Empty frame provided.")
    
    faces = app.get(frame)
    if len(faces) == 0:
        raise ValueError("No face detected in frame.")
    
    return faces[0].embedding
    
# Function to compare embeddings
def faceCheck(img1_path, img2_path, threshold=0.8):
    
    emb1 = get_embedding(img1_path)
    emb2 = get_embedding(img2_path)

    # Cosine similarity
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    print(f"Similarity Score: {similarity:.4f}")
    if similarity > threshold:
        print("✅ Faces match!")
        return 5
    else:
        print("❌ Faces do not match.")
        return 3

# Make file function that runs at the beginning of the program to make a folder for each patient 
def makeFile():
    global info
    global fullPath
    
    fullPath = os.path.join(path,str(info[1])) # Creates patient folder (name)
    if not os.path.exists(fullPath): # Checks whether the patient is a pre-existing patient
        try:
            os.makedirs(fullPath) # If the patient is new, it creates a new folder 
            print(f"Directory '{str(info[1])}' created successfully.")
        except FileExistsError:
            print(f"Directory '{str(info[1])}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{str(info[1])}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Save file function for when the patient's information has to be saved in their file 
def saveFile(fileName):
    global info
    global fullpath
    
    fullPath = os.path.join(path,str(info[1])) # Creates patient folder (name)
    patientFilePath = os.path.join(fullPath, fileName) # Creates data file to save the patient's information
     
    with open(patientFilePath, "w") as file: # Opens the data file 
        file.write("Name: " + str(info[1]) + "\n") # Writes the patient's name
        file.write("DOB: (dd/mm/yyyy): " + str(info[3]) + "\n") # Writes the patient's DOB
        
        infoLength = len(info) # Returns the length of the info array
        for data in range(4, infoLength-1, 2): # Loops through the questions in the info array not including the patient's name and DOB
            file.write(str(info[data] + " " + str(info[data+1])) + "\n") # Writes all of the questions followed by their corresponding answers into the file
            
    file.close() # Closes the patients file

# User type function to verify which type of user the patient is (New or Returning)
def userType():
    global userYesRect
    global userNoRect
    
    # Renders question
    userTypeSurface = font.render("Are You A New Patient?", True, BLACK)
    userTypeRect = userTypeSurface.get_rect()
    userTypeRect.center = (sX/2,sY/2-115) # Positions the question
    screen.blit(userTypeSurface,userTypeRect)

    # Sets up the YES and NO buttons 
    userYesRect = pygame.Rect((sX/2-200, sY/2), (150, 75))
    userNoRect = pygame.Rect((sX/2+50, sY/2), (150, 75))

    # Renders the buttons
    pygame.draw.rect(screen, GREEN if userYesRect.collidepoint(mouse_pos) else DARK_GREEN, userYesRect, border_radius=15)
    pygame.draw.rect(screen, LIGHT_ORANGE if userNoRect.collidepoint(mouse_pos) else DARK_ORANGE, userNoRect, border_radius=15)

    # Sets up button text
    userYesText = font.render("Yes", True, BLACK)
    userNoText = font.render("No", True, BLACK)

    # Renders the button text
    screen.blit(userYesText, (userYesRect.centerx - userYesText.get_width() // 2, userYesRect.centery - userYesText.get_height() // 2))
    screen.blit(userNoText, (userNoRect.centerx - userNoText.get_width() // 2, userNoRect.centery - userNoText.get_height() // 2))

# Camera function for when the robot has to open the video capture stream
def camera(camText):
    global faceFrame 
    
    # Reads frames from the video capture
    ret, faceFrame = faceCapture.read(2)
    frames = np.rot90(faceFrame) # Rotates the frame
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB) # Sets the RBG colourspace
    display = pygame.surfarray.make_surface(frames)
    display = pygame.transform.scale(display,(sX,sY)) # Scales the video capture stream to the entire screen 
    rect = display.get_rect()
    rect.center = (sX/2,sY/2)
    screen.blit(display,rect)

    # Render text
    camTextSurface = font.render(camText, True, WHITE)
    camTextRect = camTextSurface.get_rect()
    camTextRect.center = (sX/2,sY/4*3) # Positions the text
    screen.blit(camTextSurface,camTextRect)

# Data entry error function for when the patient attempts to skip a mandatory question
def error():
    errType = pygame.transform.scale(errorBox,(485,223)) # Sets the size of the error box
    errRect = errType.get_rect()
    errRect.center = (sX/2+5,sY/2) # Positioning of the error box
    screen.blit(errType, errRect)        
    pygame.display.update()
    pygame.time.delay(1750)

# Authorization error function for when the patient's identity authorization fails
def authError():
    authErrType = pygame.transform.scale(authErrorBox, (485, 450)) # Sets the size of the error box
    authErrRect =  authErrType.get_rect()
    authErrRect.center = (sX/2+5, sY/2) # Positioning of the error box
    screen.blit(authErrType, authErrRect)
    pygame.display.update()
    pygame.time.delay(1750)

# Instructions pages function for when the patient must read the instructions
def instructions(instructionPage):
    global instructionBtnRect
    global instructionRect
    
    # Sets the size and position of the instructions page and draws it (MUST BE CHANGED)
    instructionType = pygame.transform.scale(instructionPage,(sX, sY))
    instructionRect = instructionType.get_rect()
    instructionRect.center = (sX/2,sY/2) 
    screen.blit(instructionType, instructionRect)   
    
    # UNDERSTOOD button setup
    uButtonWidth, uButtonLength = 175, 50
    instructionBtnRect = pygame.Rect(sX/2-uButtonWidth/2, sY/2+150, uButtonWidth, uButtonLength)
    uButtonColour = WHITE # Sets the colour of the UNDERSTOOD button
    uButtonText = font.render("I Understand", True, LIGHT_GREEN) # Sets up the text in the UNDERSTOOD button

    # Render Enter button with rounded corners
    pygame.draw.rect(screen, BLACK if instructionBtnRect.collidepoint(mouse_pos) else uButtonColour, instructionBtnRect, border_radius=10)
    screen.blit(uButtonText, (instructionBtnRect.x + (uButtonWidth - uButtonText.get_width()) // 2, instructionBtnRect.y + (uButtonLength - uButtonText.get_height()) // 2))

# Back button function for when the patient would like to re-enter data
def backBtn():
    global backRect
        
    # Draws the background rectangle
    backBtnRect = pygame.Rect((50, 49.5), (50, 50))

    # Renders the button
    pygame.draw.rect(screen, LIGHT_ORANGE if backBtnRect.collidepoint(mouse_pos) else WHITE, backBtnRect, border_radius=10)
    
    backType = pygame.transform.scale(backButton, (75, 75)) # Sets the size of the back button
    backRect = backType.get_rect()
    backRect.center = (75,75) # Positioning of the back button
    screen.blit(backType, backRect) # Displays the back button

# Question function for when the robot is asking the patient for information
def questions(question):
    global buttonRect
    global questionStatus
    global currentInput

    questionStatus = True

    # Sets up the input text that the patient enters
    textSurface = font.render(currentInput, True, BLACK) # Sets the colour of the text
    textRect = textSurface.get_rect()
    textRect.center = (sX/2, sY/2) # Sets the position of the text
    screen.blit(textSurface, textRect)

    # Render question
    questionSurface = font.render(question, True, BLACK)
    questionRect = questionSurface.get_rect()
    questionRect.center = (sX/2,sY/2-115) # Positions the question
    screen.blit(questionSurface,questionRect)

    # Enter button setup
    buttonWidth, buttonLength = 120, 50
    buttonRect = pygame.Rect(sX/2-buttonWidth/2, sY/2+150, buttonWidth, buttonLength)
    buttonColour = LIGHT_GREEN # Sets the colour of the ENTER button
    buttonText = font.render("Enter", True, WHITE) # Sets up the text in the ENTER button

    # Render Enter button with rounded corners
    pygame.draw.rect(screen, BLACK if buttonRect.collidepoint(mouse_pos) else buttonColour, buttonRect, border_radius=10)
    screen.blit(buttonText, (buttonRect.x + (buttonWidth - buttonText.get_width()) // 2, buttonRect.y + (buttonLength - buttonText.get_height()) // 2))

# Function that allows the patients to pick a unit of time
def durationQuestion():
    global timeStatus
    global hoursRect
    global daysRect
    global weeksRect

    timeStatus = True

    # Sets up the buttons
    buttonWidth, buttonLength = 120, 50
    hoursRect = pygame.Rect(sX/2-buttonWidth/2-200, sY/2+90, buttonWidth, buttonLength)
    daysRect = pygame.Rect(sX/2-buttonWidth/2, sY/2+90, buttonWidth, buttonLength)
    weeksRect = pygame.Rect(sX/2-buttonWidth/2+200, sY/2+90, buttonWidth, buttonLength)

    # Sets up the button text
    timeColour = LIGHT_ORANGE # Sets the colour of the buttons
    hoursText = font.render("Hours", True, WHITE) # Sets up the text in the hours button
    daysText = font.render("Days", True, WHITE) # Sets up the text in the days button
    weeksText = font.render("Weeks", True, WHITE) # Sets up the text in the weeks button

    # Renders the 3 buttons
    pygame.draw.rect(screen, BLACK if hoursRect.collidepoint(mouse_pos) else timeColour, hoursRect, border_radius=10)
    screen.blit(hoursText, (hoursRect.x + (buttonWidth - hoursText.get_width()) // 2, hoursRect.y + (buttonLength - hoursText.get_height()) // 2))
    
    pygame.draw.rect(screen, BLACK if daysRect.collidepoint(mouse_pos) else timeColour, daysRect, border_radius=10)
    screen.blit(daysText, (daysRect.x + (buttonWidth - daysText.get_width()) // 2, daysRect.y + (buttonLength - daysText.get_height()) // 2))
    
    pygame.draw.rect(screen, BLACK if weeksRect.collidepoint(mouse_pos) else timeColour, weeksRect, border_radius=10)
    screen.blit(weeksText, (weeksRect.x + (buttonWidth - weeksText.get_width()) // 2, weeksRect.y + (buttonLength - weeksText.get_height()) // 2))

# yesNo function to set up the yes or no questions for the patients
def yesNo(yesNoQuestions):
    global understoodRect
    global yesNoStatus
    global yesRect
    global noRect

    yesNoStatus = True

    # Sets up the YES and NO buttons 
    yesRect = pygame.Rect((sX/2-200, sY/2), (150, 75))
    noRect = pygame.Rect((sX/2+50, sY/2), (150, 75))

    # Renders the buttons
    pygame.draw.rect(screen, GREEN if yesRect.collidepoint(mouse_pos) else DARK_GREEN, yesRect, border_radius=15)
    pygame.draw.rect(screen, LIGHT_ORANGE if noRect.collidepoint(mouse_pos) else DARK_ORANGE, noRect, border_radius=15)

    # Sets up button text
    yesText = font.render("Yes", True, BLACK)
    noText = font.render("No", True, BLACK)

    # Renders the button text
    screen.blit(yesText, (yesRect.centerx - yesText.get_width() // 2, yesRect.centery - yesText.get_height() // 2))
    screen.blit(noText, (noRect.centerx - noText.get_width() // 2, noRect.centery - noText.get_height() // 2))

    # Render question
    questionSurface = font.render(yesNoQuestions, True, BLACK)
    questionRect = questionSurface.get_rect()
    questionRect.center = (sX/2,sY/2-115) # Positions the question
    screen.blit(questionSurface,questionRect)

# Rate function that allows the user to rate how they are feeling overall
def rateFeeling():
    global rateStatus
    global greatRect
    global goodRect
    global mehRect
    global badRect
    global terribleRect

    rateStatus = True

    # Render question
    rateSurface = font.render("Please Rate How You Are Feeling Overall:", True, BLACK)
    rateRect = rateSurface.get_rect()
    rateRect.center = (sX/2,sY/2-115) # Positions the question
    screen.blit(rateSurface,rateRect)

    # Sets the size and position of the great icon and draws it
    greatType = pygame.transform.scale(great,(135, 135))
    greatRect = greatType.get_rect()
    greatRect.center = (sX/2+300,sY/2) 
    screen.blit(greatType, greatRect)    

    # Sets the size and position of the great icon and draws it
    goodType = pygame.transform.scale(good,(135, 135)) 
    goodRect = goodType.get_rect()
    goodRect.center = (sX/2+150,sY/2) 
    screen.blit(goodType, goodRect)  

    # Sets the size and position of the meh icon and draws it
    mehType = pygame.transform.scale(meh,(135, 135))
    mehRect = mehType.get_rect()
    mehRect.center = (sX/2+5,sY/2) 
    screen.blit(mehType, mehRect)  

    # Sets the size and position of the bad icon and draws it
    badType = pygame.transform.scale(bad,(135, 135))
    badRect = badType.get_rect()
    badRect.center = (sX/2-150,sY/2) 
    screen.blit(badType, badRect)  

    # Sets the size and position of the terrible icon and draws it
    terribleType = pygame.transform.scale(terrible,(135, 135))
    terribleRect = terribleType.get_rect()
    terribleRect.center = (sX/2-300,sY/2) 
    screen.blit(terribleType, terribleRect)   

# Check what the arduino is giving
def ard():
    arduino = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # wait for Arduino reset
    print("Connected to Arduino. Sending file contents...")

    with open(FILENAME, 'r') as f:
        for line in f:
            msg = line.strip()
            if msg:
                arduino.write((msg + '\n').encode())
                time.sleep(0.1)
                print(msg)

    print("File sent. Keeping connection open so Arduino can keep running.")
    try:
        
        if arduino.in_waiting:
            print(arduino.readline().decode(errors='ignore').strip())
            beat = ("Arduino: ", arduino.readline().decode(errors='ignore').strip())

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Exiting.")
    print(beat)
    return beat

quitVar = True

# History with diabetes variable
history = False

tf = False

# Creates the interface loop
while quitVar == True:
    
    # Gets the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Sets the background colour for the screen
    screen.fill(screenColour)
    
    # Sets the font for the text
    font = pygame.font.Font("./Poppins-Medium.ttf", 20)

    # Controls the displaying of the back button
    if backBtnStatus == True:
        backBtn()

    # Display screens that interact with the patient to ask questions
    if displayScreen == 0:
        # send("idle")
        # be = ard()
        backBtnStatus = False
        history = False
        color_timer=0
        idle()
        blinkTimer += 1

    # Questions to check if the patient is a new patient
    elif displayScreen == 40:
        yesNoStatus = False
        backBtnStatus = False
        userType()

    elif displayScreen == 41:
        backBtnStatus = True
        question = "What is Your Full Name?"
        questions(question)
        
    elif displayScreen == 42:
        backBtnStatus = True
        question = "Enter Your Date of Birth (dd/mm/yyyy):"
        questions(question)

    elif displayScreen == 43:
        question = "Describe Your Current Situation:"
        questions(question)

    elif displayScreen == 44:
        backBtnStatus = False
        
        cv2.destroyAllWindows
        saveFile("patientRevisit.txt") # Runs the function to save all of the patients information in their designated folder
        displayScreen = 0 # Resets the user interface to the beginning for the next patient
        info = [] # Resets the info array for the next patient
    
    # Questions for new patients
    elif displayScreen == 1:
        backBtnStatus = True
        question = "What is Your Full Name?"
        questions(question)

    elif displayScreen == 2:
        makeFile()
        question = "Enter Your Date of Birth (dd/mm/yyyy):"
        questions(question)
        
    elif displayScreen == 3:
        backBtnStatus = False
        camera("Press the Spacebar When Ready to Scan ID")

    elif displayScreen == 4:
        camera("Press the Spacebar When Ready to Scan Face")
        pathcheck = True

    elif displayScreen == 5:
        backBtnStatus = False
        displayScreen = faceCheck(path1, path2)
        print(displayScreen)
        
        # Saves the image using cv2.imwrite()
        if pathcheck:
            cv2.imwrite(pathId, path1)
            cv2.imwrite(pathFace, path2)
            pathcheck = False
        if displayScreen == 5:
            backBtnStatus = False
            rateFeeling()

    elif displayScreen == 6:
        backBtnStatus = True
        yesNoQuestions = "Are You Having Difficulty Breathing?"
        tf = True
        yesNo(yesNoQuestions)

    elif displayScreen == 7:
        yesNoQuestions = "Do You Have Any Chest Pain?"
        yesNo(yesNoQuestions)

    elif displayScreen == 8:
        yesNoQuestions = "Do You Have a History of Heart Attack/Angina?"
        yesNo(yesNoQuestions)
        timeStatus = False
        
    elif displayScreen == 9: 
        question = "How Long Has This Been Occurring?"
        questions(question)
        durationQuestion()

    elif displayScreen == 10:
        timeStatus = False
        yesNoQuestions = "Are You Bleeding or do You Have any Visible Wounds?"
        yesNo(yesNoQuestions)

    elif displayScreen == 11:
        question = "Where Are You Bleeding?"
        questions(question)

    elif displayScreen == 12:
        question = "How Long Have You Been Bleeding?"
        questions(question)
        durationQuestion()
    
    elif displayScreen == 13:
        yesNoQuestions = "Have You Fainted or Lost Consciousness Within the Last 24 Hours?"
        yesNo(yesNoQuestions)

    elif displayScreen == 14:
        question = "When Did You Last Lose Consciousness?"
        questions(question)
        durationQuestion()

    elif displayScreen == 15:
        question = "How Long Did You Last Lose Consciousness for?"
        questions(question)
        durationQuestion()

    elif displayScreen == 16:
        yesNoQuestions = "Do You Have a Medical Condition Related to This?"
        yesNo(yesNoQuestions)

    elif displayScreen == 17:
        question = "What Medical Condition do You Have?"
        questions(question)

    elif displayScreen == 18:
        yesNoQuestions = "Do You Feel Dizzy or Lightheaded?"
        yesNo(yesNoQuestions) 

    elif displayScreen == 19:
        question = "How Long Have You Been Feeling Dizzy or Lightheaded?"
        questions(question)
        durationQuestion()

    elif displayScreen == 20:
        yesNoQuestions = "Do You Have a Fever, Chills, or Sweating?"
        yesNo(yesNoQuestions)

    elif displayScreen == 21:
        question = "How Long Have You Been Experiencing This?"
        questions(question)
        durationQuestion()

    elif displayScreen == 22:
        yesNoQuestions = "Are You Taking Any Medication?"
        yesNo(yesNoQuestions)

    elif displayScreen == 23:
        question = "What Medication Are You Taking?"
        questions(question)

    elif displayScreen == 24:
        question = "What is the Reason For the Medication?"
        questions(question)

    elif displayScreen == 25:
        yesNoQuestions = "Do You Have Any Allergies?"
        yesNo(yesNoQuestions)

    elif displayScreen == 26:
        question = "Please List Your Allergies:"
        questions(question)

    elif displayScreen == 27: 
        yesNoQuestions = "Have You Been Exposed to any of Your Allergens Within the Past 24 Hours?"
        yesNo(yesNoQuestions)

    elif displayScreen == 28:
        yesNoQuestions = "Do You Have Diabetes/Family History of Diabetes?"
        yesNo(yesNoQuestions)

    elif displayScreen == 29:
        yesNoQuestions = "Do You Have a History of Urinary Disease?"
        yesNo(yesNoQuestions)

    elif displayScreen == 30:
        backBtnStatus = True
        question = "Please List Any Other Signs/Symptoms You are Experiencing:"
        questions(question)

    elif displayScreen == 31:
        backBtnStatus = False
        if info[-3] == "Yes" or info[-5] == "Yes": # Diabetes or Urinary disease
            instructions(urineAnalysis)
        else: # If the instructions do not need to be displayed for the urine testing
            backBtnStatus = False
            cv2.destroyAllWindows
            saveFile("data.txt") # Runs the function to save all of the patients information in their designated folder
            displayScreen = 0 # Resets the user interface to the beginning for the next patient
            info = [] # Resets the info array for the next patient

    elif displayScreen == 32:
        faceCapture.release()
        
        if info[-3] == "Yes" or info[-5] == "Yes": # Diabetes or Urinary disease
            
            backBtnStatus = False
            # Reads the urine analysis frame from the camera
            ret, urineFrame = cap.read() 
                    
            # Convert the frame from BGR to HSV color space
            hsv_frame = cv2.cvtColor(urineFrame, cv2.COLOR_BGR2HSV) 
            blurred_image = cv2.GaussianBlur(urineFrame, (5, 5), 100000000) # Blurs the frame so that the colour can be detected more accurately
            
            # YELLOW
            lightYellowLow = [22, 80, 140]
            lightYellowHigh = [30, 145, 190]
            findcolor(lightYellowHigh, lightYellowLow, "light yellow",blurred_image)

            darkYellowLow = [15, 80, 110]
            darkYellowHigh = [22, 175, 155]
            findcolor(darkYellowHigh, darkYellowLow, "dark yellow",blurred_image)

            # GREEN
            lightGreenLow = [29, 54, 85]
            lightGreenHigh = [100,255, 130]
            findcolor(lightGreenHigh, lightGreenLow, "light green",blurred_image)
            
            lower_color1 = np.array([0, 0, 0])
            upper_color1 = np.array([255, 255, 255])
            mask = cv2.inRange(hsv_frame, lower_color1, upper_color1)
            result = cv2.bitwise_and(urineFrame, urineFrame, mask=mask)
            send("urine")
            
        else:
            backBtnStatus = False
            cv2.destroyAllWindows
            saveFile("data.txt") # Runs the function to save all of the patients information in their designated folder
            info = [] # Resets the info array for the next patient 
            displayScreen = 33 # Moves to the heartbeat and vitals monitoring screen
        
    elif displayScreen == 33:
        send("vitals")
        vitalsText = font.render("Please place your finger on the indicated surface", True, BLACK)
        vitalsRect = vitalsText.get_rect()
        vitalsRect.center = (sX/2,sY/2-150) # Position
        screen.blit(vitalsText,vitalsRect)
            
        vitalsStatus = True

    else:
        backBtnStatus = False
        cv2.destroyAllWindows
        saveFile("data.txt") # Runs the function to save all of the patients information in their designated folder
        displayScreen = 0 # Resets the user interface to the beginning for the next patient
        info = [] # Resets the info array for the next patient

    # Checks for events while the interface is running
    for event in pygame.event.get():
        # Gets mouse position
        position = pygame.mouse.get_pos()
        # Controls the keyboard inputs from the patients 
        if event.type == pygame.KEYDOWN:
            # Checks if the patient is trying to save a picture of the ID card
            if displayScreen == 3:
                if event.key == pygame.K_SPACE:                    
                    # Defines the full file path (directory + filename)
                    idPath = os.path.join(fullPath, "idImage.jpg")
                    pathId = idPath
                    path1 = faceFrame
                    
                    displayScreen += 1 # Moves to the next display screen   
                    
            # Checks if the patient is trying to save a picture of their face
            elif displayScreen == 4: 
                if event.key == pygame.K_SPACE:
                    # Defines the full file path (directory + filename)
                    facePath = os.path.join(fullPath, "faceScan.jpg")
                    pathFace = facePath
                    path2 = faceFrame
                    
                    displayScreen += 1 # Moves to the next display screen
            
            elif displayScreen == 32:
                if event.key == pygame.K_SPACE:
                    # Defines the full file path (directory + filename)
                    urineTestPath = os.path.join(fullPath, "urineTest.jpg")
                    
                    # Saves the image using cv2.imwrite()
                    cv2.imwrite(urineTestPath, urineFrame)
                    
                    displayScreen += 1 # Moves to the next display screen
                
            # Checks if the patient is entering an input
            elif questionStatus == True:
                # Checks if the user is trying to enter and save the data
                if event.key == pygame.K_RETURN:
                    if currentInput == "" or currentInput == " ": # Checks if patient did not input any information
                        error() # Runs the error function to display the error message
                        print(currentInput + "q stat")
                    else:
                        info.append(question) # Appends the question into the array
                        info.append(currentInput) # Appends the current input and stores it in the info array
                        currentInput = '' # Resets the current input for the next question
                        questionStatus = False # Resets status to false 
                        displayScreen += 1 # Moves to the next display screen
                elif event.key == pygame.K_BACKSPACE:
                    currentInput = currentInput[:-1] 
                else:
                    currentInput += event.unicode

        # Checks if the user is trying to interact with the robot initially
        if event.type == pygame.MOUSEBUTTONDOWN and displayScreen == 0:
            displayScreen = 40 # Moves to the first screen

        # Checks if the user is a new patient
        elif event.type == pygame.MOUSEBUTTONDOWN and userYesRect.collidepoint(event.pos) and yesNoStatus != True:
            displayScreen = 1 # Moves to the first screen for new patients

        # Checks if the user is a returning patient
        elif event.type == pygame.MOUSEBUTTONDOWN and userNoRect.collidepoint(event.pos) and yesNoStatus != True:
            displayScreen = 41 # Moves to the first screen for returning patients
        
        # Checks if the enter button is pressed
        elif questionStatus == True:
            if event.type == pygame.MOUSEBUTTONDOWN and buttonRect.collidepoint(event.pos):
                if currentInput == "" or currentInput == " ": # Checks if patient did not input any information
                    error() # Runs the error function to display the error message
                    print(currentInput+"Qstat2")
                else:
                    info.append(question) # Appends the question into the array
                    info.append(currentInput) # Appends the current input and stores it in the info array
                    timeStatus= False
                    currentInput = "" # Resets the current input for the next question
                    questionStatus = False # Resets status to false
                    displayScreen += 1 # Moves to the next display screen
      
        # Checks if the understood button is pressed for the instructions
        elif displayScreen == 31:
           if event.type == pygame.MOUSEBUTTONDOWN and instructionBtnRect.collidepoint(event.pos):
               displayScreen = 32 # Moves to the next display screen
        
        # Checks if the user is trying to go back from a question
        if event.type == pygame.MOUSEBUTTONDOWN and backBtnRect.collidepoint(event.pos):
            print(displayScreen)
            currentInput = "" # Resets the current input
            timeStatus= False

            if displayScreen == 41:
                info = []
                displayScreen = 40
            elif displayScreen == 1:
                displayScreen = 40
            elif displayScreen == 10 and info[-2] == "Do You Have Any Chest Pain?": # Checks to see if the subquestions were skipped
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the previous question
                displayScreen = 7 # Sets display 7
            elif displayScreen == 13 and info[-2] == "Are You Bleeding or do You Have any Visible Wounds?": # Checks to see if the subquesions were skipped
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the previous question
                displayScreen = 10 #Sets the display
            elif displayScreen == 18 and info[-2] == "Have You Fainted or Lost Consciousness Within the Last 24 Hours?": # Checks to see if the subquesions were skipped
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the prevopis question
                displayScreen = 13 #Sets the display
            elif displayScreen == 20 and info[-2] == "Do You Feel Dizzy or Lightheaded?": # Checks to see if the subquesions were skipped
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the previous question
                displayScreen = 18 #Sets the display
            elif displayScreen == 22 and info[-2] == "Do You Have a Fever, Chills, or Sweating?": # Checks to see if the subquesions were skipped
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the previous question
                displayScreen = 20 #Sets the display
            elif displayScreen == 25 and info[-2] == "Are You Taking Any Medication?": # Checks to see if the subquesions were skipped
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the previous question
                displayScreen = 22 #Sets the display
            elif displayScreen == 28 and info[-2] == "Do You Have Diabetes/Family History of Diabetes?": # Checks to see if the subquesions were skipped
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the previous question
                displayScreen = 26 #Sets the display
            else: 
                del info[len(info)-1] # Deletes the previous answer
                del info[len(info)-2] # Deletes the previous question
                displayScreen -= 1 # Moves back one screen
            print(info)

        # Checks if the user pressed the yes or no button when entering the question
        elif event.type == pygame.MOUSEBUTTONDOWN and yesNoStatus == True:
            # Checks if the user clicks "YES"
            if yesRect.collidepoint(event.pos):
                info.append(yesNoQuestions) # Appends the question into the array
                info.append("Yes") # Appends "YES" and the input and stores in the info array
                yesNoStatus = False # Resets status to false
                displayScreen += 1 # Moves to the next display screen

            # Checks if the user clicks "NO"
            elif noRect.collidepoint(event.pos):
                if displayScreen == 7 or displayScreen == 10 or displayScreen == 22 or displayScreen == 25: # Checks for the condition to skip the subquestions 
                    info.append(yesNoQuestions) # Appends the question into the array 
                    info.append("No") # Appends "NO" and the input and stores in the info array
                    yesNoStatus = False # Resets status to false
                    displayScreen += 3 # Skips over the subquestion display screens
                elif displayScreen == 13: # Checks for the condition to skip the subquestions
                    info.append(yesNoQuestions) # Appends the question into the array
                    info.append("No") # Appends "NO" and the input and stores in the info array
                    yesNoStatus = False # Resets status to false
                    displayScreen += 5 # Skips over the subquestion display screens
                elif displayScreen == 16 or displayScreen == 18 or displayScreen == 20: # Checks for the condition to skip the subquestions
                    info.append(yesNoQuestions) # Appends the question into the array
                    info.append("No") # Appends "NO" and the input and stores in the info array
                    yesNoStatus = False # Resets status to false
                    displayScreen += 2 # Skips over the subquestion display screens
                else: 
                    info.append(yesNoQuestions) # Appends the question into the array
                    info.append("No") # Appends "NO" and the input and stores in the info array
                    displayScreen += 1 # Moves to the next display screen
                    yesNoStatus = False # Resets status to false          
    
        # Checks if the user selected an icon when rating how they are feeling
        elif event.type == pygame.MOUSEBUTTONDOWN and rateStatus == True:
            info.append("Please Rate How You Are Feeling Overall:")
            if greatRect.collidepoint(event.pos): # Checks if the user clicked the great icon
                info.append("Great") # Appends "Great" and stores in the info array
                rateStatus = False # Resets status to false
                displayScreen = 6 # Moves to the next display screen
            if goodRect.collidepoint(event.pos): # Checks if the user clicked the good icon
                info.append("Good") # Appends "Good" and stores in the info array
                rateStatus = False # Resets status to false
                displayScreen = 6 # Moves to the next display screen
            if mehRect.collidepoint(event.pos): # Checks if the user clicked the meh icon
                info.append("Meh") # Appends "Meh" and stores in the info array
                rateStatus = False # Resets status to false
                displayScreen = 6 # Moves to the next display screen
            if badRect.collidepoint(event.pos): # Checks if the user clicked the great icon
                info.append("Bad") # Appends "Bad" and stores in the info array
                rateStatus = False # Resets status to false
                displayScreen = 6 # Moves to the next display screen
            if terribleRect.collidepoint(event.pos): # Checks if the user clicked the great icon
                info.append("Terrible") # Appends "Terrible" and stores in the info array
                rateStatus = False # Resets status to false
                displayScreen = 6 # Moves to the next display screen

        # Checks if the question requires a unit of time
        if timeStatus == True and event.type == pygame.MOUSEBUTTONDOWN: 
            if currentInput == "" or currentInput == " ":
                error()
                print(currentInput+"Tstat")
            else:
                inputText = ""
                if hoursRect.collidepoint(event.pos): # Checks if hours is pressed
                    currentInput = currentInput.strip(" hours")
                    currentInput = currentInput.strip(" days")
                    currentInput = currentInput.strip(" weeks")
                    inputText = " hours"
                elif daysRect.collidepoint(event.pos): # Checks if days is pressed
                    currentInput = currentInput.strip(" hours")
                    currentInput = currentInput.strip(" days")
                    currentInput = currentInput.strip(" weeks")
                    inputText = " days"
                elif weeksRect.collidepoint(event.pos): # Checks if weeks is pressed
                    currentInput = currentInput.strip(" hours")
                    currentInput = currentInput.strip(" days")
                    currentInput = currentInput.strip(" weeks")
                    inputText = " weeks"
                currentInput += inputText
                print(currentInput)
                timeStatus = False
                
        if event.type == pygame.QUIT:
            quitVar = False

    # Updates the screen every loop to show changes
    pygame.display.update()

    # Connects with the clock and the frame limit
    fpsClock.tick(FPS)

# Exits the window
print(info)
pygame.quit()

# Stops the video capture streams
faceCapture.release()
cv2.destroyAllWindows()
