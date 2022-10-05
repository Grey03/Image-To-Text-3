# Image To Text 3
Hello all! Welcome to Image to Text 3.0! I've made some in the past. This started with a simple python script that you run in the console. All it did was a 1 to 1 conversion of an image to a bullet point text are. The second I made took that further. It instead use braille letters which would 1 make the file smaller but also see more detail with less letters. Each I had made did their own thing, the second actually had a gui. Well good things come in 3s right?! Welp with 3.0 It combines the two previous scripts with a new one that makes "SHADING". It has a nicer ui too!

I'm sorry for bad spelling or grammar; I'm just crappy at grammar haha.

I will say the code is messy, and I've learned more from it. With each program I write I learn more and I had exactly that with this. It seems to be a bit faster than the older scripts but now you can spice it up more.

In the settings.json file you will see "ComplexThemes" this is something that can only be changed by hand. The "SimplySym" can be changed in the settings menu. Basically one can create a custom pallete for the Complex mode that has "Shading". To simplify that is a list, it will assume the first character is the "lightest" and the last is the "darkest". It will equally dived them among the spectrum of brightness so make whatever you want. Aslong as it has a custom name and a list like ["<character>",] it will work.

 Some explanation
 A quick breakdown on the simple mode, it looks at each pixel if its brightness is greater than or equal to the contrast setting it will make a dot, it is that simeple.
 For an explanation on the compact/compressed mode, just look at my repositorie called Image to braille. It's readme explains it.
 I will explain the Complex mode here due to it not being said and not so simple. First it looks at the theme chosen. It then divides 256(The max brightness) by the number of symbols in the theme. This leaves each theme an equal portion of the brightness scale. A selected pixel will find the nearest symbol and use that for its spot. It is simple mode but with different symbols on brightness. It takes a bit longer because it has to first get the pixel data and then find out what it is closest to which takes time.
 
 
