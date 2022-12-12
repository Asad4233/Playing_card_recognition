import cv2
import os
from tqdm import tqdm
import numpy as np
from utils import make_folder


def generate_individual_card_suits(suit_folder, output_folder=""):
    # find all cards in the image
    # find the suit of each card
    # save each card in a folder

    suit_folder_images = [
        os.path.join(suit_folder, image)
        for image in os.listdir(suit_folder)
        if ".png" in image or ".jpg" in image
    ]

    suit_name = suit_folder.split("/")[-1]
    make_folder(os.path.join("Dataset", "Cards"))
    output_folder = os.path.join("Dataset", "Cards", f"{suit_name}_cards")
    make_folder(output_folder)

    i = 0
    for image in tqdm(suit_folder_images, leave=False):
        image_color = cv2.imread(image)

        image = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        image = cv2.Canny(image, 150, 250)

        # cv2.imshow("image", image)
        # cv2.waitKey(0)


        ret, thresh = cv2.threshold(image, 127, 255, 0)
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        for contour in tqdm(contours, leave=False):
            # Approximate the corner points of the card
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
            pts = np.float32(approx)

            x, y, w, h = cv2.boundingRect(contour)

            print(x, y, w, h)

            if w > 200 and h > 150:
            
                # Crop the card
                crop = image_color[y : y + h, x : x + w]
                crop = cv2.resize(crop, (150, 230), interpolation=cv2.INTER_LINEAR)

                # Save the card
                image_name = os.path.join(output_folder, f"{str(i)}.png")
                cv2.imwrite(image_name, crop)
                i += 1


def main():
    os.system("clear")

    suits = [
        os.path.join("Dataset", suit)
        for suit in os.listdir("Dataset")
        if os.path.isdir(os.path.join("Dataset", suit) 
        )
    ]

    for suit in tqdm(suits, leave=False):
        generate_individual_card_suits(suit)


if __name__ == "__main__":
    main()
