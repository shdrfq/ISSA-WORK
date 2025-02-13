import matplotlib.pyplot as plt
import numpy as np

class MarlaHome:
    def __init__(self, width=25, height=45, rooms=2, bathrooms=1, lawn=True, garage=False):
        self.width = width  # feet
        self.height = height  # feet
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.lawn = lawn
        self.garage = garage
    
    def display_details(self):
        return {
            "Width (ft)": self.width,
            "Height (ft)": self.height,
            "Rooms": self.rooms,
            "Bathrooms": self.bathrooms,
            "Lawn": "Yes" if self.lawn else "No",
            "Garage": "Yes" if self.garage else "No"
        }
    
    def draw_house(self):
        fig, ax = plt.subplots(figsize=(5, 8))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        
        # Draw house boundary
        house_boundary = plt.Rectangle((0, 0), self.width, self.height, fill=None, edgecolor='black', linewidth=2)
        ax.add_patch(house_boundary)
        
        # Draw rooms
        for i in range(self.rooms):
            ax.add_patch(plt.Rectangle((5, (i+1) * (self.height / (self.rooms + 2))), self.width-10, self.height / (self.rooms + 2), fill=True, color='lightgray', edgecolor='black'))
            ax.text(self.width / 2, (i+1) * (self.height / (self.rooms + 2)) + 2, f"Room {i+1}", fontsize=10, ha='center')
        
        # Draw bathrooms
        for i in range(self.bathrooms):
            ax.add_patch(plt.Rectangle((self.width - 7, (i+1) * (self.height / 6)), 5, self.height / 6, fill=True, color='blue', edgecolor='black'))
            ax.text(self.width - 4.5, (i+1) * (self.height / 6) + 2, "Bath", fontsize=8, ha='center')
        
        # Draw lawn if present
        if self.lawn:
            ax.add_patch(plt.Rectangle((0, 0), self.width, 5, fill=True, color='green', edgecolor='black'))
            ax.text(self.width / 2, 2, "Lawn", fontsize=10, ha='center', color='white')
        
        # Draw garage if present
        if self.garage:
            ax.add_patch(plt.Rectangle((0, self.height - 10), self.width / 3, 10, fill=True, color='gray', edgecolor='black'))
            ax.text(self.width / 6, self.height - 5, "Garage", fontsize=10, ha='center', color='white')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("5 Marla Home Design")
        plt.show()

# Get user input
rooms = int(input("Enter number of rooms: "))
bathrooms = int(input("Enter number of bathrooms: "))
lawn = input("Do you want a lawn? (yes/no): ").strip().lower() == "yes"
garage = input("Do you want a garage? (yes/no): ").strip().lower() == "yes"

# Create a house object with user input
my_house = MarlaHome(rooms=rooms, bathrooms=bathrooms, lawn=lawn, garage=garage)
print(my_house.display_details())

# Draw the house
my_house.draw_house()
