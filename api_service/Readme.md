

## Objective : 
- To have a Go Server running as a backend service.
- Will use just Http(for trial) and Https(for prod) 
- The Go server will have 2 end-points as of now.
    - /v1/get_image -> Returns a compresed and base64 encoded image data in json. 
    - /v1/stream_image -> Returns a HTTP stream maybe returns a fetch or something like that.


## Uses : 
- For sending data we use PiCamera written in GoLang 
- Documentation : https://pkg.go.dev/github.com/gbbirkisson/picamera#section-readme 
