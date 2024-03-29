# Amy Liu
# Paint Project.py
'''
A Hollow Knight themed program that lets the user draw on a canvas with a variety of tools and choose the colour and size of what is drawn. Tools include a pencil, eraser, pen,
eyedropper, ellipse, rectangle, line, polygon, text, paint bucket, six stamps, and two backgrounds. There are alse undo and redo buttons that can be used. The user can also save
their image to their computer or load an image to the canvas.
'''


from pygame import *
from tkinter import *
from tkinter import filedialog
from math import *

root = Tk()
root.withdraw()

font.init()

screen = display.set_mode((1140, 760))
screen.fill((128, 128, 128))
WHITE = (255, 255, 255)
pastmx = 250
pastmy = 50

# loading images
windowIcon = image.load("WindowIcon.png")

colourPicker = image.load("colourPallet.jpg")
colourPicker = transform.scale(colourPicker, (130, 215))

godhomeImg = image.load("promo_godmaster.jpg")
godhomeImg = transform.scale(godhomeImg, (1140, 760))

crossroadsImg = image.load("GreenpathBg.webp")
crossroadsImgBut = transform.scale(crossroadsImg, (120, 60))
crossroadsImgTrans = transform.scale(crossroadsImg, (840, 567))
greenpathImg = image.load("ColosseumBg.webp")
greenpathImgBut = transform.scale(greenpathImg, (120, 60))
greenpathImgTrans = transform.scale(greenpathImg, (840, 567))

pencilIcon = image.load("PencilTool.png")
eraserIcon = image.load("EraserTool.png")
penIcon = image.load("PenTool.png")
dropperIcon = image.load("DropperTool.png")
ellipseIcon = image.load("EllipseTool.png")
rectIcon = image.load("RectTool.png")
lineIcon = image.load("LineTool.png")
polyIcon = image.load("PolygonTool.png")
fillIcon = image.load("FillTool.png")
textIcon = image.load("TextTool.png")
loadIcon = image.load("LoadIcon.png")
saveIcon = image.load("SaveIcon.png")
undoIcon = image.load("UndoIcon.png")
redoIcon = image.load("RedoIcon.png")

checkmark = image.load("Checkmark.png")

knightStamp = image.load("KnightStamp.webp")
hornetStamp = image.load("HornetStamp.webp")
grimmStamp = image.load("GrimmStamp.webp")
quirrelStamp = image.load("QuirrelStamp.webp")
pvStamp = image.load("PVStamp.webp")
shadeStamp = image.load("ShadeStamp.webp")

display.set_caption("The Hollow Knight Paint Program")
display.set_icon(windowIcon)

screen.blit(godhomeImg, (0, 0))


# stamps
stampsRect = []     # list for storing the rects of the stamps
stampsIcon = []     # stores the transformed version of the stamp
stampsList = [knightStamp, hornetStamp, grimmStamp, quirrelStamp, pvStamp, shadeStamp]
for i in range(len(stampsList)):    # gets the transformed versions of the stamps and their rect and appends it to the right list
    stampWidth = stampsList[i].get_width()
    stampHeight = stampsList[i].get_height()

    stampIcon = transform.scale(stampsList[i], (stampWidth * (60/stampHeight), 60))     # scales the image down to 60 pixels
    
    stampsIcon.append(stampIcon)
    stampsRect.append(stampIcon.get_rect())

for i in range(len(stampsIcon)):
        stampsRect[i] = stampsRect[i].move((550 + i*80, 650))   # spaces the buttons out by 80 pixels

        screen.blit(stampsIcon[i], stampsRect[i])


# icons
checkmark = transform.scale(checkmark, (20, 18))    

iconsList = [pencilIcon, eraserIcon, penIcon, dropperIcon, ellipseIcon, rectIcon, lineIcon, polyIcon, textIcon, fillIcon]
topIconsList = [loadIcon, saveIcon, undoIcon, redoIcon]

for i in range(len(iconsList)):  # this and next loop scale the icons down
    iconsList[i] = transform.scale(iconsList[i], (50, 50))

for i in range(len(topIconsList)):
    topIconsList[i] = transform.scale(topIconsList[i], (30, 30))



