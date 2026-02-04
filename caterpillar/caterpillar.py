import time

class Caterpillar:
    def __init__(self):
        self.state = "egg"
        self.stomach = []
        self.days = [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ]
        self.day_index = 0

    def hatch(self):
        print("In the light of the moon a little egg lay on a leaf.")
        time.sleep(1)
        print("One Sunday morning the warm sun came up and - pop! - out of the egg came a tiny and very hungry caterpillar.")
        self.state = "caterpillar"
        self.day_index = 0  # Starts eating on Monday

    def eat(self):
        if self.state != "caterpillar":
            print("The caterpillar is not here to eat!")
            return

        day = self.days[self.day_index]
        print(f"\nOn {day}, he ate through:")

        if day == "Monday":
            food = ["1 apple"]
        elif day == "Tuesday":
            food = ["2 pears"]
        elif day == "Wednesday":
            food = ["3 plums"]
        elif day == "Thursday":
            food = ["4 strawberries"]
        elif day == "Friday":
            food = ["5 oranges"]
        elif day == "Saturday":
            food = [
                "1 piece of chocolate cake", "1 ice-cream cone", "1 pickle",
                "1 slice of Swiss cheese", "1 slice of salami", "1 lollipop",
                "1 piece of cherry pie", "1 sausage", "1 cupcake", "1 slice of watermelon"
            ]
            print(f"  {', '.join(food)}")
            print("That night he had a stomachache!")
            self.stomach.extend(food)
            self.day_index += 1
            return # Skip iterating, special case

        elif day == "Sunday": # The next Sunday
            print("  1 nice green leaf")
            print("And after that he felt much better.")
            self.state = "fat_caterpillar"
            return

        for item in food:
            print(f"  {item}")
        self.stomach.extend(food)
        
        # Advance day unless it's Sunday (end of eating cycle)
        if self.day_index < 6:
            self.day_index += 1

    def transform(self):
        if self.state == "fat_caterpillar":
            print("\nNow he wasn't hungry any more - and he wasn't a little caterpillar any more.")
            print("He was a big, fat caterpillar.")
            time.sleep(1)
            print("He built a small house, called a cocoon, around himself.")
            self.state = "cocoon"
            time.sleep(1)
            print("He stayed inside for more than two weeks.")
            time.sleep(1)
            print("Then he nibbled a hole in the cocoon, pushed his way out and...")
            time.sleep(1)
            print("He was a beautiful butterfly!")
            self.state = "butterfly"
        else:
            print("He's not ready to transform yet!")

def main():
    caterpillar = Caterpillar()
    caterpillar.hatch()
    
    # Go through the week
    for _ in range(7): 
        time.sleep(1)
        caterpillar.eat()
        
    # The next Sunday
    time.sleep(1)
    caterpillar.eat() # Eat the leaf
    
    # Transformation
    time.sleep(1)
    caterpillar.transform()

if __name__ == "__main__":
    main()
