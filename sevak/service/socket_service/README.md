### Idea : 
Idea is to have a Pub, Sub Model right ! 
Now what happens is I have 3 services right now. 

- Camera Service : Takes a picture and pubs a data/get_image/rgb_image or data/get_stream/rgb_image.
- Detection Service : Would run some kind of Object Detection here it will sub to data/*/rgb_image and pub data/obj_detect_image
- Data_Stream Service : 
   - Sends data to a Public hosted IP via Websockets.
   - Can also take a payload right, please note websockets is basically a port opened. 
   - Would send something like to RaspberryPi. 
	a) take_image
	b) take_stream ${TIMEOUT}
	c) take_stream INF -> Runs a while loop here.
	d) take_image AND detect_image -> Runs serially (first takes the image and thenn runs Obj Detection).

### Notes :
- The Webserver would be written in either Rust or GoLang. 
- Would see what do I prefer more.



