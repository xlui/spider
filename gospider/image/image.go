package image

import (
	"gospider/context"
	"net/http"
)

type Image struct {
	Url    string
	File   string
	Folder string
}

func (image *Image) Download(ctx *context.Context, client *http.Client) {

}
