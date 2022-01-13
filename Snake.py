import turtle
import random
class Button:

    def __init__(self, turtleDrawer: turtle.Turtle, topLeftX: int, topLeftY: int, bottomRightX: int, bottomRightY: int, buttonText: str, borderColor = "Black", fillColor = None, fontColor = None, fontSize: int = 12):
        self.turt = turtleDrawer
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY
        self.text = buttonText
        self.fill = fillColor
        self.font = ('Arial', fontSize, 'normal')
        self.fontColor = fontColor
        self.borderColor = borderColor
        self.draw()
    
    def draw(self):
        ''' This function draws the button using the turtleDrawer given in the constructor'''
        self.turt.goto(self.topLeftX, self.topLeftY)
        self.turt.setheading(0)
        oldColor = self.turt.color()
        oldWidth = self.turt.width()
        self.turt.color(self.borderColor)

        if self.fill: # Begins filling if fillColor was given in constructor
            self.turt.fillcolor(self.fill)
            self.turt.begin_fill()
        
        self.turt.pendown()
        self.turt.width(5)
        for i in range(2): # Draws the boundary of the button
            self.turt.forward(self.bottomRightX-self.topLeftX)
            self.turt.right(90)
            self.turt.forward(self.topLeftY - self.bottomRightY)
            self.turt.right(90)
        self.turt.penup()

        if self.fill:
            self.turt.end_fill()

        # Draws the text in the center of the box
        self.turt.goto(int((self.topLeftX + self.bottomRightX)/2), 
                        int((self.topLeftY + self.bottomRightY)/2) - self.font[1])
        self.turt.pencolor(self.fontColor)
        self.turt.write(self.text, align = "center", font = self.font)
        self.turt.pencolor(oldColor[0])
        self.turt.pencolor(oldColor[1])
        self.turt.width(oldWidth)

    def pointInside(self, pointX: int, pointY: int) -> bool:
        ''' This function returns True if the point given by (pointX, pointY) is within the 
            bounds of the button given in the constructor'''
        return (pointX >= self.topLeftX
            and pointX <= self.bottomRightX
            and pointY >= self.bottomRightY
            and pointY <= self.topLeftY)

class Snake:

    def __init__(self):
        mySquare = ((-10, -10), (10, -10), (10, 10), (-10, 10))
        s = turtle.Shape("polygon", mySquare)
        turtle.register_shape("mySquare", s)
        self.started = False
        self.segments = None
        self.food = None
        self.turtleDrawer = turtle.Turtle()
        self.screen = self.turtleDrawer.getscreen()
        self.screen.setup(600, 600)
        self.player = turtle.Turtle("mySquare")
        self.player.hideturtle()
        self.startScreen()

    def startScreen(self):
        if self.turtleDrawer == None:
            self.turtleDrawer = turtle.Turtle()
        self.turtleDrawer.penup()
        self.turtleDrawer.hideturtle()
        self.screen.tracer(False)
        playButton = Button(self.turtleDrawer, 100, 100, 200, 0, "Click Me\nTo Play", borderColor="Red", 
                         fillColor="Green", fontColor="Blue", fontSize=13)
        quitButton = Button(self.turtleDrawer, -200, 100, -100, 0, "Click Me\nTo Quit", borderColor="Red", 
                         fillColor="Green", fontColor="Blue", fontSize=13)
        playButton.draw()
        quitButton.draw()

        def clickTest(x, y):
            if playButton.pointInside(x, y):
                self.screen.clear()
                self.play()
            elif quitButton.pointInside(x, y):
                self.screen.clear()
                turtle.bye()
        
        self.screen.onclick(clickTest)
        self.screen.mainloop()

    def play(self):
        self.screen.tracer(False)
        self.player = turtle.Turtle("mySquare")
        self.player.penup()
        self.player.color("red")
        self.player.goto(0, 0)
        self.segments = [self.player]
        self.food = self.makeFood()
        self.started = True

        self.screen.update()
        self.setupEvents()
        self.screen.mainloop()

    def setupEvents(self):
        for key in ["Up", "Down", "Left", "Right"]:
            self.screen.onkeypress(eval("self."+key.lower()), key)
        self.screen.listen()
        self.move()

    def up(self):
        if self.player.heading() != 270:
            self.player.setheading(90)
            self.screen.update()
    def down(self):
        if self.player.heading() != 90:
            self.player.setheading(270)
            self.screen.update()
    def left(self):
        if self.player.heading() != 0:
            self.player.setheading(180)
            self.screen.update()
    def right(self):
        if self.player.heading() != 180:
            self.player.setheading(0)
            self.screen.update()

    def move(self):
        if self.started:
            for i in range(1, len(self.segments)):
                self.segments[-i].goto(self.segments[-i-1].pos())
            self.player.forward(20)
            self.collisionCheck()
            self.screen.update()
            self.screen.ontimer(self.move, 50)
    
    def makeFood(self):
        food = turtle.Turtle("mySquare")
        food.color(random.random()/2, random.random(), random.random())
        food.penup()
        food.goto(random.randint(-300, 300), random.randint(-300, 300))
        return food

    def collisionCheck(self):
        if self.player.distance(self.food) < 20:
            self.food.hideturtle()
            self.food = self.makeFood()
            newSegment = turtle.Turtle("mySquare")
            newSegment.penup()
            newSegment.goto(self.segments[-1].pos())
            newSegment.color("red")
            self.segments.append(newSegment)
        
        for segment in self.segments[2:]:
            if self.player.distance(segment) <= 5:
                self.started = False
                self.screen.clear()
                self.endScreen()

    def endScreen(self):
        self.screen.tracer(False)
        self.turtleDrawer = turtle.Turtle()
        self.turtleDrawer.hideturtle()
        self.turtleDrawer.penup()
        self.turtleDrawer.goto(-0, 200)
        self.turtleDrawer.write("Game Over", align='center', font=("Arial", 30, "normal"))
        self.turtleDrawer.goto(0, 100)
        self.turtleDrawer.write("Score: "+str(len(self.segments)-1), align='center', font=("Arial", 20, "normal"))
        mainMenuButton = Button(self.turtleDrawer, -100, 0, 100, -200, "Main Menu", borderColor="Red", 
                         fillColor="Green", fontColor="Blue", fontSize=13)
        mainMenuButton.draw()

        def click(x, y):
            if mainMenuButton.pointInside(x, y):
                self.screen.clear()
                self.startScreen()
        self.screen.onclick(click)
        self.screen.listen()
        self.screen.mainloop()
        
        self.screen.update()

if __name__=="__main__":
    Snake()