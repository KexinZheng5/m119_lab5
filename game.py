# game gui

# reference: https://www.quickprogrammingtips.com/python/how-to-create-canvas-animation-using-tkinter.html

import tkinter
 
class Game():
    # window size
    window_width = 1500
    window_height = 800

    # wall thickness
    thickness = 20

    # bar size and postion
    bar_width = 50
    bar_height = 150

    bar1 = None
    bar1_x = 1400
    bar1_y = 0
    bar1_offset = 0

    threshold = 0.2

    # bar size and postion
    bar2 = None
    bar2_x = 100
    bar2_y = 0
    bar2_offset = 0

    # ball radius
    ball = None
    ball_x = window_width / 2
    ball_y = window_height / 2
    radius = 30
    shift_x = 20
    shift_y = 0
    
    # player 1
    p1_score = 0
    p1_display = None

    # player 2
    p2_score = 0
    p2_display = None
    
    exit = False

    # main window of the animation
    def create_animation_window(self):
        window = tkinter.Tk()
        window.title("Pong")
        window.geometry(f'{self.window_width}x{self.window_height}')
        window.protocol("WM_DELETE_WINDOW", self.on_close)
        return window
    
    # create a canvas for animation and add it to main window
    def create_animation_canvas(self, window):
        canvas = tkinter.Canvas(window)
        canvas.configure(bg="black")
        canvas.pack(fill="both", expand=True)
        return canvas


    # initialize window
    def __init__(self, mode):
        self.window = self.create_animation_window()
        self.canvas = self.create_animation_canvas(self.window)
        self.mode = mode
        self.canvas.create_rectangle(0, 0, self.window_width, self.thickness, fill="#737373", outline="")
        self.canvas.create_rectangle(0, self.window_height - self.thickness, self.window_width, self.window_height, fill="#737373", outline="")
        self.ball = self.canvas.create_oval(self.ball_x - self.radius, 
                        self.ball_y - self.radius,
                        self.ball_x + self.radius, 
                        self.ball_y + self.radius, 
                        fill="#ff9a1f", outline="")
        self.bar1 = self.draw_bar(self.bar1_x, self.bar1_y)
        # single player mode
        if (mode):
            self.canvas.create_rectangle(0, 0, self.thickness, self.window_height, fill="#737373", outline="")
        # multi player mode
        else:
            print(self.mode, mode)
            self.bar2 = self.draw_bar(self.bar2_x, self.bar2_y)
            
    # update frame
    def update_frame(self):
        self.update_bar()
        self.update_display()
        self.update_ball()
        self.window.update()

    # update bar position based on current offset
    def update_bar(self):
        # player 1
        # out of lower bound
        if self.bar1_offset + self.bar1_y > self.window_height - self.bar_height/2:
            self.bar1_y = self.window_height - self.bar_height/2
            self.canvas.delete(self.bar1)
            self.bar1 = self.draw_bar(self.bar1_x, self.bar1_y)
        # out of lower bound
        elif self.bar1_offset + self.bar1_y < self.bar_height/2:
            self.bar1_y = self.bar_height/2
            self.canvas.delete(self.bar1)
            self.bar1 = self.draw_bar(self.bar1_x, self.bar1_y)
        # otherwise
        else: 
            self.canvas.move(self.bar1, 0, self.bar1_offset)
            self.bar1_y += self.bar1_offset
        # player 2    
        if not self.mode:
            # out of lower bound
            if self.bar2_offset + self.bar2_y > self.window_height - self.bar_height/2:
                self.bar2_y = self.window_height - self.bar_height/2
                self.canvas.delete(self.bar2)
                self.bar2 = self.draw_bar(self.bar2_x, self.bar2_y)
            # out of lower bound
            elif self.bar2_offset + self.bar2_y < self.bar_height/2:
                self.bar2_y = self.bar_height/2
                self.canvas.delete(self.bar2)
                self.bar2 = self.draw_bar(self.bar2_x, self.bar2_y)
            # otherwise
            else: 
                self.canvas.move(self.bar2, 0, self.bar2_offset)
                self.bar2_y += self.bar2_offset

    # update bar offset given user input
    def update_bar_offset(self, id, value):
        # player 1
        if id == 1:
            if value < -self.threshold or value > self.threshold:
                self.bar1_offset = value * 40
            else:
                self.bar1_offset = 0
        # player 2
        else:
            if value < -self.threshold or value > self.threshold:
                self.bar2_offset = value * 40
            else:
                self.bar2_offset = 0

    # draw bar
    def draw_bar(self, x, y):
        return self.canvas.create_rectangle(x-(self.bar_width)/2, 
            y-(self.bar_height)/2, 
            x+(self.bar_width)/2, 
            y+(self.bar_height)/2, 
            fill="#fff", outline="")

    # draw ball
    def update_ball(self):
        # hit left edge
        if self.mode and self.ball_x - self.radius / 2 < self.thickness:
            self.shift_x = -self.shift_x
        # hit top edge
        elif self.ball_y - self.radius / 2 < self.thickness:
            self.shift_y = -self.shift_y
        # hit bottom edge 
        elif self.ball_y + self.radius / 2 > self.window_height - self.thickness:
            self.shift_y = -self.shift_y 
        # hit left player
        elif not self.mode \
            and self.ball_x < self.bar2_x + (self.radius + self.bar_width) / 2 \
            and self.ball_y - self.radius / 2 < self.bar2_y + self.bar_height / 2 \
            and self.ball_y + self.radius / 2 > self.bar2_y - self.bar_height / 2:
                self.p2_score += 1
                self.shift_x = -self.shift_x
                self.shift_y = self.shift_y + self.bar1_offset // 10
        # hit right player
        elif self.ball_x > self.bar1_x - (self.radius + self.bar_width) / 2 \
            and self.ball_y - self.radius / 2 < self.bar1_y + self.bar_height / 2 \
            and self.ball_y + self.radius / 2 > self.bar1_y - self.bar_height / 2:
                self.p1_score += 1
                self.shift_x = -self.shift_x
                self.shift_y = self.shift_y + self.bar1_offset // 10
        # right player out of bound
        elif self.ball_x - self.radius/2 > self.window_width:
            self.p1_score -= 1
            self.reset_ball()
        # left player out of bound
        elif not self.mode and self.ball_x + self.radius/2 < 0:
            self.p2_score -= 1
            self.reset_ball()
        self.ball_x = self.ball_x + self.shift_x
        self.ball_y = self.ball_y + self.shift_y
        self.canvas.move(self.ball, self.shift_x, self.shift_y)
        self.canvas.tag_raise(self.ball)

    # reset ball position
    def reset_ball(self):
        self.ball_x = self.window_width / 2
        self.ball_y = self.window_height / 2
        self.shift_x = 20
        self.shift_y = 0
        self.canvas.delete(self.ball)
        self.ball = self.canvas.create_oval(self.ball_x - self.radius, 
                                    self.ball_y - self.radius,
                                    self.ball_x + self.radius, 
                                    self.ball_y + self.radius, 
                                    fill="#ff9a1f", outline="")

    # update player score display
    def update_display(self):
        # player 1
        if self.p1_display is not None:
            self.canvas.delete(self.p1_display)
        self.p1_display = self.canvas.create_text(1100, self.window_height / 2, text=str(self.p1_score), fill="#38271d", font=('Calibri 300'))
        # player 2
        if not self.mode:
            if self.p2_display is not None:
                self.canvas.delete(self.p2_display)
            self.p2_display = self.canvas.create_text(400, self.window_height / 2, text=str(self.p2_score), fill="#38271d", font=('Calibri 300'))
    

    def on_close(self):
        print("exiting...")
        self.exit = True
        self.window.destroy()
