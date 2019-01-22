package context

import (
	"bufio"
	"gospider/config"
	"gospider/utils"
	"io"
	"log"
	"net/http"
	"os"
)

type Image struct {
	Url    string
	File   string
	Folder string
}

func (image *Image) Download(ctx *Context, client *http.Client) {
	req, err := http.NewRequest("GET", image.Url, nil)
	utils.CheckError(err, "Image[1]: failed to create request!")

	resp, err := client.Do(req)
	utils.CheckError(err, "Image[2]: failed to request the url "+image.Url)

	err = os.MkdirAll(image.Folder, 0755)
	utils.CheckError(err, "Image[3]: failed to create directory for saving file!")
	img, err := os.Create(image.File)
	utils.CheckError(err, "Image[4]: failed to create file!")

	writer := bufio.NewWriterSize(img, config.BufSize)
	_, err = io.Copy(writer, resp.Body)
	utils.CheckError(err, "Image[5]: failed to copy image from response body!")

	_ = writer.Flush()
	ctx.ImageState[image.Url] = config.Success
	log.Println("Image: Successfully fetch a image!", image.Url)
}
