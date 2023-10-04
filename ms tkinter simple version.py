import math
import tkinter as tk

window = tk.Tk()
max_dwell,max_square_depth,canvas_length,center,side = 150,10,750,(-0.5,0),3  # variables to change
counter = 0
start_x, start_y,end_x, end_y = center[0] - side/2,center[1] + side/2,center[0] + side/2,center[1] - side/2
canvas = tk.Canvas(window, width=canvas_length, height=canvas_length)
canvas.pack()


def color_fn(c):
    if c == max_dwell:
        return 0,0,0
    else:
        # return 255,255,255
        return tuple([int(255 * (math.sin(3.1415923 * ((c+j) / 20)) ** 2)) for j in [0,5,10]])  # faster w/o trig?


def check_bounded(x, y):
    xa, ya = x + canvas_length / 2, y + canvas_length / 2
    graph_width, graph_height = end_x - start_x, end_y - start_y
    percent_x, percent_y = xa / canvas_length, ya / canvas_length
    x1, y1 = start_x + graph_width * percent_x, start_y + graph_height * percent_y
    n = (0, 0)
    for d in range(max_dwell):
        n = n[0]**2 - n[1]**2 + x1,2*n[0]*n[1] + y1
        if math.sqrt(n[0] ** 2 + n[1] ** 2) > 2:
            # if n[0] >= 2 or n[1] >= 2:
            return d
    return max_dwell


def polygon(color,x,y,sl):  # color is in rgb
    canvas.create_polygon([i + canvas_length / 2 for i in [x,y,x+sl,y,x+sl,y-sl,x,y-sl]],outline="#%02x%02x%02x" % color)


def square_layer(x_start, y_start, length, top0, bottom0, left0, right0):
    global counter
    counter += 1
    middle_horizontal_left = [check_bounded(i, y_start - length)
                              for i in range(int(x_start), int(x_start + length))]
    middle_horizontal_right = [check_bounded(i, y_start - length)
                               for i in range(int(x_start + length), int(x_start + 2 * length))]
    middle_vertical_top = [check_bounded(x_start + length, i)
                           for i in range(int(y_start), int(y_start - length), -1)]
    middle_vertical_bottom = [check_bounded(x_start + length, i)
                              for i in range(int(y_start - length), int(y_start - 2 * length), -1)]
    split_x,split_y = -int(x_start) + int(x_start + length),int(y_start) - int(y_start - length)
    for each_square in range(4):
        x_translated = x_start + length * (each_square % 2)
        y_translated = y_start - length * int((each_square - (each_square % 2)) / 2)
        top = [top0[:split_x], top0[split_x:], middle_horizontal_left, middle_horizontal_right][each_square]
        bottom = [middle_horizontal_left, middle_horizontal_right, bottom0[:split_x], bottom0[split_x:]][each_square]
        left = [left0[:split_y], middle_vertical_top, left0[split_y:], middle_vertical_bottom][each_square]
        right = [middle_vertical_top, right0[:split_y], middle_vertical_bottom, right0[split_y:]][each_square]
        combined = top + bottom + left + right
        if len(combined) > 0:
            rgb = color_fn(combined[0])
            if all(x == combined[0] for x in combined):
                polygon(rgb,x_translated,y_translated,length)
            else:
                if counter < max_square_depth:
                    square_layer(x_translated, y_translated, length / 2, top, bottom, left, right)
                    counter -= 1
                else:
                    polygon(rgb,x_translated,y_translated,max(0.5,length))


square_layer(int(canvas_length / -2), int(canvas_length / 2), int(canvas_length / 2),
             [check_bounded(i, (canvas_length / 2))
              for i in range(int(canvas_length / (-2)), int(canvas_length / 2))],
             [check_bounded(i, (canvas_length / (-2)))
              for i in range(int(canvas_length / (-2)), int(canvas_length / 2))],
             [check_bounded(int(canvas_length / -2), i)
              for i in range(int(canvas_length / 2), int(canvas_length / (-2)), -1)],
             [check_bounded(int(canvas_length / 2), i)
              for i in range(int(canvas_length / 2), int(canvas_length / (-2)), -1)],
             )
canvas.mainloop()
