'''A simple Calculator interface'''

import graphics as gr

def pointInRectangle(point, rectangle):
    '''This function returns True if a graphics Point is within a graphics Rectangle, and False otherwise
    Note that this function assumes that the rectangle was created from top left towards the bottom right
    That is, rectangle.getP1() is neither below nor to the right of rectangle.getP2()
    This assumption is easily fixable, but I'm lazy - Bender'''
    return (point.getX() >= rectangle.getP1().getX() 
            and point.getX() <= rectangle.getP2().getX() 
            and point.getY() >= rectangle.getP1().getY() 
            and point.getY() <= rectangle.getP2().getY())

def applyOperation(operation, num1, num2):
    if operation == "":
        return num2
    elif operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    else: 
        return num1 / num2

def main():
    '''Handles construction, computation, and general interface of calculator'''
    screen = gr.GraphWin('Calculator', 400,600) # Create our screen

    # First, we create our numberKeys list to store the rectangles for each number button
    # We create it so that numberKeys[i] contains the rectangle for the button i
    numberKeys = []
    numberKeys.append(gr.Rectangle(gr.Point(25,525), gr.Point(75,575)))
    numberKeys[0].draw(screen)
    gr.Text(gr.Point(50,550),"0").draw(screen)

    # We use a *nested for loop* (more on these later) to create the remaining number keys
    for i in range(3):
        for j in range(3):
            numberKeys.append(gr.Rectangle(gr.Point(100*j+25, 425-i*100), gr.Point(100*j+75, 475-i*100)))
            numberKeys[3*i+j+1].draw(screen)
            buttonText = gr.Text(gr.Point(50+100*j, 450-100*i), str(3*i+j+1))
            buttonText.draw(screen)
    
    # Creation of clear button
    clearButton = gr.Rectangle(gr.Point(125, 525), gr.Point(175, 575))
    clearButtonText = gr.Text(gr.Point(150, 550), "c")
    clearButton.draw(screen)
    clearButtonText.draw(screen)

    # Creation of equals button
    equalsButton = gr.Rectangle(gr.Point(225, 525), gr.Point(275, 575))
    equalsButtonText = gr.Text(gr.Point(250, 550), "=")
    equalsButton.draw(screen)
    equalsButtonText.draw(screen)

    # Creation of addition button
    addButton = gr.Rectangle(gr.Point(325,525), gr.Point(375, 575))
    addButtonText = gr.Text(gr.Point(350,550), "+")
    addButton.draw(screen)
    addButtonText.draw(screen)

    # Creation of subtraction button
    minusButton = gr.Rectangle(gr.Point(325,425), gr.Point(375, 475))
    minusButtonText = gr.Text(gr.Point(350,450), "-")
    minusButton.draw(screen)
    minusButtonText.draw(screen)

    # Creation of multiplication button
    timesButton = gr.Rectangle(gr.Point(325,325), gr.Point(375, 375))
    timesButtonText = gr.Text(gr.Point(350,350), "*")
    timesButton.draw(screen)
    timesButtonText.draw(screen)

    # Creation of division button
    divideButton = gr.Rectangle(gr.Point(325,225), gr.Point(375, 275))
    divideButtonText = gr.Text(gr.Point(350,250), "/")
    divideButton.draw(screen)
    divideButtonText.draw(screen)

    # Creation of text display
    textDisplay = gr.Rectangle(gr.Point(25,25), gr.Point(375, 175))
    textDisplay.draw(screen)
    textDisplayText = gr.Text(gr.Point(200, 100), "0")
    textDisplayText.draw(screen)

    firstNumber = True  # This allows us to determine whether the user is inputting the first digit of their next number
    previousNumber = 0  # This will be used to keep track of the previous number for use with our operators
    operation = ""      # This will keep track of what operation we're applying ('+', '-', '*', '/')
    
    while(True):
        '''In this loop we handle all operations of the interface'''
        mousePos = screen.getMouse()

        operationButtons = [addButton, minusButton, timesButton, divideButton]
        operationButtonTexts = [addButtonText, minusButtonText, timesButtonText, divideButtonText]

        if pointInRectangle(mousePos, clearButton): 
            previousNumber = 0
            textDisplayText.setText("0")
            firstNumber = True
            operation = ""
        elif pointInRectangle(mousePos, equalsButton):
            previousNumber = applyOperation(operation, previousNumber, float(textDisplayText.getText()))
            textDisplayText.setText(str(previousNumber))
            firstNumber = True
            operation = ""
        else: 
            for i in range(4):
                if pointInRectangle(mousePos, operationButtons[i]):
                    previousNumber = applyOperation(operation, previousNumber, float(textDisplayText.getText()))
                    textDisplayText.setText(str(previousNumber))
                    firstNumber = True
                    operation = operationButtonTexts[i].getText()
            for i in range(10):
                if pointInRectangle(mousePos, numberKeys[i]):
                    if firstNumber:
                        textDisplayText.setText("")
                        firstNumber = False
                    textDisplayText.setText(textDisplayText.getText() + str(i))

if __name__ == "__main__":
    main()