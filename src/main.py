from engine import Engine

WIDTH, HEIGHT = (500, 300) #(1280, 720) # (1920, 1080)

if __name__=="__main__":
    e = Engine(WIDTH, HEIGHT)
    e.run()