# starting conditions
prevScreen = []     # stores the previous iterations of the canvas for use when undoing
redoScreen = []     # stores the interation of the canvas that were undone, for redoing

tool = "pencil"
isFilled = False    # variable that determines if a drawn shape (circle, rect, polygon) will be filled

# represents the state of when something is being drawn with the polygon or text tool
writingText = False
drawingPoly = False

polyPoints = []     # stores the points of the polygon the user is drawing
stampToDraw = None      # the stamp that the user has selected


lineWidth = 10
lenBar = 50     # length of rect that represents the line width
drawCol = (0, 0, 0)     # variable for the current colour used
drawFont = font.SysFont("Calibri", 40)      # font used when user is drawing text onto the canvas
genFont = font.SysFont("Calibri", 13)       # font used for informational text outside the canvas
word = ""   # variable storing the letters the user is drawing on the canvas



# Defining rects
# canvas
canvas = Rect(250, 50, 840, 567)
canvasSub = screen.subsurface(canvas)
canvasColours = []
draw.rect(screen, WHITE, canvas)

# tools
pencil = Rect(60, 420, 50, 50)
eraser = Rect(150, 420, 50, 50)
pen = Rect(60, 480, 50, 50)
eyedrop = Rect(150, 480, 50, 50)
drawCircle = Rect(60, 540, 50, 50)
drawRect = Rect(150, 540, 50, 50)
drawLine = Rect(60, 600, 50, 50)
polygon = Rect(150, 600, 50, 50)
drawText = Rect(60, 660, 50, 50)
fill = Rect(150, 660, 50, 50)

# stamps + bgs
    
crossroadsBg = crossroadsImgBut.get_rect()
crossroadsBg = crossroadsBg.move((250, 650))

greenpathBg = greenpathImgBut.get_rect()
greenpathBg = greenpathBg.move((380, 650))
    

# other
load = Rect(50, 50, 30, 30)
save = Rect(90, 50, 30, 30)
undo = Rect(140, 50, 30, 30)
redo = Rect(180, 50, 30, 30)

# colour and size pickers
colourPick = Rect(50, 100, 130, 215)
curColDisplay = Rect(180, 100, 30, 215)
sizeBar = Rect(50, 334, 160, 37)


filledCheck = Rect(50, 385, 20, 20)
clearScreen = Rect(125, 385, 85, 20)


# lists for convenience
toolsList = [pencil, eraser, pen, eyedrop, drawCircle, drawRect, drawLine, polygon, drawText, fill]
selected = [True, False, False, False, False, False, False, False, False, False]     # each element corresponds to a tool, False for a tool that is not selected, True for one that is
stampSelected = [False, False, False, False, False, False]      # does the same as "selected", but for stamps

bgList = [crossroadsBg, greenpathBg]     # changable canvas backgrounds
otherList = [load, save, undo, redo, clearScreen]     # buttons that have miscallaneous functions
colourSizeList = [colourPick, curColDisplay, sizeBar]    # buttons that relate to changing what is drawn


# functions
def setSelect(position):    # sets a tool as selected in the "selected" list
    for i in range(len(selected)):   # sets every other element as False, then sets the referred to tool as True so that only one is selected
        selected[i] = False
        selected[position] = True

def setSelectStamps(position):   # same as "setSelect", but for stamps
    for i in range(len(stampSelected)):
        stampSelected[i] = False
        stampSelected[position] = True

def genLine(colour, width):     # creates a line that is made out of many circles
    for i in range(round(distance)):
        draw.circle(screen, colour, (xdist * i/distance + pastmx, ydist * i/distance + pastmy), width/2)

def fillTool(x, y):     # fills an area of a single colour with another colour
    canvasPxs = PixelArray(canvasSub)   # creates a numerical representation of the canvas that can be changed
    checking = [(x - 250, y - 50)]    # list of positions in the pixel array to check for if the colour is the same and should be changed
    oldCol = canvasPxs[x - 251, y - 51]   # the colour of the area that will be replaced
    
    while len(checking) > 0:
        curX, curY = checking.pop()   # current position that is being checked

        if canvasPxs[curX, curY] != oldCol:   # if the position's colour is different, then that means we hit a boundary that doesnt need to be replaced, so we ignore the rest of the code that does that
            continue
        
        if canvasPxs[curX, curY] == oldCol:
            canvasPxs[curX, curY] = drawCol   # replaces the pixel with the new colour

            # adds the neighbouring pixels to be checked, as long as those pixels are not outside the bounds of the canvas            
            if curX + 1 < 840:
                checking.append((curX + 1, curY))
            if curX - 1 >= 0:
                checking.append((curX - 1, curY))
            if curY + 1 < 567:
                checking.append((curX, curY + 1))
            if curY - 1 >= 0:
                checking.append((curX, curY - 1))

    del canvasPxs   # deletes the pixel array so the pixels in the canvas are no longer locked


