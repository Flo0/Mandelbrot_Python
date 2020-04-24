import numpy as np
from PIL import Image
import time

# -------------------------  Prameter  ------------------------- #
# Bildweite
image_width = 1280
# Bildhöhe
image_height = 720
# Anzahl der Iterationen. Höherer Wert bedeutet bessere Auflösung
# an den Rändern des Mandelbrotsets aber auch (wesentlich) mehr CPU Aufwand.
iterations = 200
# Setze auf True zum exportieren
save_image_afterwards = False
image_format = "PNG"
seconds_between_progress_notice = 1.5
# Ab hier nichts verhändern
__pixel_amount = image_width * image_height
__pixel_counter = 0
__last_notice = time.time()


# -------------------------    Util    ------------------------- #
# Nur eine util Funktion
# Unix time ist normalerweise ein long aber
# Python gibt mir einen double...
def get_unix_time():
    return int(time.time())


# ------------------------- Funktional ------------------------- #

# Wir haben eine komplexe Ebene (x = real, y = imaginär [Hier unser Bild])
# Für jeden Integer Punkt auf dieser Ebene bilden wir eine komplexe Zahl c0.
#
# Jetzt testen wir, ob die Funktion f = z^2 + c0 divergiert
# Wir starten die Iteration bei z = 0 bis zum festgelegten Punkt 'iterations'
#
# nach jeder Iteration wird:
# 1) Getestet, ob der Betrag von z größer ist als 2 (wir erinnern uns an sqrt(re^2 + im^2))
#    Wenn die Zahl jemals größer wird als 2 dann wird sie sicher divergieren. (Noch nicht ganz verstanden warum)
# 2) z neu festgelegt als z = z^2 + c0 für die nächste Iteration
#    wir benutzen also das vorherige Ergebnis unserer Funktion als neuen
#    Parameter in der nächsten Iteration (rekursion)
#
# Wenn die Zahl nach 'iterations'-maliger Iteration immer noch nicht divergiert,
# dann gehen wir einfach von konvergenz aus.
#
# Nun zur Darstellung als Bild.
# Bei Konvergenz returnen wir einen Tuple(0, 0, 0) also Schwarz
# Bei Divergenz returnen wir bei welcher Iteration die Zahl divergiert ist.
# Diese Zahl liegt zwischen 0 und 'iterations'
# Mit der Funktion toRGB() wandeln wir jetzt diese Zahl von 0 - 'iterations'
# in einen RGB Tuple(R, G, B) um, welcher uns einen farbigeb Pixel liefert
def mandelbrot(re, im):
    c0 = complex(re, im)
    z = 0
    for i in range(1, iterations):
        if abs(z) > 2:
            return toRGB(i)
        z = z ** 2 + c0
    return 0, 0, 0


# Damit kann man rumspielen
# Ich habe jetzt mal R, G und B den gleichen Wert
# zwischen 0 und 255 gegebn. (Abhängig von der Anzahl der Iterationen)
# Daraus folgen Graustufen
def toRGB(i):
    percent_of_iter = 1.0 / iterations * i
    value = percent_of_iter * 255
    return value, value, value


# Ein Beispiel für rot-stufen
# https://i.imgur.com/LensYSX.png
def toRGB_redonly(i):
    percent_of_iter = 1.0 / iterations * i
    value = percent_of_iter * 255
    return value, 0, 0


# Etwas bunter
# https://i.imgur.com/qFPmMt2.png
def rotRGB_colorfull(i):
    percent_of_iter = 1.0 / iterations * i
    value = percent_of_iter * 255 * 40
    r, g, b = 0, 0, 0
    if value <= 255:
        r = value
    if 255 < value <= 255 * 2:
        g = value / 2
    if 255 * 2 <= value <= 255 * 3:
        b = value / 3
    return r, g, b


# Zeigt den Fortschritt an
def show_progess():
    print("Fortschritt: %.2f %%" % ((100.0 / __pixel_amount) * __pixel_counter))


# ------------------------- Execution ------------------------- #

# Wir erstellen 3D array (Weite, Höhe, RGB)
# Also ein Fläche mit 3 Ebenen, welche jeweils Rot, Grün oder Blau darstellen
# RGB Werte liegen zwischen 0 und 255 deswegen füllen wir das array nur mit 8 bit ints
# np.zeros initialisiert jeden Wert mit effektiv 0
# Dieses array würde dargestellt einfach ein Schwarzes Bild sein, da jeder Pixel
# mit (0, 0, 0) als RGB also Schwarz angezeigt wäre [(255, 255, 255) ist übrigens Weiß]
data = np.zeros((image_height, image_width, 3), dtype=np.uint8)

show_progess()
# Wir iterieren durch jeden Pixel (x und y) und bilden sie auf die
# komplexe Ebene ab.
for x in range(0, image_width):
    for y in range(0, image_height):
        __pixel_counter += 1
        # Fortschritt
        if time.time() - __last_notice >= seconds_between_progress_notice:
            __last_notice = time.time()
            show_progess()
        # Hier verschiebe und strecke ich das Bild um x und y so, dass der Koordinaten-
        # ursprung der Komplexen Ebene in der Mitte des Bilds liegt.
        # Das wurde eher so Pi*Daumen gemacht.
        dx = (x - (0.75 * image_width)) / (image_width / 4)
        dy = (y - (image_height / 2)) / (image_height / 2.5)
        # Hier wird für den Pixel (x, y) getestet, ob die Funktion divergiert.
        # Siehe def mandelbrot
        mandelResult = mandelbrot(dx, dy)
        # Wir legen jetzt Rot, Grün und Blau fest
        data[y][x][0] = mandelResult[0]
        data[y][x][1] = mandelResult[1]
        data[y][x][2] = mandelResult[2]

show_progess()
print("Done")
# -------------------------     IO     ------------------------- #

img = Image.fromarray(data, "RGB")
if save_image_afterwards:
    img.save(str(get_unix_time()) + "." + image_format.lower(), image_format)
img.show()
