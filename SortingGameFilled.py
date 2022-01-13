'''Lect9 Code'''

import graphics as gr
import random as r

def pointInRectangle(point, rectangle):
    '''This function returns True if a graphics Point is within a graphics Triangle, and False otherwise
    Note that this function assumes that the rectangle was created from top left towards the bottom right
    That is, rectangle.getP1() is neither below nor to the right of rectangle.getP2()
    This assumption is easily fixable, but I'm lazy - Bender'''
    return point.getX() >= rectangle.getP1().getX() and point.getX() <= rectangle.getP2().getX() and point.getY() >= rectangle.getP1().getY() and point.getY() <= rectangle.getP2().getY()

def isSorted(listOfNums):
    '''This function returns True if listOfNums is a list of numbers sorted from least to greatest, and False otherwise'''
    for i in range(len(listOfNums)-1):
        if listOfNums[i] > listOfNums[i+1]:
            return False
    return True

def main():
    '''This function is the main function of this game, which creates the window and handles all aspects of the game'''

    # First, we create the window
    screen = gr.GraphWin("Game", 600, 600)

    # Next, we create a few rectangles on the screen and put random numbers inside of them
    # We store these gr.Rectangles in the list rectangles and the gr.Texts in the list numberTexts
    # Notably, we put these in the same order. That is, numberTexts[i] stores the number inside of rectangles[i]
    rectangles = []
    numberTexts = []
    for i in range(5):
        rectangles.append(gr.Rectangle(gr.Point(75*i + 37.5*(i+1), 275), gr.Point(75*(i+1) + 37.5*(i+1), 325)))
        rectangles[i].draw(screen)
        numberTexts.append(gr.Text(gr.Point(75*i+37.5*(i+2), 300), str(r.randint(0, 100))))
        numberTexts[i].draw(screen)

    # Next we create a rectangle that we'll use as a submission button
    submitButton = gr.Rectangle(gr.Point(500, 0), gr.Point(600, 100))
    submitButton.setFill("Blue")
    submitText = gr.Text(gr.Point(550, 50), "Submit")
    submitText.setTextColor("Red")
    submitButton.draw(screen)
    submitText.draw(screen)

    # We create but do not yet draw the following texts so that we have them ready for later use
    winText = gr.Text(gr.Point(300, 200), "Great job!")
    notQuiteText = gr.Text(gr.Point(300, 100), "Not quite, keep trying!")
    
    # We create the boolean variables gameNotOver and oddRound to help us keep track of the state of the game
    # Since at this point the user has not interacted with our game yet, the game is not over and the user is
    # on the first round, so we set gameNotOver = True and oddRound = True.
    gameNotOver = True
    oddRound = True

    # We also create a variable to help us keep track of the first rectangle selected for swapping purposes.
    firstRectangleIndex = -1

    # We now enter the main loop of our game
    while(gameNotOver):
        # Within this loop, we repeatedly wait for the user to click, then check if the user has clicked on any
        # of the rectangles of the submission button, and act accordingly. 
        mousePos = screen.getMouse()

        if pointInRectangle(mousePos, submitButton):
            # If the mouse clicks the submit button, we should check if the numbers are sorted. 
            # If they are, draw the winText to the screen. If not, draw the notQuiteText to the screen.
            notQuiteText.undraw()
            numbers = []
            for i in range(5):
                numbers.append(int(numberTexts[i].getText()))
            if isSorted(numbers):
                winText.draw(screen)
                gameNotOver = False
            else:
                notQuiteText.draw(screen)
        else: 
            # If the submit button is not clicked, we should check if any of the rectangles were clicked
            # If a rectangle is clicked and it is an odd round, we should highlight it and save its index for later
            # If a rectangle is clicked and it is an even round, we should swap the text within that rectangle
            # with the text in the rectangle selected in the previous round
            for i in range(5): 
                if pointInRectangle(mousePos, rectangles[i]):
                    if(oddRound):
                        rectangles[i].setOutline("Yellow")
                        firstRectangleIndex = i
                        oddRound = False
                    else: 
                        temp = numberTexts[i].getText()
                        numberTexts[i].setText(numberTexts[firstRectangleIndex].getText())
                        numberTexts[firstRectangleIndex].setText(temp)
                        rectangles[firstRectangleIndex].setOutline("Black")
                        oddRound = True

    # Once we are out of the loop, the next mouse click will close the screen. 
    screen.getMouse()
    screen.close()

if(__name__ == "__main__"):
    # If someone executes this code (but doesn't import it), we'll start the game
    main()