back = canvasSub.copy()


running = True
while running:
    mouseDown = False
    mouseUp = False
    rightClick = False
    
    for evt in event.get():
        

        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:     
                mouseDown = True    # represents a left click
            if evt.button == 3:
                rightClick = True    # represents a right click
                
        if evt.type == MOUSEBUTTONUP:
            mouseUp = True      # represents when the mouse is released

        if evt.type == KEYDOWN:
            curLetter = evt.unicode
            word += curLetter   # adds the letter that was typed to the word
        
        if evt.type == QUIT:
            running = False


    #---------------------------


    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    
    for i in range(len(toolsList)):   # draws the tool buttons and icons
        draw.rect(screen, WHITE, toolsList[i])
        screen.blit(iconsList[i], toolsList[i])

    for i in range(len(selected)):   # draws the outline for the tool buttons, green for selected, black for unselected
        if selected[i]:
            draw.rect(screen, (0, 255, 0), toolsList[i], 1)

        else:
            draw.rect(screen, (0, 0, 0), toolsList[i], 1)
        

    for i in range(len(otherList)):     # draws the buttons and the outlines
        draw.rect(screen, WHITE, otherList[i])
        draw.rect(screen, (0, 0, 0), otherList[i], 1)

        if i == 4:      # ignores the clear button because it doesn't have an icon
            continue
        
        screen.blit(topIconsList[i], otherList[i])

    screen.blit(crossroadsImgBut, crossroadsBg)
    screen.blit(greenpathImgBut, greenpathBg)

    for i in bgList:    # outlines for the background buttons
        draw.rect(screen, (0, 0, 0), i, 1)

 
    # drawing the text and shapes relating to the 'filled' checkbox
    filledText = genFont.render("filled", False, WHITE)
    screen.blit(filledText, (77, 390))
    draw.rect(screen, WHITE, filledCheck)
    draw.rect(screen, (0, 0, 0), filledCheck, 1)

    if isFilled == True:
        screen.blit(checkmark, (filledCheck))

    # drawing the clear button
    clearText = genFont.render("Clear Screen", False, (0, 0, 0))
    screen.blit(clearText, (clearScreen[0] + 11, clearScreen[1] + 4))



    # colour picking
    screen.blit(colourPicker, colourPick)
    draw.rect(screen, drawCol, curColDisplay)
    draw.rect(screen, WHITE, sizeBar)
    draw.rect(screen, (200, 200, 255), Rect(50, 334, lenBar, 37))

    for i in colourSizeList:    # outlines for buttons
        draw.rect(screen, (0, 0, 0), i, 1)

    

        
    # button collision
    for i in range(len(stampsRect)):    # goes through the stamps and checks if any are clicked
        if stampsRect[i].collidepoint((mx, my)):
            if mouseDown:
                setSelectStamps(i)
                stampToDraw = stampsList[i]     # represents the selected stamp
                tool = "stamp"      # makes stamp a tool so that it doesnt draw with another tool at the same time

                break

    for i in range(len(stampSelected)):     # outlines of buttons
        if stampSelected[i]:
            draw.rect(screen, (0, 255, 0), stampsRect[i], 1)
        else:
            draw.rect(screen, (0, 0, 0), stampsRect[i], 1)


    
    if pencil.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), pencil, 1)   # makes the outline green when hovering over the button
        if mouseDown:
            tool = "pencil"
            setSelect(0)
            
    if eraser.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), eraser, 1)
        if mouseDown:
            tool = "eraser"
            setSelect(1)

    if pen.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), pen, 1)
        if mouseDown:
            tool = "pen"
            setSelect(2)


    if eyedrop.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), eyedrop, 1)
        if mouseDown:
            tool = "eyedrop"
            setSelect(3)

    if drawCircle.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), drawCircle, 1)
        if mouseDown:
            tool = "circle"
            setSelect(4)

    if drawRect.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), drawRect, 1)
        if mouseDown:
            tool = "rect"
            setSelect(5)

    if drawLine.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), drawLine, 1)
        if mouseDown:
            tool = "line"
            setSelect(6)

    if polygon.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), polygon, 1)
        if mouseDown:
            tool = "polygon"
            setSelect(7)

    if drawText.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), drawText, 1)
        if mouseDown:
            tool = "text"
            setSelect(8)

    if fill.collidepoint((mx, my)):
        draw.rect(screen, (0, 255, 0), fill, 1)
        if mouseDown:
            tool = "fill"
            setSelect(9)

    if tool != "stamp":     # makes it so that only one thing is displayed as selected at a time, rather than a stamp and a tool at the same time
        for i in range(len(stampSelected)):
            stampSelected[i] = False

    if tool == "stamp":
        for i in range(len(selected)):
            selected[i] = False


    if undo.collidepoint((mx, my)):
        draw.rect(screen, WHITE, undo, 1)
        if mouseDown:
            if len(prevScreen) > 0:
                redoScreen.append(canvasSub.copy())     # puts the current screen into the redo list, so that it can be blitted back on
                screen.blit(prevScreen[-1], (250, 50))
                back = canvasSub.copy()     # the variable 'back' is used when a shape needs to move around on the canvas without leaving a trail behind; it is blitted on to the canvas to cover the previous shape
                del prevScreen[-1]

    if redo.collidepoint((mx, my)):
        draw.rect(screen, WHITE, redo, 1)    # draws an outline when hovering over
        if mouseDown:
            if len(redoScreen) > 0:
                prevScreen.append(canvasSub.copy())     # puts the current screen into the undo list
                screen.blit(redoScreen[-1], (250, 50))
                back = canvasSub.copy()
                del redoScreen[-1]
    
    changed = False     # boolean for whether or not the mouse has already clicked on the checkbox in this loop; stops the checkbox from swithching back and forth
    if filledCheck.collidepoint((mx, my)):
        if mouseUp:
            if isFilled == True and changed == False:
                isFilled = False
                changed = True


            if isFilled == False and changed == False:
                isFilled = True
                changed = True

    if sizeBar.collidepoint((mx, my)):      # changes the line width based on where the user clicks on the rectangle
        draw.rect(screen, WHITE, sizeBar, 1)    
        if mb[0]:
            lenBar = mx - 50    # length of the second rectangle that represents the line width
            lineWidth = lenBar


            
    if crossroadsBg.collidepoint((mx, my)):     # blits the background onto the canvas
        draw.rect(screen, WHITE, crossroadsBg, 1)
        if mouseDown:
            prevScreen.append(canvasSub.copy())
            screen.blit(crossroadsImgTrans, canvas)
            
            back = canvasSub.copy()
            redoScreen = []     # clears the redo list when something is drawn on the canvas, because you should only be able to redo directly after an undo

    if greenpathBg.collidepoint((mx, my)):
        draw.rect(screen, WHITE, greenpathBg, 1)
        if mouseDown:
            prevScreen.append(canvasSub.copy())
            screen.blit(greenpathImgTrans, canvas)
            
            back = canvasSub.copy()
            redoScreen = []

    if colourPick.collidepoint((mx, my)):   # when any clicks happen on the colour selector, the colour will change
        if mb[0]:
            drawCol = screen.get_at((mx, my))

    if clearScreen.collidepoint((mx, my)):
        draw.rect(screen, WHITE, clearScreen, 1)    
        if mouseDown:
            prevScreen.append(canvasSub.copy())
            draw.rect(screen, WHITE, canvas)
            
            back = canvasSub.copy()
            redoScreen = []


    if load.collidepoint((mx, my)):
        draw.rect(screen, WHITE, load, 1)
        if mouseDown:
            result = filedialog.askopenfilename(filetypes = [("Picture files", "*.png;*.jpg")])
            if result != "":    # result will be "" if cancel is pressed
                loadImg = image.load(result)
                prevScreen.append(canvasSub.copy())
                canvasSub.blit(loadImg, (0, 0))
                redoScreen = []
            
        
    if save.collidepoint((mx, my)):
        draw.rect(screen, WHITE, save, 1)
        if mouseDown:
            result = filedialog.asksaveasfilename(filetypes = [("Picture files", "*.png;*.jpg")])
            
            sav = canvasSub
            image.save(sav, result + ".png")
    

    # text
    if tool == "polygon":
        polyText = genFont.render("Right click to end shape", False, WHITE)
        screen.blit(polyText, (10, 740))

    if tool != "polygon":   # covers up the info text when the tool is not polygon
        draw.rect(screen, (0, 0, 0), Rect(10, 740, 130, 30))
            

    if canvas.collidepoint((mx, my)):
        draw.rect(screen, (0, 0, 0), Rect(1080, 740, 100, 40))  # covers old text
        mouseText = genFont.render(str(mx - 250) + ", " + str(my - 50), False, WHITE)  # displays the mouse's current x and y values in relation to the canvas
        screen.blit(mouseText, (1080, 740))
    else:
        draw.rect(screen, (0, 0, 0), Rect(1080, 740, 100, 40))
            
    # on canvas
    if canvas.collidepoint((mx, my)):
        screen.set_clip(canvas) 

        xdist = mx - pastmx
        ydist = my - pastmy
        distance = ((mx - pastmx)**2 + (my - pastmy)**2) ** 0.5     # finds the distance between the current mouse position and the past position so that circles can be drawn at each point between the two positions

        if mouseDown:
            prevScreen.append(canvasSub.copy())
            redoScreen = []     # clears the redo list when something is drawn


        # takes certain actions based on the tool that is selected
        if tool == "pencil":
            if mb[0]:
                genLine(drawCol, lineWidth)
                back = canvasSub.copy()
            
        if tool == "eraser":
            if mb[0]:
                genLine((255, 255, 255), lineWidth)
                back = canvasSub.copy()

        if tool == "pen":
            if mb[0]:
                penDist = dist((pastmx, pastmy), (mx, my))
                genLine(drawCol, lineWidth/abs(penDist/5 + 1) + 2)      # varies the width of the line based on the speed that the user draws at; the random numbers just regulate the line so it doesn't vary too much
                back = canvasSub.copy()
                
        if tool == "circle":
            if mouseDown:
                startShapeX = mx    # sets the point that the shape start at
                startShapeY = my
      
            if mb[0]:
                screen.blit(back, (250, 50))    # covers up previous shapes so that a trail isn't left
                back = canvasSub.copy()

                ellipseNormalize = Rect(startShapeX, startShapeY, mx - startShapeX, my - startShapeY)
                ellipseNormalize.normalize()
                
                if isFilled == False:    # makes the shape filled based on the isFilled variable
                    draw.ellipse(screen, drawCol, ellipseNormalize, lineWidth)
                if isFilled == True:
                    draw.ellipse(screen, drawCol, ellipseNormalize)

            if mouseUp:              
                back = canvasSub.copy()

        if tool == "rect":    # similar to ellipse tool
            if mouseDown:
                startShapeX = mx
                startShapeY = my
            
            if mb[0]:
                rectNormalize = Rect(startShapeX, startShapeY, mx - startShapeX, my - startShapeY)
                rectNormalize.normalize()
                
                screen.blit(back, (250, 50))
                back = canvasSub.copy()
                if isFilled == False:
                    draw.rect(screen, drawCol, rectNormalize, lineWidth)
                if isFilled:
                    draw.rect(screen, drawCol, rectNormalize)

            if mouseUp:
                back = canvasSub.copy()

        if tool == "line":
            if mouseDown:
                startShapeX = mx
                startShapeY = my
                
            if mb[0]:
                screen.blit(back, (250, 50))
                back = canvasSub.copy()

                lineDist = ((mx - startShapeX)**2 + (my - startShapeY)**2) ** 0.5   # finds the distance between the starting point and the current mouse position
                lineXDist = mx - startShapeX
                lineYDist = my - startShapeY
                
                for i in range(round(lineDist)):    # draws the circles in a straight line based on the previously calculated distance
                    draw.circle(screen, drawCol, (lineXDist * i/lineDist + startShapeX, lineYDist * i/lineDist + startShapeY), lineWidth/2)

            if mouseUp:
                back = canvasSub.copy()


        if tool == "eyedrop":
            if mouseDown:
                drawCol = screen.get_at((mx, my))
                tool = "pencil"
                setSelect(0)

        if tool == "polygon":
            if mouseDown:
                back = canvasSub.copy()
                polyPoints.append((mx, my))     # adds the point the user clicked at to the list so that it can be drawn later
                drawingPoly = True

            if rightClick and drawingPoly == True:
                polyPoints.append((mx, my))
                firstLastDist = dist(polyPoints[0], polyPoints[-1])
                
                for i in range(round(firstLastDist)):   # draws line from first to last point to complete the polygon
                    draw.circle(screen, drawCol, (((polyPoints[-1])[0] - (polyPoints[0])[0]) * i/firstLastDist + (polyPoints[0])[0], ((polyPoints[-1])[1] - (polyPoints[0])[1]) * i/firstLastDist + (polyPoints[0])[1]), lineWidth/2)
                
                if isFilled:
                    draw.polygon(screen, drawCol, polyPoints)   # draws a filled polygon to fill the polygon
                    
                polyPoints = []     # clears the list for the next polygon
                drawingPoly = False

                back = canvasSub.copy()
                
                            
            if drawingPoly:     # draws the current line so that it follows the mouse
                screen.blit(back, (250, 50))
                back = canvasSub.copy()

                polyDistX = mx - (polyPoints[-1])[0]
                polyDistY = my - (polyPoints[-1])[1]
                polyDist = ((polyDistX)**2 + (polyDistY)**2) ** 0.5

                for i in range(round(polyDist)):
                    draw.circle(screen, drawCol, (polyDistX * i/polyDist + (polyPoints[-1])[0], polyDistY * i/polyDist + (polyPoints[-1])[1]), lineWidth/2)


        if tool == "text":
            if mouseDown:    # starts a line of text
                writingText = True
                textLoc = (mx, my)
                word = ""

                
            if writingText:
                text = drawFont.render(word, False, drawCol)
                screen.blit(text, textLoc)
                back = canvasSub.copy()


        if tool == "fill":
            if mouseDown:
                if screen.get_at((mx, my)) != drawCol:      # doesn't run if the colour is the same, since it would be redundant
                    fillTool(mx, my)
                    back = canvasSub.copy()

        if tool == "stamp":
            if mb[0]:    # allows the stamp to be dragged before being placed
                stampHeight = stampToDraw.get_height()
                stampWidth = stampToDraw.get_width()

                screen.blit(back, (250, 50))
                back = canvasSub.copy()
                screen.blit(stampToDraw, (mx - stampWidth/2, my - stampHeight/2))

            if mouseUp:
                screen.blit(stampToDraw, (mx - stampWidth/2, my - stampHeight/2))
                back = canvasSub.copy()
                

            
        screen.set_clip(None)


    if canvas.collidepoint((mx, my)) == False:      # exceptions that might occur when clicking outside of the canvas
        screen.set_clip(canvas)
        if tool == "text":      # stops writing text when clicking off the canvas
            if mouseDown:
                writingText = False
                word = ""

        if tool == "polygon":      # stops drawing the polygon when clicking off the canvas
            if mouseDown:
                drawingPoly = False
                polyPoints = []

        if tool == "circle":      # allows for starting a shape outside of the canvas
            if mouseDown:
                startShapeX = mx
                startShapeY = my

            if mouseUp:
                back = canvasSub.copy()

        if tool == "rect":
            if mouseDown:
                startShapeX = mx
                startShapeY = my

            if mouseUp:
                back = canvasSub.copy()

            
        if tool == "line":
            if mouseDown:
                startShapeX = mx
                startShapeY = my

            if mouseUp:
                back = canvasSub.copy()

        

                
                
        screen.set_clip(None)
            
    
    draw.rect(screen, (0, 0, 0), canvas, 1)     # canvas outline

    # last position of the mouse
    pastmx = mx     
    pastmy = my
    
    #---------------------------
    

    display.flip()

quit()
